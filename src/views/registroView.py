import flet as ft
import re

def RegisterView(page: ft.Page, auth_controller):

    CLAVE_SECRET_DOCENTE = "SIGE_DOCENTE_2026"

    # --- FUNCIONES AUXILIARES DE INTERFAZ ---
    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN_600):
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=2500,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def ir_login(e):
        page.go("/")

    def cambiar_rol(e):
        rol_actual = list(selector_rol.selected)[0]

        if rol_actual == "alumno":
            campos_alumno.visible = True
            campo_seguridad_maestro.visible = False
        else:
            campos_alumno.visible = False
            campo_seguridad_maestro.visible = True

        mensaje.value = ""
        page.update()

    # --- COMPONENTES PRINCIPALES DEL FORMULARIO ---
    
    selector_rol = ft.SegmentedButton(
        selected=["alumno"],
        segments=[
            ft.Segment(value="alumno", label=ft.Text("Alumno")),
            ft.Segment(value="maestro", label=ft.Text("Maestro/Docente")),
        ],
        show_selected_icon=False,
        on_change=cambiar_rol,
    )
    
    nombre = ft.TextField(
        label="Nombre(s)",
        prefix_icon="person",
        border_radius=10,
    )

    apellido_paterno = ft.TextField(
        label="Apellido Paterno",
        prefix_icon="person_outline",
        border_radius=10,
    )

    apellido_materno = ft.TextField(
        label="Apellido Materno (Opcional)",
        prefix_icon="person_outline",
        border_radius=10,
    )

    matricula = ft.TextField(
        label="Matrícula",
        prefix_icon="numbers",
        border_radius=10,
    )

    email = ft.TextField(
        label="Correo electrónico",
        prefix_icon="email",
        border_radius=10,
    )

    password = ft.TextField(
        label="Contraseña",
        prefix_icon="lock",
        password=True,
        can_reveal_password=True,
        border_radius=10,
    )

    confirm_password = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon="lock_outline",
        password=True,
        can_reveal_password=True,
        border_radius=10,
    )

    codigo_token = ft.TextField(
        label="Código de Seguridad Docente",
        prefix_icon="security",
        password=True,
        can_reveal_password=True,
        border_radius=10,
    )

    mensaje = ft.Text("", color=ft.Colors.RED_ACCENT_400, size=12)

    # --- CONTENEDORES DINÁMICOS SEGÚN EL ROL ---
    campos_alumno = ft.Column([matricula], visible=True, spacing=10)
    campo_seguridad_maestro = ft.Column([codigo_token], visible=False, spacing=10)

    # --- MANEJADOR DEL EVENTO CLICK REGISTRAR ---
    def registrar_click(e):
        rol_actual = list(selector_rol.selected)[0]

        if not nombre.value or not apellido_paterno.value or not email.value or not password.value or not confirm_password.value:
            mensaje.value = "Por favor, llena todos los campos obligatorios."
            page.update()
            return
        
        if rol_actual == "alumno" and not matricula.value:
            mensaje.value = "La matrícula es obligatoria para alumnos."
            page.update()
            return

        if rol_actual == "maestro":
            if not codigo_token.value:
                mensaje.value = "Introduce el código de autorización docente."
                page.update()
                return
            if codigo_token.value.strip() != CLAVE_SECRET_DOCENTE:
                mensaje.value = "Código docente inválido. No tienes autorización."
                page.update()
                return
        
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden."
            page.update()
            return
        
        if len(password.value) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres."
            page.update()
            return
        
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.value):
            mensaje.value = "Correo electrónico inválido."
            page.update()
            return

        matricula_envio = matricula.value.strip() if rol_actual == "alumno" else "DOCENTE"

        exito, msg = auth_controller.registrar(
            matricula=matricula_envio,
            nombre=nombre.value.strip(),
            correo=email.value.strip(),
            password=password.value
        )
        
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión")
            nombre.value = ""
            apellido_paterno.value = ""
            apellido_materno.value = ""
            matricula.value = ""
            codigo_token.value = ""
            email.value = ""
            password.value = ""
            confirm_password.value = ""
            mensaje.value = ""
            page.update()
            page.go("/")
        else:
            mensaje.value = msg or "Error al registrar usuario."
            page.update()
            
    # --- BOTONES DE ACCIÓN ---
    btn_registrar = ft.ElevatedButton(
        "Registrarse",
        width=300,
        height=50,
        bgcolor=ft.Colors.INDIGO_600,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=registrar_click,
    )
    
    btn_login = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión",
        on_click=ir_login,
    )
    
    # --- RETORNO DE LA VISTA COMPATIBLE ---
    return ft.View(
        route="/register",
        bgcolor=ft.Colors.GREY_100,
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
                                width=550,
                                height=page.height - 80 if page.height else 700, # Evita que se salga arriba y abajo
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
                                                    "Crear Cuenta",
                                                    size=28,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    "Sistema SIGE - ScanClass",
                                                    color=ft.Colors.GREY_600,
                                                    size=14,
                                                ),
                                                ft.Divider(height=10),
                                                selector_rol,
                                                ft.Container(height=5),
                                                nombre,
                                                apellido_paterno,
                                                apellido_materno,
                                                campos_alumno,
                                                campo_seguridad_maestro,
                                                email,
                                                password,
                                                confirm_password,
                                                mensaje,
                                                ft.Container(height=5),
                                                btn_registrar,
                                                btn_login
                                            ]
                                        )
                                    ],
                                    expand=True
                                )
                            )
                        ]
                    )
                ],
                expand=True # Ocupa todo el espacio para poder calcular el centro exacto
            )
        ],
    )