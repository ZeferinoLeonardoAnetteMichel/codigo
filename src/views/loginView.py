
import flet as ft

def LoginView(page: ft.Page, auth_controller):

    def rellenar_campos(datos):
        correo.value = datos.get("correo", "")
        contraseña.focus()
        page.update()

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2500,
        )

        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    correo_recuperacion = ft.TextField(
        label="Introduce tu correo electrónico",
        width=350,
        autofocus=True
    )

    codigo_verificacion = ft.TextField(
        label="Introduce el código recibido",
        width=350,
        visible=False
    )

    nueva_password = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        visible=False
    )

    confirmar_password = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        visible=False
    )

    msg_dialogo = ft.Text(
        "",
        color="red"
    )

    def ejecutar_recuperacion(e):

        try:

            print("CLICK DETECTADO EN RECUPERACIÓN")

            if (
                not codigo_verificacion.visible
                and not nueva_password.visible
            ):

                correo_ingresado = (
                    correo_recuperacion.value.strip()
                )

                if correo_ingresado == "":

                    msg_dialogo.value = (
                        "Por favor, escribe tu correo."
                    )

                    msg_dialogo.color = "red"

                    page.update()

                    return

                exito, resultado = (
                    auth_controller.enviar_correo_recuperacion(
                        correo_ingresado
                    )
                )

                if exito:

                    correo_recuperacion.visible = False

                    codigo_verificacion.visible = True

                    btn_enviar.text = "Verificar código"

                    msg_dialogo.value = (
                        "Código enviado. Revisa tu correo."
                    )

                    msg_dialogo.color = "green"

                    page.update()

                else:

                    msg_dialogo.value = resultado
                    msg_dialogo.color = "red"

                    page.update()

            elif codigo_verificacion.visible:

                codigo_ingresado = (
                    codigo_verificacion.value.strip()
                )

                if codigo_ingresado == "":

                    msg_dialogo.value = "Ingresa el código."
                    msg_dialogo.color = "red"

                    page.update()

                    return

                verificado, mensaje_codigo = (
                    auth_controller.verificar_codigo_recuperacion(
                        correo_recuperacion.value,
                        codigo_ingresado
                    )
                )

                if verificado:

                    codigo_verificacion.visible = False

                    nueva_password.visible = True
                    confirmar_password.visible = True

                    btn_enviar.text = "Cambiar contraseña"

                    msg_dialogo.value = (
                        "Código correcto. "
                        "Ingresa tu nueva contraseña."
                    )

                    msg_dialogo.color = "green"

                    page.update()

                else:

                    msg_dialogo.value = mensaje_codigo
                    msg_dialogo.color = "red"

                    page.update()

            elif nueva_password.visible:

                nueva = nueva_password.value.strip()

                confirmar = (
                    confirmar_password.value.strip()
                )

                if nueva == "" or confirmar == "":

                    msg_dialogo.value = (
                        "Completa todos los campos."
                    )
                    msg_dialogo.color = "red"
                    page.update()
                    return
                if nueva != confirmar:
                    msg_dialogo.value = (
                        "Las contraseñas no coinciden."
                    )
                    msg_dialogo.color = "red"
                    page.update()
                    return
                exito = auth_controller.cambiar_password(
                    correo_recuperacion.value,
                    nueva
                )
                if exito:
                    dialogo_olvido.open = False
                    page.update()
                    mostrar_snackbar(
                        "Contraseña actualizada correctamente",
                        ft.Colors.GREEN
                    )
                else:
                    msg_dialogo.value = (
                        "No se pudo actualizar la contraseña."
                    )
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
        title=ft.Text(
            "Recuperar Contraseña"
        ),
        content=ft.Column(
            [ft.Text("Sigue las instrucciones en pantalla:"),correo_recuperacion,codigo_verificacion,nueva_password,
                confirmar_password,msg_dialogo],tight=True,spacing=10),
        actions=[
            ft.TextButton("Cancelar",on_click=cerrar_dialogo),btn_enviar],
        actions_alignment=ft.MainAxisAlignment.END)

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
    correo = ft.TextField(label="Correo electrónico",prefix_icon=ft.Icons.PERSON,width=400,
        border_radius=10,border_color="purple",keyboard_type=ft.KeyboardType.EMAIL
    )
    contraseña = ft.TextField(label="Contraseña",prefix_icon=ft.Icons.KEY,password=True,can_reveal_password=True,
    width=400,border_radius=10,border_color="purple")
    mensaje = ft.Text("",color="red")

    def login_click(e):
        if not correo.value or not contraseña.value:
            mensaje.value = ("Por favor, llene todos los campos")
            mensaje.color = "red"
            page.update()
            return
        
        user, msg = auth_controller.login(correo.value, contraseña.value, page)
        
        if user:

            page.user_data = user

    # GUARDAR EL ROL
            page.user_role = "alumno"
            mostrar_snackbar(
                    "¡Sesión iniciada correctamente!",
                ft.Colors.GREEN
            )

            page.go("/dashboard")
        else:
            mensaje.value = msg
            mensaje.color = "red"
            page.update()
            return
        user, msg = auth_controller.login(correo.value,contraseña.value,page)
        if user:
            page.user_data = user
            mostrar_snackbar("¡Sesión iniciada correctamente!",ft.Colors.GREEN)
            page.go("/dashboard")
        else:
            mensaje.value = msg
            mensaje.color = "red"
            page.update()
    iniciar_sesion = ft.ElevatedButton(
        "Iniciar sesión",width=250,on_click=login_click,
        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_200,color=ft.Colors.WHITE,padding=20,shape=ft.RoundedRectangleBorder(radius=12
            ),
        ),
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
    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(title=ft.Text("SIGE - Login"),bgcolor=ft.Colors.PURPLE_200,color=ft.Colors.WHITE
        ),
        controls=[
            ft.Column(
                [
                    ft.Text("Acceso al Sistema",size=35,weight="bold",color="purple"
                    ),
                    ft.Container(height=10),
                    correo,
                    ft.Container(height=10),
                    contraseña,
                    ft.Container(height=10),
                    mensaje,
                    ft.Container(height=10),
                    ft.Row([iniciar_sesion],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(height=10),btn_olvido_password,btn_registro
                    ],horizontal_alignment=(ft.CrossAxisAlignment.CENTER),tight=True,spacing=10
            )
        ]
    )