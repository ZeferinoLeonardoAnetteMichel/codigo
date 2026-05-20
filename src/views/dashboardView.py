import flet as ft

def DashboardView(page: ft.Page, auth_controller):
    # Recuperamos los datos del usuario logueado
    usuario_actual = getattr(page, "user_data", {})
    rol_actual = getattr(page, "user_role", "alumno").lower()

    # --- FUNCIONES DE ACCIÓN ---
    def cerrar_sesion(e):
        page.user_data = None
        page.user_role = None
        page.go("/")

    def simular_escaneo_qr(e):
        snack = ft.SnackBar(
            content=ft.Text("Iniciando Cámara... Escaneando código QR de asistencia", weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.PURPLE_700
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()


    # =========================================================================
    # 1. INTERFAZ PARA EL ALUMNO (Información + Cámara de Escaneo)
    # =========================================================================
    def info_item_alumno(icono, titulo, valor):
        return ft.Row([
            ft.Icon(icono, color=ft.Colors.PURPLE_700, size=20),
            ft.Text(f"{titulo}: ", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLUE_GREY_700),
            ft.Text(valor, size=14, color=ft.Colors.BLUE_GREY_900)
        ], spacing=10)

    # Contenedor de la credencial digital del alumno
    tarjeta_info_alumno = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, size=40, color=ft.Colors.PURPLE_600),
                ft.Text("Información Escolar", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800)
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            ft.Divider(color=ft.Colors.PURPLE_300),
            info_item_alumno(ft.Icons.PERSON, "Nombre", usuario_actual.get("nombre", "Nombre Alumno")),
            info_item_alumno(ft.Icons.CARD_MEMBERSHIP, "Matrícula", usuario_actual.get("matricula", "N/A")),
            info_item_alumno(ft.Icons.LAYERS, "Grado y Grupo", f"{usuario_actual.get('grado', 'N/A')}° '{usuario_actual.get('grupo', 'N/A')}'"),
            info_item_alumno(ft.Icons.EMAIL, "Correo", usuario_actual.get("correo", "correo@alumno.com")),
        ], spacing=12),
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK))
    )

    # Contenedor simulador del área de la cámara / Escáner QR
    tarjeta_camara_alumno = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.QR_CODE_SCANNER, size=80, color=ft.Colors.PURPLE_600),
            ft.Text("Escanear Código de Asistencia", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
            ft.Text("Coloca el código QR generado por el profesor frente a la cámara para registrar tu entrada.", 
                    size=12, color=ft.Colors.BLUE_GREY_500, text_align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            ft.ElevatedButton(
                "Abrir Cámara / Escanear",
                icon=ft.Icons.CAMERA_ALT,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.PURPLE_600,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                width=250,
                height=45,
                on_click=simular_escaneo_qr
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK))
    )

    vista_alumno = ft.Column([
        ft.Text(f"¡Bienvenido de vuelta, {usuario_actual.get('nombre', 'Alumno')}!", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ft.Text("Usa este panel para verificar tus datos y registrar tu asistencia diaria.", size=14, color=ft.Colors.BLUE_GREY_500),
        ft.Container(height=15),
        ft.ResponsiveRow([
            ft.col({"md": 6, "xs": 12}, controls=[tarjeta_info_alumno]),
            ft.col({"md": 6, "xs": 12}, controls=[tarjeta_camara_alumno]),
        ], spacing=20)
    ], spacing=10, scroll=ft.ScrollMode.AUTO)


    # =========================================================================
    # 2. INTERFAZ PARA EL MAESTRO (Información + Listas de Asistencia)
    # =========================================================================
    
    # Datos simulados para las tablas
    alumnos_registrados = [
        {"nombre": "Carlos Mendoza Ortiz", "matricula": "2026001", "hora": "07:02 AM"},
        {"nombre": "Ana Valeria Gómez", "matricula": "2026042", "hora": "07:05 AM"},
        {"nombre": "Luis Fernando Perea", "matricula": "2026015", "hora": "07:11 AM"},
    ]
    
    alumnos_no_registrados = [
        {"nombre": "Diana Laura Martínez", "matricula": "2026089"},
        {"nombre": "Jorge Alberto Ríos", "matricula": "2026112"},
    ]

    tarjeta_info_maestro = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SUPERVISED_USER_CIRCLE, size=50, color=ft.Colors.WHITE),
            ft.Column([
                ft.Text(usuario_actual.get("nombre", "Profesor Titular"), size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(f"Docente Autorizado • {usuario_actual.get('correo', 'maestro@escuela.com')}", size=13, color=ft.Colors.PURPLE_100),
            ], spacing=2)
        ], alignment=ft.MainAxisAlignment.START, spacing=15),
        bgcolor=ft.Colors.PURPLE_600,
        padding=20,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
    )

    # Tabla de Alumnos Presentes
    tabla_registrados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Matrícula", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre Completo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Hora de Entrada", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estatus", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(al["matricula"])),
                ft.DataCell(ft.Text(al["nombre"])),
                ft.DataCell(ft.Text(al["hora"])),
                ft.DataCell(ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600, size=20)),
            ]) for al in alumnos_registrados
        ],
        heading_row_color=ft.Colors.PURPLE_50,
        border_radius=8
    )

    # Tabla de Alumnos Ausentes (Rojo para marcar inasistencia)
    tabla_no_registrados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Matrícula", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre Completo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estatus", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(al["matricula"])),
                ft.DataCell(ft.Text(al["nombre"])),
                ft.DataCell(ft.Row([
                    ft.Icon(ft.Icons.CANCEL, color=ft.Colors.RED_600, size=20),
                    ft.Text("Ausente", color=ft.Colors.RED_600, size=12, weight=ft.FontWeight.W_500)
                ], spacing=5)),
            ]) for al in alumnos_no_registrados
        ],
        heading_row_color=ft.Colors.PURPLE_50,
        border_radius=8
    )

    vista_maestro = ft.Column([
        tarjeta_info_maestro,
        ft.Container(height=15),
        
        # Pestañas con los colores del sistema asignados directamente
        ft.Tabs(
            selected_index=0,
            animation_duration=200,
            indicator_color=ft.Colors.PURPLE_600,
            label_color=ft.Colors.PURPLE_800,
            tabs=[
                ft.Tab(
                    text="Registrados / Presentes",
                    icon=ft.Icons.PERSON_PIN_ROUNDED,
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Alumnos que ya escanearon su código exitosamente:", size=14, color=ft.Colors.BLUE_GREY_600, italic=True),
                            ft.Container(content=tabla_registrados, margin=ft.margin.only(top=10))
                        ]),
                        padding=15
                    )
                ),
                ft.Tab(
                    text="No Registrados / Ausentes",
                    icon=ft.Icons.PERSON_OFF_ROUNDED,
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Alumnos pendientes de registrar asistencia hoy:", size=14, color=ft.Colors.BLUE_GREY_600, italic=True),
                            ft.Container(content=tabla_no_registrados, margin=ft.margin.only(top=10))
                        ]),
                        padding=15
                    )
                )
            ],
            expand=True
        )
    ], spacing=10, scroll=ft.ScrollMode.AUTO)


    # =========================================================================
    # RENDERIZADO FINAL CONDICIONAL
    # =========================================================================
    controles_pantalla = vista_maestro if rol_actual == "maestro" else vista_alumno

    return ft.View(
        route="/dashboard",
        bgcolor=ft.Colors.BLUE_GREY_50,
        appbar=ft.AppBar(
            title=ft.Text("ScanClass - Panel de Control", weight=ft.FontWeight.W_500, size=20),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            elevation=2,
            automatically_imply_leading=False,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT, 
                    icon_color=ft.Colors.WHITE, 
                    tooltip="Cerrar Sesión",
                    on_click=cerrar_sesion
                ),
                ft.Container(width=10)
            ]
        ),
        controls=[
            ft.Container(
                content=controles_pantalla,
                padding=30,
                expand=True
            )
        ]
    )