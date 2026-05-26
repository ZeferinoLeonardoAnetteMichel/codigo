import flet as ft

def AsistenciaView(page: ft.Page, auth_controller=None):
    
    # --- FUNCIONES DE ACCIÓN ---
    def volver_al_dashboard(e):
        page.go("/dashboard")

    # =========================================================================
    # DATOS DE PRUEBA (Aquí harás tus consultas SQL reales con tu auth_controller)
    # =========================================================================
    alumnos_presentes = [
        {"matricula": "2026001", "nombre": "Carlos Mendoza Ortiz", "hora": "07:02 AM"},
        {"matricula": "2026042", "nombre": "Ana Valeria Gómez", "hora": "07:05 AM"},
        {"matricula": "2026015", "nombre": "Luis Fernando Perea", "hora": "07:11 AM"},
    ]
    
    alumnos_ausentes = [
        {"matricula": "2026089", "nombre": "Diana Laura Martínez"},
        {"matricula": "2026112", "nombre": "Jorge Alberto Ríos"},
    ]

    # =========================================================================
    # 1. PRIMERO DECLARAMOS LAS TABLAS VACÍAS O CON SUS DATOS INICIALES
    # =========================================================================
    tabla_presentes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Matrícula", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
            ft.DataColumn(ft.Text("Nombre Completo", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
            ft.DataColumn(ft.Text("Hora de Entrada", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
            ft.DataColumn(ft.Text("Estatus", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(al["matricula"])),
                ft.DataCell(ft.Text(al["nombre"])),
                ft.DataCell(ft.Text(al["hora"])),
                ft.DataCell(ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600, size=20)),
            ]) for al in alumnos_presentes
        ],
        heading_row_color=ft.Colors.PURPLE_50,
        border_radius=8,
    )

    tabla_ausentes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Matrícula", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
            ft.DataColumn(ft.Text("Nombre Completo", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
            ft.DataColumn(ft.Text("Estatus", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(al["matricula"])),
                ft.DataCell(ft.Text(al["nombre"])),
                ft.DataCell(ft.Row([
                    ft.Icon(ft.Icons.CANCEL, color=ft.Colors.RED_600, size=20),
                    ft.Text("Ausente", color=ft.Colors.RED_600, size=13, weight=ft.FontWeight.W_500)
                ], spacing=5)),
            ]) for al in alumnos_ausentes
        ],
        heading_row_color=ft.Colors.PURPLE_50,
        border_radius=8,
    )

    # =========================================================================
    # 2. FUNCIÓN DE ACTUALIZACIÓN (RELOAD)
    # =========================================================================
    def actualizar_lista(e):
        tabla_presentes.rows.clear()
        tabla_ausentes.rows.clear()
        
        # Mapeamos los nuevos datos a las filas de Presentes
        for al in alumnos_presentes: 
            tabla_presentes.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(al["matricula"])),
                    ft.DataCell(ft.Text(al["nombre"])),
                    ft.DataCell(ft.Text(al["hora"])),
                    ft.DataCell(ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600, size=20)),
                ])
            )
            
        # Mapeamos los nuevos datos a las filas de Ausentes
        for al in alumnos_ausentes: 
            tabla_ausentes.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(al["matricula"])),
                    ft.DataCell(ft.Text(al["nombre"])),
                    ft.DataCell(ft.Row([
                        ft.Icon(ft.Icons.CANCEL, color=ft.Colors.RED_600, size=20),
                        ft.Text("Ausente", color=ft.Colors.RED_600, size=13, weight=ft.FontWeight.W_500)
                    ], spacing=5)),
                ])
            )
        
        # Notificamos el cambio exitoso con el SnackBar
        snack = ft.SnackBar(ft.Text("¡Lista de asistencia actualizada con éxito!"), bgcolor=ft.Colors.GREEN_600)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # =========================================================================
    # 3. INTERFAZ DINÁMICA DE PESTAÑAS (COMPATIBILIDAD TOTAL) 🚀
    # =========================================================================
    # =========================================================================
    # 3. INTERFAZ DINÁMICA DE PESTAÑAS (COMPATIBILIDAD ULTRA SEGURA) 🚀
    # =========================================================================
    vista_presentes = ft.ListView([
        ft.Container(height=10),
        ft.Row([
            ft.Icon(ft.Icons.PERSON_PIN_ROUNDED, color=ft.Colors.PURPLE_700),
            ft.Text("ALUMNOS PRESENTES", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700, size=16)
        ], alignment=ft.MainAxisAlignment.START, spacing=10),
        ft.Text("Alumnos que escanearon el QR exitosamente hoy:", size=14, color=ft.Colors.BLUE_GREY_600, italic=True),
        ft.Container(height=10),
        ft.Container(content=tabla_presentes, bgcolor=ft.Colors.WHITE, padding=10, border_radius=10)
    ], spacing=10, expand=True)

    vista_ausentes = ft.ListView([
        ft.Container(height=10),
        ft.Row([
            ft.Icon(ft.Icons.PERSON_OFF_ROUNDED, color=ft.Colors.RED_700),
            ft.Text("ALUMNOS AUSENTES", weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700, size=16)
        ], alignment=ft.MainAxisAlignment.START, spacing=10),
        ft.Text("Alumnos pendientes de registrar asistencia:", size=14, color=ft.Colors.BLUE_GREY_600, italic=True),
        ft.Container(height=10),
        ft.Container(content=tabla_ausentes, bgcolor=ft.Colors.WHITE, padding=10, border_radius=10)
    ], spacing=10, expand=True)

    # El contenedor del cuerpo arranca mostrando la lista de presentes
    seccion_activa = ft.Container(content=vista_presentes, expand=True)

    # Controlador para cambiar de tabla al hacer clic
    def cambiar_seccion(e):
        # Evaluamos el contenido del texto interno del botón de forma segura
        if e.control.data == "presentes":
            seccion_activa.content = vista_presentes
            btn_ver_presentes.bgcolor = ft.Colors.PURPLE_100
            btn_ver_ausentes.bgcolor = ft.Colors.TRANSPARENT
        else:
            seccion_activa.content = vista_ausentes
            btn_ver_ausentes.bgcolor = ft.Colors.RED_100
            btn_ver_presentes.bgcolor = ft.Colors.TRANSPARENT
        page.update()

    # Botones usando 'content' y 'data' para evitar parámetros conflictivos de Flet
    btn_ver_presentes = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.PERSON_PIN_ROUNDED, color=ft.Colors.PURPLE_800), ft.Text("Presentes", color=ft.Colors.PURPLE_800)], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        bgcolor=ft.Colors.PURPLE_100,
        padding=10,
        border_radius=8,
        on_click=cambiar_seccion,
        data="presentes"
    )
    
    btn_ver_ausentes = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.PERSON_OFF_ROUNDED, color=ft.Colors.BLUE_GREY_400), ft.Text("Ausentes", color=ft.Colors.BLUE_GREY_400)], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        bgcolor=ft.Colors.TRANSPARENT,
        padding=10,
        border_radius=8,
        on_click=cambiar_seccion,
        data="ausentes"
    )

    # Estructura limpia que emula las pestañas nativas
    contenedor_pestanas = ft.Column([
        ft.Row([btn_ver_presentes, btn_ver_ausentes], alignment=ft.MainAxisAlignment.START, spacing=10),
        ft.Divider(height=1, color=ft.Colors.PURPLE_200),
        ft.Container(height=10),
        seccion_activa
    ], expand=True)

    # =========================================================================
    # 4. RETORNO DE LA ESTRUCTURA GLOBAL DE LA VISTA
    # =========================================================================
    return ft.View(
        route="/login",
        bgcolor=ft.Colors.BLUE_GREY_50,
        appbar=ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=volver_al_dashboard),
            title=ft.Text("Control de Asistencia Daily", weight=ft.FontWeight.W_500, size=20),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(icon=ft.Icons.REFRESH, icon_color=ft.Colors.WHITE, tooltip="Recargar Lista", on_click=actualizar_lista),
                ft.Container(width=10)
            ]
        ),
        controls=[
            ft.Container(
                content=contenedor_pestanas,
                padding=20,
                expand=True
            )
        ]
    )