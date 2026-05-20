import flet as ft

def LoginView(page: ft.Page, auth_controller):

    # --- Funciones de utilidad ---
    def rellenar_campos(datos):
        identificador.value = datos.get("email", datos.get("matricula", ""))
        contraseña.focus()
        page.update()
        
    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN_600):
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=2500,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # --- Función dinámica para cambiar entre Correo y Matrícula ---
    def cambiar_identificador_rol(e):
        rol_actual = list(selector_rol.selected)[0]
        if rol_actual == "alumno":
            identificador.label = "Matrícula"
            identificador.prefix_icon = ft.Icons.CARD_MEMBERSHIP_OUTLINED
            identificador.keyboard_type = ft.KeyboardType.TEXT
        else:
            identificador.label = "Correo electrónico"
            identificador.prefix_icon = ft.Icons.MAIL_OUTLINE
            identificador.keyboard_type = ft.KeyboardType.EMAIL
        identificador.value = ""  # Limpiamos el campo al cambiar de rol para evitar confusiones
        mensaje.value = ""
        page.update()

    # --- Componentes del Modal de Recuperación ---
    correo_recuperacion = ft.TextField(
        label="Correo electrónico de recuperación",
        width=350,
        autofocus=True,
        border_radius=8,
        border_color=ft.Colors.PURPLE_400
    )
    codigo_verificacion = ft.TextField(
        label="Código de verificación recibido",
        width=350,
        visible=False,
        border_radius=8,
        border_color=ft.Colors.PURPLE_400
    )
    nueva_password = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        visible=False,
        border_radius=8,
        border_color=ft.Colors.PURPLE_400
    )
    confirmar_password = ft.TextField(
        label="Confirmar nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        visible=False,
        border_radius=8,
        border_color=ft.Colors.PURPLE_400
    )
    msg_dialogo = ft.Text("", color=ft.Colors.RED_600, weight=ft.FontWeight.W_500)

    def ejecutar_recuperacion(e):
        try:
            if not codigo_verificacion.visible and not nueva_password.visible:
                correo_ingresado = correo_recuperacion.value.strip()
                if correo_ingresado == "":
                    msg_dialogo.value = "Por favor, escribe tu correo."
                    msg_dialogo.color = ft.Colors.RED_600
                    page.update()
                    return
                exito, resultado = auth_controller.enviar_correo_recuperacion(correo_ingresado)
                if exito:
                    correo_recuperacion.visible = False
                    codigo_verificacion.visible = True
                    btn_enviar.text = "Verificar código"
                    msg_dialogo.value = "Código enviado. Revisa tu correo."
                    msg_dialogo.color = ft.Colors.GREEN_600
                    page.update()
                else:
                    msg_dialogo.value = resultado
                    msg_dialogo.color = ft.Colors.RED_600
                    page.update()

            elif codigo_verificacion.visible:
                codigo_ingresado = codigo_verificacion.value.strip()
                if codigo_ingresado == "":
                    msg_dialogo.value = "Ingresa el código."
                    msg_dialogo.color = ft.Colors.RED_600
                    page.update()
                    return
                verificado, mensaje_codigo = auth_controller.verificar_codigo_recuperacion(
                    correo_recuperacion.value, codigo_ingresado
                )
                if verificado:
                    codigo_verificacion.visible = False
                    nueva_password.visible = True
                    confirmar_password.visible = True
                    btn_enviar.text = "Cambiar contraseña"
                    msg_dialogo.value = "Código correcto. Ingresa tu nueva contraseña."
                    msg_dialogo.color = ft.Colors.GREEN_600
                    page.update()
                else:
                    msg_dialogo.value = mensaje_codigo
                    msg_dialogo.color = ft.Colors.RED_600
                    page.update()

            elif nueva_password.visible:
                nueva = nueva_password.value.strip()
                confirmar = confirmar_password.value.strip()
                if nueva == "" or confirmar == "":
                    msg_dialogo.value = "Completa todos los campos."
                    msg_dialogo.color = ft.Colors.RED_600
                    page.update()
                    return
                if nueva != confirmar:
                    msg_dialogo.value = "Las contraseñas no coinciden."
                    msg_dialogo.color = ft.Colors.RED_600
                    page.update()
                    return
                exito = auth_controller.cambiar_password(correo_recuperacion.value, nueva)
                if exito:
                    dialogo_olvido.open = False
                    page.update()
                    mostrar_snackbar("Contraseña actualizada correctamente", ft.Colors.GREEN_600)
                else:
                    msg_dialogo.value = "No se pudo actualizar la contraseña."
                    msg_dialogo.color = ft.Colors.RED_600
                    page.update()
        except Exception as ex:
            print("ERROR TOTAL EN MODAL:", ex)

    def cerrar_dialogo(e):
        dialogo_olvido.open = False
        page.update()

    btn_enviar = ft.ElevatedButton(
        "Enviar código",
        on_click=ejecutar_recuperacion,
        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)
    )
    
    dialogo_olvido = ft.AlertDialog(
        modal=True,
        title=ft.Text("Recuperar Contraseña", weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                ft.Text("Sigue las instrucciones en pantalla:", color=ft.Colors.BLUE_GREY_700),
                correo_recuperacion,
                codigo_verificacion,
                nueva_password,
                confirmar_password,
                msg_dialogo
            ],
            tight=True,
            spacing=15
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo, style=ft.ButtonStyle(color=ft.Colors.BLUE_GREY_400)),
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

    # --- Componentes Principales de la Vista de Login ---
    
    selector_rol = ft.SegmentedButton(
        selected=["alumno"],  
        segments=[
            ft.Segment(value="alumno", label=ft.Text("Alumno"), icon=ft.Icon(ft.Icons.SCHOOL)),
            ft.Segment(value="maestro", label=ft.Text("Maestro/Docente"), icon=ft.Icon(ft.Icons.SUPERVISED_USER_CIRCLE)),
        ],
        show_selected_icon=False,
        on_change=cambiar_identificador_rol  # Ejecuta la mutación visual cuando cambian de pestaña
    )

    # Renombrado a identificador ya que alojará tanto la Matrícula como el Correo dinámicamente
    identificador = ft.TextField(
        label="Matrícula",  # Por defecto inicia como alumno
        prefix_icon=ft.Icons.CARD_MEMBERSHIP_OUTLINED,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700,
        keyboard_type=ft.KeyboardType.TEXT
    )
    
    contraseña = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )
    
    mensaje = ft.Text("", color=ft.Colors.RED_600, weight=ft.FontWeight.W_500, size=13)

    def login_click(e):
        if not identificador.value or not contraseña.value:
            mensaje.value = "Por favor, llene todos los campos."
            page.update()
            return
            
        rol_seleccionado = list(selector_rol.selected)[0]
        val_identificador = identificador.value.strip()
        
        print(f"Iniciando sesión como: {rol_seleccionado} | Credencial: {val_identificador}")
        
        # Enviamos de forma adaptada la credencial (ya sea correo o matrícula) al auth_controller
        user, msg = auth_controller.login(val_identificador, contraseña.value, page, rol=rol_seleccionado)
        
        if user:
            page.user_data = user
            page.user_role = rol_seleccionado
            mostrar_snackbar("¡Sesión iniciada correctamente!", ft.Colors.GREEN_600)
            page.go("/dashboard")
        else:
            mensaje.value = msg
            page.update()

    iniciar_sesion = ft.ElevatedButton(
        "Iniciar Sesión",
        width=380,
        height=50,
        on_click=login_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    btn_registro = ft.TextButton(
        "¿No tienes cuenta? Regístrate aquí",
        style=ft.ButtonStyle(color=ft.Colors.PURPLE_700),
        on_click=lambda _: page.go("/register")
    )
    
    btn_olvido_password = ft.TextButton(
        "¿Olvidaste tu contraseña?",
        style=ft.ButtonStyle(color=ft.Colors.BLUE_GREY_500),
        on_click=abrir_modal_olvido
    )
    
    contraseña.on_submit = login_click
    identificador.on_submit = login_click

    # Tarjeta Contenedora Principal
    tarjeta_login = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.LOCK_PERSON_OUTLINED, size=50, color=ft.Colors.PURPLE_600),
                ft.Text("Acceso al Sistema", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
                ft.Text("Por favor, selecciona tu perfil e introduce tus credenciales", size=13, color=ft.Colors.BLUE_GREY_400, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                
                selector_rol,
                ft.Container(height=10),
                
                identificador, # Campo unificado adaptable
                contraseña,
                mensaje,
                ft.Container(height=5),
                iniciar_sesion,
                ft.Divider(height=30, color=ft.Colors.BLUE_GREY_100),
                ft.Column(
                    [
                        btn_olvido_password,
                        btn_registro
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            tight=True
        ),
        bgcolor=ft.Colors.WHITE,
        padding=40,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 8)
        ),
        width=450
    )

    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_50, 
        appbar=ft.AppBar(
            title=ft.Text("ScanClass", weight=ft.FontWeight.W_500, size=20),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            elevation=2
        ),
        controls=[
            ft.Container(content=tarjeta_login, padding=ft.Padding(0, 10, 0, 10))
        ]
    )