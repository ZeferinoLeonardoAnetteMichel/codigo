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
    # 2. AHORA SÍ COLOCAMOS TU FUNCIÓN (Ya que puede "ver" las variables de arriba)
    # =========================================================================
    def actualizar_lista(e):
        # NOTA: Cuando conectes tu base de datos, aquí llamarías a tu controlador:
        # nonlocal alumnos_presentes, alumnos_ausentes
        # alumnos_presentes = auth_controller.obtener_asistencias_db()
        # alumnos_ausentes = auth_controller.obtener_ausencias_db()

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
        
        # Actualizamos la pantalla completa una sola vez al final
        page.update()

    # =========================================================================
    # 3. PESTAÑAS (Tabs) DE NAVEGACIÓN
    # =========================================================================
    contenedor_pestanas = ft.Tabs(
        selected_index=0,
        animation_duration=250,
        indicator_color=ft.Colors.PURPLE_600,
        label_color=ft.Colors.PURPLE_800,
        unselected_label_color=ft.Colors.BLUE_GREY_400,
        tabs=[
            ft.Tab(
                text="Presentes",
                icon=ft.Icons.PERSON_PIN_ROUNDED,
                content=ft.ListView([
                    ft.Container(height=10),
                    ft.Text("Alumnos que escanearon el QR exitosamente hoy:", size=14, color=ft.Colors.BLUE_GREY_600, italic=True),
                    ft.Container(height=10),
                    ft.Container(content=tabla_presentes, bgcolor=ft.Colors.WHITE, padding=10, border_radius=10)
                ], spacing=10, expand=True)
            ),
            ft.Tab(
                text="Ausentes",
                icon=ft.Icons.PERSON_OFF_ROUNDED,
                content=ft.ListView([
                    ft.Container(height=10),
                    ft.Text("Alumnos pendientes de registrar asistencia:", size=14, color=ft.Colors.BLUE_GREY_600, italic=True),
                    ft.Container(height=10),
                    ft.Container(content=tabla_ausentes, bgcolor=ft.Colors.WHITE, padding=10, border_radius=10)
                ], spacing=10, expand=True)
            )
        ],
        expand=True
    )

    # =========================================================================
    # 4. RETORNO DE LA ESTRUCTURA GLOBAL DE LA VISTA
    # =========================================================================
    return ft.View(
        route="/asistencia",
        bgcolor=ft.Colors.BLUE_GREY_50,
        appbar=ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=volver_al_dashboard),
            title=ft.Text("Control de Asistencia Daily", weight=ft.FontWeight.W_500, size=20),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            actions=[
                # Aquí vinculamos tu función al botón físico de refresh
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