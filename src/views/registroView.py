import flet as ft
import re
import time 

def RegisterView(page: ft.Page, auth_controller):
    CLAVE_SECRET_DOCENTE = "CETIS_DOCENTEs_2026"

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
        matricula.value = ""
        grado.value = ""
        grupo.value = ""
        codigo_token.value = ""
        
        if rol_actual == "alumno":
            campos_alumno.visible = True
            campo_seguridad_maestro.visible = False
        else:
            campos_alumno.visible = False
            campo_seguridad_maestro.visible = True
        mensaje.value = ""
        page.update()

    # --- Componentes ---
    selector_rol = ft.SegmentedButton(
        selected=["alumno"],
        segments=[
            ft.Segment(value="alumno", label=ft.Text("Alumno")),
            ft.Segment(value="maestro", label=ft.Text("Maestro/Docente")),
        ],
        show_selected_icon=False,
        on_change=cambiar_rol,
    ) 
    
    nombre = ft.TextField(label="Nombre(s)", prefix_icon="person", border_radius=10)
    apellido_paterno = ft.TextField(label="Apellido Paterno", prefix_icon="person_outline", border_radius=10)
    apellido_materno = ft.TextField(label="Apellido Materno (Opcional)", prefix_icon="person_outline", border_radius=10)
    matricula = ft.TextField(label="Matrícula", prefix_icon="numbers", border_radius=10)
    grado = ft.TextField(label="Grado (ej: 6)")
    grupo = ft.TextField(label="Grupo (ej: D)")
    email = ft.TextField(label="Correo electrónico", prefix_icon="email", border_radius=10)
    password = ft.TextField(label="Contraseña", prefix_icon="lock", password=True, can_reveal_password=True, border_radius=10)
    confirm_password = ft.TextField(label="Confirmar contraseña", prefix_icon="lock_outline", password=True, can_reveal_password=True, border_radius=10)
    codigo_token = ft.TextField(label="Código de Seguridad Docente", prefix_icon="security", password=True, can_reveal_password=True, border_radius=10)
    
    mensaje = ft.Text("", color=ft.Colors.RED_ACCENT_400, size=12)
    campos_alumno = ft.Column([matricula, grado, grupo], visible=True, spacing=10)
    campo_seguridad_maestro = ft.Column([codigo_token], visible=False, spacing=10)

    def registrar_click(e):
        rol_actual = list(selector_rol.selected)[0]
        if not nombre.value or not apellido_paterno.value or not email.value or not password.value:
            mensaje.value = "Por favor, llena todos los campos obligatorios."
            page.update()
            return
        if rol_actual == "alumno" and not matricula.value.strip():
            mensaje.value = "La matrícula es obligatoria para alumnos."
            page.update()
            return
        if rol_actual == "maestro" and codigo_token.value.strip() != CLAVE_SECRET_DOCENTE:
            mensaje.value = "Código docente inválido."
            page.update()
            return
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden."
            page.update()
            return

        matricula_envio = matricula.value.strip() if rol_actual == "alumno" else f"DOC_{int(time.time())}"
        
        exito, msg = auth_controller.registrar(
            rol=rol_actual,
            matricula=matricula_envio,
            nombre=nombre.value.strip(),
            apellido_paterno=apellido_paterno.value.strip(),
            apellido_materno=apellido_materno.value.strip(),
            correo=email.value.strip(),
            password=password.value,
            grupo=grupo.value.strip().upper() if rol_actual == "alumno" else "N/A",
            grado=grado.value.strip() if rol_actual == "alumno" else "0"
        )
        
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión")
            page.go("/")
        else:
            mensaje.value = msg
            page.update()

    btn_registrar = ft.ElevatedButton("Registrarse", width=300, height=50, bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE, on_click=registrar_click)
    btn_login = ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=ir_login)

    return ft.View(
        route="/register",
        bgcolor=ft.Colors.GREY_100,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                ft.Container(
                    width=550,
                    height=650, # Altura fija para activar el scroll
                    bgcolor=ft.Colors.WHITE,
                    border_radius=20,
                    padding=35,
                    border=ft.Border(
                        left=ft.BorderSide(1, ft.Colors.GREY_200),
                        top=ft.BorderSide(1, ft.Colors.GREY_200),
                        right=ft.BorderSide(1, ft.Colors.GREY_200),
                        bottom=ft.BorderSide(1, ft.Colors.GREY_200),
                    ),
                    content=ft.ListView(
                        expand=True,
                        spacing=15,
                        controls=[
                            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, controls=[
                                ft.Icon(ft.Icons.SCHOOL, size=60, color=ft.Colors.INDIGO_600),
                                ft.Text("Crear Cuenta", size=28, weight=ft.FontWeight.BOLD),
                                selector_rol,
                                nombre, apellido_paterno, apellido_materno,
                                campos_alumno,
                                campo_seguridad_maestro,
                                email, password, confirm_password,
                                mensaje,
                                btn_registrar,
                                btn_login
                            ])
                        ]
                    )
                )
            ])
        ]
    )