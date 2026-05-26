import flet as ft
import cv2

def DashboardView(page: ft.Page, auth_controller=None):
    
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
            content=ft.Text("Cámara abierta. Muestra tu código QR..."),
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

        # ... (Todo tu bucle While de OpenCV se queda exactamente igual) ...

        # Liberación obligatoria de recursos de la cámara tras salir del bucle
        cap.release()
        cv2.destroyAllWindows()

        # =========================================================================
        # NUEVA LÓGICA: PROCESAR EL QR CON EL CONTROLADOR
        # =========================================================================
        if codigo_detectado:
            # Limpiamos el texto por si tiene espacios vacíos accidentales
            matricula_escaneada = codigo_detectado.strip()
            
            # Llamamos al método que creamos en el Paso 1
            exito_registro, mensaje_bd = auth_controller.registrar_asistencia_qr(matricula_escaneada)
            
            if exito_registro:
                snack_exito = ft.SnackBar(
                    content=ft.Text(f"¡Genial!: {mensaje_bd} (Matrícula: {matricula_escaneada})"),
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
            # Caso en que cerraron la cámara con la tecla 'q' sin escanear nada
            snack_cancelado = ft.SnackBar(
                content=ft.Text("Escaneo cancelado. No se detectó ningún código."),
                bgcolor=ft.Colors.RED_600
            )
            page.overlay.append(snack_cancelado)
            snack_cancelado.open = True

        page.update()

    # =========================================================================
    # EXTRAER INFORMACIÓN REAL DE LA SESIÓN (Mapeo dinámico)
    # =========================================================================
    # Recuperamos el diccionario que guardaste en LoginView. Si por alguna razón
    # viene vacío, ponemos un diccionario por defecto para que no rompa la app.
    user_info = getattr(page, "user_data", {}) or {}
    
    # Extraemos los campos (Ajusta los nombres dentro de .get() según tus columnas de la BD)
    # Por ejemplo, si en tu BD se llama 'name' en lugar de 'nombre', cámbialo aquí.
    nombre_usuario = user_info.get("nombre", "Usuario")
    apellido_usuario = user_info.get("apellido", "")
    nombre_completo = f"{nombre_usuario} {apellido_usuario}".strip()
    
    correo_usuario = user_info.get("correo", "Sin correo registrado")
    matricula_usuario = user_info.get("matricula", "S/M")

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
            
            # Aquí inyectamos las variables dinámicas que acabamos de extraer
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
            ft.Text("Presiona el botón para abrir la cámara de tu dispositivo.", size=12, color=ft.Colors.BLUE_GREY_500, text_align=ft.TextAlign.CENTER),
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