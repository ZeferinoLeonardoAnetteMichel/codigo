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
            content=ft.Text("Cámara abierta. Muestra el código QR del salón..."),
            bgcolor=ft.Colors.PURPLE_700
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

        # Liberación obligatoria de recursos de la cámara tras salir del bucle
        cap.release()
        cv2.destroyAllWindows()

        # =========================================================================
        # LÓGICA DE PROCESAMIENTO: OPCIÓN B (Registra al alumno de la sesión) 🚀
        # =========================================================================
        if codigo_detectado:
            # Verificamos que el controlador realmente exista y no sea None
            if auth_controller is not None:
                # INTEGRADO OPCIÓN B: Enviamos 'matricula_usuario' en vez del texto del QR
                exito_registro, mensaje_bd = auth_controller.registrar_asistencia_qr(matricula_usuario)
                
                if exito_registro:
                    snack_exito = ft.SnackBar(
                        content=ft.Text(f"¡Asistencia Registrada!: {mensaje_bd} (Matrícula: {matricula_usuario})"),
                        bgcolor=ft.Colors.GREEN_600
                    )
                    page.overlay.append(snack_exito)
                    snack_exito.open = True
                else:
                    snack_error = ft.SnackBar(
                        content=ft.Text(f"Error: {mensaje_bd}"),
                        bgcolor=ft.Colors.ORANGE_700
                    )
                    page.overlay.append(snack_error)
                    snack_error.open = True
            else:
                # Mensaje de error seguro si el controlador sigue sin aparecer
                snack_error_interno = ft.SnackBar(
                    content=ft.Text("Error de sistema: No se pudo enlazar el controlador de asistencia."),
                    bgcolor=ft.Colors.RED_700
                )
                page.overlay.append(snack_error_interno)
                snack_error_interno.open = True
        else:
            # Caso en que cerraron la cámara con la tecla 'q' sin escanear nada
            snack_cancelado = ft.SnackBar(
                content=ft.Text("Escaneo cancelado. No se detectó ningún código."),
                bgcolor=ft.Colors.RED_600
            )
            page.overlay.append(snack_cancelado)
            snack_cancelado.open = True

        page.update()

    # =========================================================================
    # COMPONENTES VISUALES CON DATOS REALES
    # =========================================================================
    tarjeta_info = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, size=40, color=ft.Colors.PURPLE_600),
                ft.Text("Información de Usuario", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800)
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            ft.Divider(color=ft.Colors.PURPLE_300),
            
            ft.Row([ft.Icon(ft.Icons.PERSON, color=ft.Colors.PURPLE_700), ft.Text(nombre_completo, size=14)]),
            ft.Row([ft.Icon(ft.Icons.CARD_MEMBERSHIP, color=ft.Colors.PURPLE_700), ft.Text(f"Matrícula: {matricula_usuario}", size=14)]),
            ft.Row([ft.Icon(ft.Icons.EMAIL, color=ft.Colors.PURPLE_700), ft.Text(correo_usuario, size=14)]),
        ], spacing=12),
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=12,
    )

    tarjeta_camara = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.QR_CODE_SCANNER, size=80, color=ft.Colors.PURPLE_600),
            ft.Text("Escanear Código de Asistencia", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
            ft.Text("Presiona el botón para abrir la cámara y escanear el QR de la clase.", size=12, color=ft.Colors.BLUE_GREY_500, text_align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            ft.ElevatedButton(
                "Escanear QR",
                icon=ft.Icons.CAMERA_ALT,
                style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE),
                on_click=encender_camara_qr
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=12,
    )

    diseño_pantalla = ft.ListView([
        ft.Text(f"¡Bienvenido, {nombre_usuario}!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ft.Container(height=10),
        tarjeta_info,
        ft.Container(height=15),
        tarjeta_camara
    ], spacing=10, expand=True)

    return ft.View(
        route="/dashboard",
        bgcolor=ft.Colors.BLUE_GREY_50,
        appbar=ft.AppBar(
            title=ft.Text("ScanClass - Panel Alumno"),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            automatically_imply_leading=False,
            actions=[
                ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, on_click=cerrar_sesion),
                ft.Container(width=10)
            ]
        ),
        controls=[diseño_pantalla]
    )