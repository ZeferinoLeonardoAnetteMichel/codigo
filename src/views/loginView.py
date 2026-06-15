import flet as ft

def LoginView(page: ft.Page, auth_controller):
    # --- FUNCIONES DE LÓGICA ---
    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=2500,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # Variables de recuperación
    correo_recuperacion = ft.TextField(label="Introduce tu correo electrónico", prefix_icon="email", border_radius=10, autofocus=True)
    codigo_verificacion = ft.TextField(label="Introduce el código recibido", prefix_icon="numbers", border_radius=10, visible=False)
    nueva_password = ft.TextField(label="Nueva contraseña", prefix_icon="lock", password=True, can_reveal_password=True, border_radius=10, visible=False)
    confirmar_password = ft.TextField(label="Confirmar contraseña", prefix_icon="lock_outline", password=True, can_reveal_password=True, border_radius=10, visible=False)
    msg_dialogo = ft.Text("", color="red")

    def ejecutar_recuperacion(e):
        if not codigo_verificacion.visible and not nueva_password.visible:
            correo_ingresado = correo_recuperacion.value.strip()
            if correo_ingresado == "":
                msg_dialogo.value = "Por favor, escribe tu correo."
                msg_dialogo.color = "red"
                page.update()
                return
            exito, resultado = auth_controller.enviar_correo_recuperacion(correo_ingresado) if hasattr(auth_controller, "enviar_correo_recuperacion") else (True, "Código enviado")
            if exito:
                correo_recuperacion.visible = False
                codigo_verificacion.visible = True
                btn_enviar.text = "Verificar código"
                msg_dialogo.value = "Código enviado. Revisa tu correo."
                msg_dialogo.color = "green"
            else:
                msg_dialogo.value = resultado
                msg_dialogo.color = "red"
        elif codigo_verificacion.visible:
            verificado, mensaje_codigo = auth_controller.verificar_codigo_recuperacion(correo_recuperacion.value, codigo_verificacion.value.strip())
            if verificado:
                codigo_verificacion.visible = False
                nueva_password.visible = True
                confirmar_password.visible = True
                btn_enviar.text = "Cambiar contraseña"
                msg_dialogo.value = "Código correcto. Ingresa tu nueva contraseña."
                msg_dialogo.color = "green"
            else:
                msg_dialogo.value = mensaje_codigo
                msg_dialogo.color = "red"
        elif nueva_password.visible:
            if nueva_password.value != confirmar_password.value:
                msg_dialogo.value = "Las contraseñas no coinciden."
                msg_dialogo.color = "red"
            else:
                if auth_controller.cambiar_password(correo_recuperacion.value, nueva_password.value):
                    dialogo_olvido.open = False
                    mostrar_snackbar("Contraseña actualizada correctamente")
                else:
                    msg_dialogo.value = "Error al actualizar."
        page.update()

    btn_enviar = ft.ElevatedButton("Enviar código", on_click=ejecutar_recuperacion)
    dialogo_olvido = ft.AlertDialog(
        modal=True, title=ft.Text("Recuperar Contraseña"),
        content=ft.Column([correo_recuperacion, codigo_verificacion, nueva_password, confirmar_password, msg_dialogo], tight=True),
        actions=[ft.TextButton("Cancelar", on_click=lambda e: setattr(dialogo_olvido, "open", False) or page.update()), btn_enviar]
    )

    def abrir_modal_olvido(e):
        page.dialog = dialogo_olvido
        dialogo_olvido.open = True
        page.update()

    # --- CAMPOS DE LOGIN ---
    correo = ft.TextField(label="Correo electrónico", prefix_icon="person", border_radius=10, keyboard_type=ft.KeyboardType.EMAIL)
    contraseña = ft.TextField(label="Contraseña", prefix_icon="lock", password=True, can_reveal_password=True, border_radius=10)
    mensaje = ft.Text("", color=ft.Colors.RED_ACCENT_400, size=12)

    def login_click(e):
        user, msg = auth_controller.login(correo.value, contraseña.value, page)
        if user:
            print("USUARIO LOGUEADO:", user)
            page.user_data = user
            print("PAGE USER DATA:", page.user_data)
            page.id_usuario_actual = user.get("id_usuario")
            page.user_role = user.get("rol")
            page.go("/asistencia" if user.get("rol") == "maestro" else "/dashboard")
        else:
            mensaje.value = "Credenciales incorrectas"
            page.update()

    iniciar_sesion = ft.ElevatedButton("Iniciar sesión", width=300, height=50, bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE, on_click=login_click)

    return ft.View(
        route="/",
        bgcolor=ft.Colors.GREY_50,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=400,
                padding=40,
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                # Reemplaza la línea del error por esta:
                border=ft.Border(
                left=ft.BorderSide(1, ft.Colors.GREY_200),
                top=ft.BorderSide(1, ft.Colors.GREY_200),
                right=ft.BorderSide(1, ft.Colors.GREY_200),
                bottom=ft.BorderSide(1, ft.Colors.GREY_200),
),
                    content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                    controls=[
                        ft.Icon(ft.Icons.SCHOOL, size=60, color=ft.Colors.INDIGO_700),
                        ft.Text("Acceso al Sistema", size=24, weight="bold"),
                        ft.Text("Sistema SIGE - ScanClass", size=14, color=ft.Colors.GREY_600),
                        ft.Container(height=20),
                        correo,
                        contraseña,
                        mensaje,
                        ft.Container(height=10),
                        iniciar_sesion,
                        ft.TextButton("¿Olvidaste tu contraseña?", on_click=abrir_modal_olvido),
                        ft.TextButton("¿No tienes cuenta? Regístrate", on_click=lambda _: page.go("/register"))
                    ]
                )
            )
        ]
    )