import flet as ft
import qrcode
import os
import json
import base64
import io
import asyncio
import time

ARCHIVO_CONFIG = "config.json"

def AsistenciaView(page: ft.Page, auth_controller=None):
    main_container = ft.Container(expand=True)

    def cargar_grupos():
        if os.path.exists(ARCHIVO_CONFIG):
            with open(ARCHIVO_CONFIG, "r") as f:
                try: return json.load(f)
                except: return ["6-D", "6-E"]
        return ["6-D", "6-E"]

    grupos = cargar_grupos()
    qr_activo = [False]

    def guardar_grupos_en_archivo(lista_grupos):
        with open(ARCHIVO_CONFIG, "w") as f:
            json.dump(lista_grupos, f)

    def generar_qr_para_grupo(nombre_grupo):
        codigo = f"ASISTENCIA-{nombre_grupo}-{int(time.time()//60)}"
        qr = qrcode.make(codigo)
        buffered = io.BytesIO()
        qr.save(buffered, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

    def abrir_dialogo_grupo(e):
        campo_nombre = ft.TextField(label="Nombre del grupo (ej: 6-F)")
        def cerrar_dialogo(e):
            dlg_modal.open = False
            page.update()

        def procesar_guardado(e):
            nuevo_nombre = campo_nombre.value
            if nuevo_nombre and nuevo_nombre not in grupos:
                grupos.append(nuevo_nombre)
                guardar_grupos_en_archivo(grupos)
                dlg_modal.open = False
                main_container.content = build_selector_grupos()
                page.update()
        dlg_modal = ft.AlertDialog(modal=True, title=ft.Text("Agregar Nuevo Grupo"), content=campo_nombre,
            actions=[ft.TextButton("Cancelar", on_click=cerrar_dialogo), ft.TextButton("Guardar", on_click=procesar_guardado)])
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()

    def eliminar_grupo(e, nombre_grupo):
        def confirmar_eliminacion(e_confirm):
            if nombre_grupo in grupos:
                grupos.remove(nombre_grupo)
                guardar_grupos_en_archivo(grupos)
                main_container.content = build_selector_grupos()
                page.update()
            dlg_confirmacion.open = False
            page.update()
        dlg_confirmacion = ft.AlertDialog(modal=True, title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar el grupo {nombre_grupo}?"),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg_confirmacion, "open", False) or page.update()), 
                    ft.TextButton("Eliminar", on_click=confirmar_eliminacion, style=ft.ButtonStyle(color=ft.Colors.RED))])
        page.overlay.append(dlg_confirmacion)
        dlg_confirmacion.open = True
        page.update()

    def ir_a_gestion_grupo(e, nombre_grupo):
        main_container.content = build_vista_gestion(nombre_grupo)
        page.update()

    def volver_grupos(e=None):
        qr_activo[0] = False
        main_container.content = build_selector_grupos()
        page.update()

    def build_vista_gestion(nombre_grupo):
        def ir_al_login(e):
            page.route = "/"  
            page.go("/")
        img_qr = ft.Image(src=generar_qr_para_grupo(nombre_grupo), width=200, height=200)
        qr_activo[0] = True
        alumnos_totales = auth_controller.obtener_alumnos_presentes(nombre_grupo) if auth_controller else []
        filtro_fecha = [None]
        lista_columna = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        def filtrar_datos(e=None):
            query = buscador.value.lower()
            lista_columna.controls.clear()
            for al in alumnos_totales:
                nombre_coincide = query in str(al.get('nombre', '')).lower()
                fecha_al = str(al.get('fecha', '')).strip()
                fecha_sel = str(filtro_fecha[0] or '').strip()
                fecha_coincide = (filtro_fecha[0] is None) or (fecha_al == fecha_sel)
                if nombre_coincide and fecha_coincide:
                    lista_columna.controls.append(
                        ft.Container(
                            bgcolor=ft.Colors.GREEN_50, border_radius=10, padding=10,
                            margin=ft.margin.Margin(0, 0, 0, 10),
                            content=ft.ListTile(
                                leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREEN_700),
                                title=ft.Text(al.get('nombre', 'Sin nombre'), weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(f"Fecha: {al.get('fecha', 'N/A')} | Hora: {al.get('hora', 'N/A')}")
                            )
                        )
                    )
            page.update()

        async def refrescar_qr():
            await asyncio.sleep(1)
            while qr_activo[0]:               
                try:
                    if img_qr.page is not None:
                        if auth_controller and hasattr(auth_controller, "rotar_codigo_qr"):
                            auth_controller.rotar_codigo_qr()
                        img_qr.src = generar_qr_para_grupo(nombre_grupo)
                        page.update()
                except Exception as ex:
                    print("Error actualizando QR:", ex)
                await asyncio.sleep(60)
        buscador = ft.TextField(label="Buscar por nombre", prefix_icon=ft.Icons.SEARCH, on_change=filtrar_datos, width=300)
        btn_calendario = ft.ElevatedButton("Seleccionar Fecha", icon=ft.Icons.CALENDAR_MONTH, on_click=lambda _: setattr(date_picker, "open", True) or page.update())
        
        def on_date_change(e):
            if e.control.value:
                fecha_str = e.control.value.strftime('%Y-%m-%d')
                filtro_fecha[0] = fecha_str
                btn_calendario.text = f"Fecha: {fecha_str}"
                btn_calendario.update()
                filtrar_datos()
        date_picker = ft.DatePicker(on_change=on_date_change)
        page.overlay.append(date_picker)
        filtrar_datos()        
        page.run_task(refrescar_qr)
        return ft.Row(expand=True, vertical_alignment=ft.CrossAxisAlignment.START, controls=[
            ft.Column(expand=2, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK, on_click=volver_grupos), 
                        ft.Text(f"Gestionando: {nombre_grupo}", size=20, weight="bold")
                    ]),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color=ft.Colors.RED, tooltip="Cerrar sesión", on_click=ir_al_login)
                ]),
                ft.Row([buscador, btn_calendario]),
                ft.Divider(),
                ft.Text("Registrados", size=18, weight="bold"),
                ft.Container(expand=True, content=lista_columna)
            ]),
            ft.Container(width=250, padding=20, bgcolor=ft.Colors.GREY_50, border_radius=15, 
                content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Text("Código de Acceso", weight="bold"), img_qr
            ]))
        ])

    def build_selector_grupos():
        tarjetas = [ft.Container(
            padding=15, border_radius=15, bgcolor=ft.Colors.GREY_50,
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.END, controls=[ft.IconButton(ft.Icons.DELETE_FOREVER, icon_color=ft.Colors.RED_400, on_click=lambda e, n=g: eliminar_grupo(e, n))]),
                ft.Icon(ft.Icons.GROUP, size=50, color=ft.Colors.INDIGO_600),
                ft.Text(g, size=18, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Seleccionar", bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE, on_click=lambda e, n=g: ir_a_gestion_grupo(e, n))
            ])
        ) for g in grupos]
        return ft.Column(expand=True, controls=[
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Gestión de Asistencia", size=28, weight="bold"), ft.ElevatedButton("Nuevo Grupo", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, on_click=abrir_dialogo_grupo)]),
            ft.Divider(),
            ft.GridView(expand=True, max_extent=250, spacing=20, run_spacing=20, controls=tarjetas)
        ])

    main_container.content = build_selector_grupos()
    return ft.View(route="/asistencia", controls=[ft.Container(width=900, height=650, bgcolor=ft.Colors.WHITE, border_radius=20, padding=30, content=main_container)])