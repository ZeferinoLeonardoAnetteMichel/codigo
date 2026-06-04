import flet as ft
import qrcode
import os

def AsistenciaView(page: ft.Page, auth_controller=None):
    main_container = ft.Container(expand=True)
    grupos = ["6-D", "6-E"]

    # --- Lógica de QR ---
    def generar_qr_para_grupo(nombre_grupo):
        if not os.path.exists("assets"): os.makedirs("assets")
        ruta = f"assets/qr_{nombre_grupo.replace('-', '_')}.png"
        qr = qrcode.make(f"ASISTENCIA-{nombre_grupo}")
        qr.save(ruta)
        return ruta
    
    def abrir_dialogo_grupo(e):
        campo_nombre = ft.TextField(label="Nombre del grupo (ej: 6-F)")
        
        def cerrar_dialogo(e):
            dlg_modal.open = False
            page.update()

        def guardar_nuevo_grupo(e):
            nuevo_nombre = campo_nombre.value
            if nuevo_nombre:
                grupos.append(nuevo_nombre)
                dlg_modal.open = False
                main_container.content = build_selector_grupos()
                page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar Nuevo Grupo"),
            content=campo_nombre,
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.TextButton("Guardar", on_click=guardar_nuevo_grupo),
            ],
        )
        
        # FUERZA la apertura y el refresco
        page.overlay.append(dlg_modal) # Algunos contenedores prefieren el overlay
        dlg_modal.open = True
        page.update()

    # --- Navegación ---
    def ir_a_gestion_grupo(e, nombre_grupo):
        main_container.content = build_vista_gestion(nombre_grupo)
        page.update()

    def volver_grupos(e=None):
        main_container.content = build_selector_grupos()
        page.update()

    # --- Vistas ---
    def build_vista_gestion(nombre_grupo):
        alumnos = auth_controller.obtener_alumnos_presentes(nombre_grupo)
        ruta_qr = generar_qr_para_grupo(nombre_grupo)

        lista_widgets = [
            ft.Container(
                bgcolor=ft.Colors.GREEN_50, border_radius=10, padding=5,
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREEN_700),
                    title=ft.Text(al['nombre'], weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"Hora: {al['hora']}"),
                )
            ) for al in alumnos
        ]

        return ft.Row(expand=True, controls=[
            ft.Column(expand=2, controls=[
                ft.Text(f"Gestionando: {nombre_grupo}", size=20, weight="bold"),
                ft.ElevatedButton("Volver", on_click=volver_grupos),
                ft.Divider(),
                ft.Text("Registrados", size=18, weight="bold"),
                ft.Column(controls=lista_widgets)
            ]),
            ft.Container(expand=1, padding=20, bgcolor=ft.Colors.GREY_50, border_radius=15,
                content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Text("Código de Acceso", weight="bold"),
                    ft.Image(src=ruta_qr, width=180, height=180),
                    ft.Text("Cambia cada 5 minutos", size=12, color=ft.Colors.GREY_600)
                ])
            )
        ])

    def build_selector_grupos():
        tarjetas = [
            ft.Container(
                padding=20, border_radius=15, bgcolor=ft.Colors.GREY_50,
                content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                    ft.Icon(ft.Icons.GROUP, size=50, color=ft.Colors.INDIGO_600),
                    ft.Text(g, size=18, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Seleccionar", bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE,
                                    on_click=lambda e, n=g: ir_a_gestion_grupo(e, n))
                ])
            ) for g in grupos
        ]

        return ft.Column(expand=True, controls=[
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Text("Gestión de Asistencia", size=28, weight=ft.FontWeight.BOLD),
ft.ElevatedButton(
    "Nuevo Grupo", 
    bgcolor=ft.Colors.GREEN, 
    color=ft.Colors.WHITE, 
    on_click=lambda e: abrir_dialogo_grupo(e) # Lambda asegura la ejecución del evento
)
            ]),
            ft.Divider(),
            ft.GridView(expand=True, max_extent=250, spacing=20, run_spacing=20, controls=tarjetas)
        ])

    # Inicialización
    main_container.content = build_selector_grupos()
    
    return ft.View(
        route="/asistencia",
        controls=[
            ft.Container(
                width=900, height=650, bgcolor=ft.Colors.WHITE, 
                border_radius=20, padding=30, content=main_container
            )
        ]
    )