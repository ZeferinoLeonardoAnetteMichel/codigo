import flet as ft
import cv2

def DashboardView(page: ft.Page, auth_controller=None):
    nombre_usuario = "Usuario"
    apellido_usuario = ""
    nombre_completo = "Usuario Invitado"
    matricula_usuario = "S/M"
    correo_usuario = "Sin correo"
    
    # Lógica para obtener los datos
    if auth_controller is None:
        auth_controller = getattr(page, "auth_ctrl", None)
        
    user_data = getattr(page, "user_data", {}) or {}
    
    # Si existen los datos, los sobrescribimos
    if user_data:
        nombre_usuario = user_data.get("nombre", "Usuario")
        apellido_usuario = user_data.get("apellido", "")
        nombre_completo = f"{nombre_usuario} {apellido_usuario}".strip()
        correo_usuario = user_data.get("correo", "Sin correo registrado")
        matricula_usuario = user_data.get("matricula", "S/M")
        

    def cerrar_sesion(e):
        page.user_data = None
        page.user_role = None
        page.go("/")

    def encender_camara_qr(e):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            return

        detector = cv2.QRCodeDetector()
        codigo_encontrado = None
        exito = False
        mensaje = ""
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            datos, puntos, _ = detector.detectAndDecode(frame)
            if datos:
                codigo_encontrado = datos
                partes = datos.split("-")
                id_maestro = int(partes[1])
                grupo = partes[2]
                exito, mensaje = auth_controller.registrar_asistencia_qr(
        matricula_usuario,
        id_maestro,
        grupo
    )
                
                cv2.putText(frame, "PROCESANDO...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("ScanClass", frame)
                cv2.waitKey(1000)
                break # Salimos del bucle al encontrar y procesar el QR
            
            cv2.imshow("ScanClass", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        
        # Notificación única después de procesar
        if codigo_encontrado:
            snack = ft.SnackBar(
                content=ft.Text(f"Resultado: {mensaje}", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.GREEN_600 if exito else ft.Colors.ORANGE_700
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
        

    # --- DISEÑO MANTENIDO TAL CUAL ---
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
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=encender_camara_qr
    )

    return ft.View(
        route="/dashboard",
        bgcolor=ft.Colors.GREY_100, 
        appbar=ft.AppBar(
            title=ft.Text("ScanClass - Panel Alumno", weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.INDIGO_600,
            color=ft.Colors.WHITE,
            automatically_imply_leading=False,
            actions=[
                ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, on_click=cerrar_sesion),
                ft.Container(width=10)
            ]
        ),
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=550, 
                                height=page.height - 140 if page.height else 650, 
                                bgcolor=ft.Colors.WHITE,
                                border_radius=20,
                                padding=35,
                                shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=ft.Colors.BLACK12, offset=ft.Offset(0, 5)),
                                content=ft.ListView(
                                    controls=[
                                        ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            tight=True,
                                            spacing=15,
                                            controls=[
                                                ft.Icon(ft.Icons.SCHOOL, size=60, color=ft.Colors.INDIGO_600),
                                                ft.Text(f"¡Bienvenido, {nombre_usuario}!", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                                ft.Text("Sistema SIGE - ScanClass", color=ft.Colors.GREY_600, size=14),
                                                ft.Divider(height=10),
                                                ft.Container(height=5),
                                                tarjeta_info,
                                                ft.Container(height=10),
                                                ft.Text("Presiona el botón para abrir la cámara y escanear el QR de la clase.", size=13, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                                                ft.Container(height=5),
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