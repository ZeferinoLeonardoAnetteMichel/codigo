import flet as ft
import re

def LoginView(page: ft.Page, auth_controller):

    def rellenar_campos(datos):
        correo.value = datos.get("correo", "")
        contraseña.focus()
        page.update()

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=2500,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # =========================================================================
    # COMPONENTES DEL MODAL DE RECUPERACIÓN (Estilizados)
    # =========================================================================
    correo_recuperacion = ft.TextField(
        label="Introduce tu correo electrónico",
        prefix_icon="email",
        border_radius=10,
        autofocus=True
    )

    codigo_verificacion = ft.TextField(
        label="Introduce el código recibido",
        prefix_icon="numbers",
        border_radius=10,
        visible=False
    )

    nueva_password = ft.TextField(
        label="Nueva contraseña",
        prefix_icon="lock",
        password=True,
        can_reveal_password=True,
        border_radius=10,
        visible=False
    )

    confirmar_password = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon="lock_outline",
        password=True,
        can_reveal_password=True,
        border_radius=10,
        visible=False
    )

    msg_dialogo = ft.Text("", color="red")

    def ejecutar_recuperacion(e):
        try:
            print("CLICK DETECTADO EN RECUPERACIÓN")

            # FASE 1: Solicitar Código
            if not codigo_verificacion.visible and not nueva_password.visible:
                correo_ingresado = correo_recuperacion.value.strip()

                if correo_ingresado == "":
                    msg_dialogo.value = "Por favor, escribe tu correo."
                    msg_dialogo.color = "red"
                    page.update()
                    return

                exito, resultado = (True, "Código enviado") if not hasattr(auth_controller, "enviar_correo_recuperacion") else auth_controller.enviar_correo_recuperacion(correo_ingresado)

                if exito:
                    correo_recuperacion.visible = False
                    codigo_verificacion.visible = True
                    btn_enviar.text = "Verificar código"
                    msg_dialogo.value = "Código enviado. Revisa tu correo."
                    msg_dialogo.color = "green"
                    page.update()
                else:
                    msg_dialogo.value = resultado
                    msg_dialogo.color = "red"
                    page.update()

            # FASE 2: Verificar Código
            elif codigo_verificacion.visible:
                codigo_ingresado = codigo_verificacion.value.strip()

                if codigo_ingresado == "":
                    msg_dialogo.value = "Ingresa el código."
                    msg_dialogo.color = "red"
                    page.update()
                    return

                verificado, mensaje_codigo = auth_controller.verificar_codigo_recuperacion(
                    correo_recuperacion.value,
                    codigo_ingresado
                )

                if verificado:
                    codigo_verificacion.visible = False
                    nueva_password.visible = True
                    confirmar_password.visible = True
                    btn_enviar.text = "Cambiar contraseña"
                    msg_dialogo.value = "Código correcto. Ingresa tu nueva contraseña."
                    msg_dialogo.color = "green"
                    page.update()
                else:
                    msg_dialogo.value = mensaje_codigo
                    msg_dialogo.color = "red"
                    page.update()

            # FASE 3: Cambiar Contraseña
            elif nueva_password.visible:
                nueva = nueva_password.value.strip()
                confirmar = confirmar_password.value.strip()

                if nueva == "" or confirmar == "":
                    msg_dialogo.value = "Completa todos los campos."
                    msg_dialogo.color = "red"
                    page.update()
                    return

                if nueva != confirmar:
                    msg_dialogo.value = "Las contraseñas no coinciden."
                    msg_dialogo.color = "red"
                    page.update()
                    return

                exito = auth_controller.cambiar_password(correo_recuperacion.value, nueva)
                if exito:
                    dialogo_olvido.open = False
                    page.update()
                    mostrar_snackbar("Contraseña actualizada correctamente", ft.Colors.GREEN)
                else:
                    msg_dialogo.value = "No se pudo actualizar la contraseña."
                    msg_dialogo.color = "red"
                    page.update()

        except Exception as ex:
            print("ERROR TOTAL EN MODAL:", ex)

    def cerrar_dialogo(e):
        dialogo_olvido.open = False
        page.update()

    btn_enviar = ft.ElevatedButton(
        "Enviar código",
        on_click=ejecutar_recuperacion
    )

    dialogo_olvido = ft.AlertDialog(
        modal=True,
        title=ft.Text("Recuperar Contraseña"),
        content=ft.Column(
            [
                ft.Text("Sigue las instrucciones en pantalla:"),
                correo_recuperacion,
                codigo_verificacion,
                nueva_password,
                confirmar_password,
                msg_dialogo
            ],
            tight=True,
            spacing=10
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            btn_enviar
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal_olvido(e):
        correo_recuperacion.value = ""
        correo_recuperacion.visible = True
        codigo_verificacion.value = ""
        codigo_verificacion.visible = False
        nueva_password.value = ""
        nueva_password.visible = False
        confirmar_password.value = ""
        confirmar_password.visible = False
        btn_enviar.text = "Enviar código"
        msg_dialogo.value = ""
        
        if dialogo_olvido not in page.overlay:
            page.overlay.append(dialogo_olvido)
        page.dialog = dialogo_olvido
        dialogo_olvido.open = True
        page.update()

    # =========================================================================
    # CAMPOS DEL FORMULARIO PRINCIPAL
    # =========================================================================
    correo = ft.TextField(
        label="Correo electrónico",
        prefix_icon="person",
        border_radius=10,
        keyboard_type=ft.KeyboardType.EMAIL
    )
    
    contraseña = ft.TextField(
        label="Contraseña",
        prefix_icon="lock",
        password=True,
        can_reveal_password=True,
        border_radius=10,
    )
    
    mensaje = ft.Text("", color=ft.Colors.RED_ACCENT_400, size=12)

    # =========================================================================
    # LOGICA DE INICIO DE SESIÓN INTEGRADA
    # =========================================================================
    def login_click(e):
        if not correo.value or not contraseña.value:
            mensaje.value = "Por favor, llene todos los campos."
            page.update()
            return
        
        user, msg = auth_controller.login(correo.value, contraseña.value, page)
        
        if user:
            page.user_data = user
            mostrar_snackbar("¡Sesión iniciada correctamente!", ft.Colors.GREEN)

            if user.get("matricula") == "DOCENTE":
                page.user_role = "maestro"
                page.go("/asistencia")  
            else:
                page.user_role = "alumno"
                page.go("/dashboard")          
        else:
            text_error = msg if msg else "Credenciales incorrectas"
            mensaje.value = text_error
            page.update()

    iniciar_sesion = ft.ElevatedButton(
        "Iniciar sesión",
        width=300,
        height=50,
        bgcolor=ft.Colors.INDIGO_600,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=login_click,
    )

    btn_registro = ft.TextButton(
        "¿No tienes cuenta? Regístrate",
        on_click=lambda _: page.go("/register")
    )

    btn_olvido_password = ft.TextButton(
        "¿Olvidaste tu contraseña?",
        on_click=abrir_modal_olvido
    )

    contraseña.on_submit = login_click

    # =========================================================================
    # RETORNO DE LA VISTA CENTRADA E IGUAL AL REGISTRO
    # =========================================================================
    return ft.View(
        route="/",
        bgcolor=ft.Colors.GREY_100,
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
                                height=page.height - 80 if page.height else 600, # Altura adaptada para Login
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
                                                    "Acceso al Sistema",
                                                    size=28,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    "Sistema SIGE - ScanClass",
                                                    color=ft.Colors.GREY_600,
                                                    size=14,
                                                ),
                                                ft.Divider(height=10),
                                                ft.Container(height=5),
                                                correo,
                                                contraseña,
                                                mensaje,
                                                ft.Container(height=5),
                                                iniciar_sesion,
                                                btn_olvido_password,
                                                btn_registro
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