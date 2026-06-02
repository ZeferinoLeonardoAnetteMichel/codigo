import flet as ft
import cv2

def DashboardView(page: ft.Page, auth_controller=None):
    
    # =========================================================================
    # RESPALDO: Si no llegó por parámetro, lo recuperamos directamente de la page
    # =========================================================================
    if auth_controller is None:
        auth_controller = getattr(page, "auth_ctrl", None)
    
    # =========================================================================
    # EXTRAER INFORMACIÓN REAL DE LA SESIÓN (Mapeo dinámico)
    # =========================================================================
    user_info = getattr(page, "user_data", {}) or {}
    
    nombre_usuario = user_info.get("nombre", "Usuario")
    apellido_usuario = user_info.get("apellido", "")
    nombre_completo = f"{nombre_usuario} {apellido_usuario}".strip()
    
    correo_usuario = user_info.get("correo", "Sin correo registrado")
    matricula_usuario = user_info.get("matricula", "S/M")

    # --- FUNCION: CERRAR SESIÓN ---
    def cerrar_sesion(e):
        page.user_data = None
        page.user_role = None
        page.go("/")

    # --- FUNCIÓN REAL DE ESCANEO DE QR ---
    def encender_camara_qr(e):
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        snack = ft.SnackBar(
            content=ft.Text("Cámara abierta. Muestra el código QR del salón...", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.INDIGO_600,
            duration=2500,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

        codigo_detectado = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            datos, puntos, _ = detector.detectAndDecode(frame)

            if datos:
                codigo_detectado = datos
                cv2.putText(
                    frame,
                    "¡QR Detectado!",
                    (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Escaneando Asistencia - ScanClass", frame)
            tecla = cv2.waitKey(1)

            if codigo_detectado:
                break
            if tecla == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        # =========================================================================
        # LÓGICA DE PROCESAMIENTO: OPCIÓN B (Registra al alumno de la sesión) 🚀
        # =========================================================================
        if codigo_detectado:
            if auth_controller is not None:
                exito_registro, mensaje_bd = auth_controller.registrar_asistencia_qr(matricula_usuario)
                
                if exito_registro:
                    snack_exito = ft.SnackBar(
                        content=ft.Text(f"¡Asistencia Registrada!: {mensaje_bd} (Matrícula: {matricula_usuario})", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.GREEN_600
                    )
                    page.overlay.append(snack_exito)
                    snack_exito.open = True
                else:
                    snack_error = ft.SnackBar(
                        content=ft.Text(f"Error: {mensaje_bd}", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.ORANGE_700
                    )
                    page.overlay.append(snack_error)
                    snack_error.open = True
            else:
                snack_error_interno = ft.SnackBar(
                    content=ft.Text("Error de sistema: No se pudo enlazar el controlador de asistencia.", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.RED_700
                )
                page.overlay.append(snack_error_interno)
                snack_error_interno.open = True
        else:
            snack_cancelado = ft.SnackBar(
                content=ft.Text("Escaneo cancelado. No se detectó ningún código.", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.RED_600
            )
            page.overlay.append(snack_cancelado)
            snack_cancelado.open = True

        page.update()

    # =========================================================================
    # COMPONENTES VISUALES REDISEÑADOS (IGUAL A REGISTERVIEW)
    # =========================================================================
    
    tarjeta_info = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, size=24, color=ft.Colors.INDIGO_600),
                ft.Text("Información de Usuario", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_600)
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            ft.Divider(height=10, color=ft.Colors.GREY_200),
            
            ft.Row([ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREY_600, size=20), ft.Text(nombre_completo, size=14, color=ft.Colors.GREY_800)]),
            ft.Row([ft.Icon(ft.Icons.CARD_MEMBERSHIP, color=ft.Colors.GREY_600, size=20), ft.Text(f"Matrícula: {matricula_usuario}", size=14, color=ft.Colors.GREY_800)]),
            ft.Row([ft.Icon(ft.Icons.EMAIL, color=ft.Colors.GREY_600, size=20), ft.Text(correo_usuario, size=14, color=ft.Colors.GREY_800)]),
        ], spacing=12),
        bgcolor=ft.Colors.GREY_50,
        padding=20,
        border_radius=10,
    )

    btn_escanear = ft.ElevatedButton(
        "Escanear QR",
        icon=ft.Icons.CAMERA_ALT,
        width=300,
        height=50,
        bgcolor=ft.Colors.INDIGO_600,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=encender_camara_qr
    )

    # =========================================================================
    # RETORNO DE LA VISTA EN CORRESPONDENCIA CON EL DISEÑO DE REGISTRO
    # =========================================================================
    return ft.View(
        route="/dashboard",
        bgcolor=ft.Colors.GREY_100, # Mismo color de fondo que RegisterView
        appbar=ft.AppBar(
            title=ft.Text("ScanClass - Panel Alumno", weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.INDIGO_600, # Navbar a juego con los botones del registro
            color=ft.Colors.WHITE,
            automatically_imply_leading=False,
            actions=[
                ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, on_click=cerrar_sesion),
                ft.Container(width=10)
            ]
        ),
        controls=[
            # Forzamos un Row centrado horizontalmente
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    # Forzamos una Column centrada verticalmente
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=550, # Mismo ancho que tu contenedor de registro
                                height=page.height - 140 if page.height else 650, # Ajuste para compensar el AppBar
                                bgcolor=ft.Colors.WHITE,
                                border_radius=20,
                                padding=35,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=20,
                                    color=ft.Colors.BLACK12,
                                    offset=ft.Offset(0, 5),
                                ),
                                content=ft.ListView(
                                    controls=[
                                        ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            tight=True,
                                            spacing=15,
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.SCHOOL,
                                                    size=60,
                                                    color=ft.Colors.INDIGO_600,
                                                ),
                                                ft.Text(
                                                    f"¡Bienvenido, {nombre_usuario}!",
                                                    size=26,
                                                    weight=ft.FontWeight.BOLD,
                                                    text_align=ft.TextAlign.CENTER
                                                ),
                                                ft.Text(
                                                    "Sistema SIGE - ScanClass",
                                                    color=ft.Colors.GREY_600,
                                                    size=14,
                                                ),
                                                ft.Divider(height=10),
                                                ft.Container(height=5),
                                                
                                                # Tarjeta con los datos de sesión reales
                                                tarjeta_info,
                                                
                                                ft.Container(height=10),
                                                
                                                # Texto descriptivo de la acción del QR
                                                ft.Text(
                                                    "Presiona el botón para abrir la cámara y escanear el QR de la clase.", 
                                                    size=13, 
                                                    color=ft.Colors.GREY_600, 
                                                    text_align=ft.TextAlign.CENTER
                                                ),
                                                
                                                ft.Container(height=5),
                                                
                                                # Botón idéntico al de Registro
                                                btn_escanear,
                                            ]
                                        )
                                    ],
                                    expand=True
                                )
                            )
                        ]
                    )
                ],
                expand=True 
            )
        ],
    )