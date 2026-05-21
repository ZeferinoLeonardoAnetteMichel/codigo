import flet as ft
import re
from models.schemasModel import UsuarioSchema  

def RegisterView(page: ft.Page, auth_controller):
    
    CLAVE_SECRET_DOCENTE = "SIGE_DOCENTE_2026"

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN_600):
        snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=2500,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

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

    # --- Componentes Principales del Formulario ---
    
    selector_rol = ft.SegmentedButton(
        selected=["alumno"],  
        segments=[
            ft.Segment(value="alumno", label=ft.Text("Alumno"), icon=ft.Icon(ft.Icons.SCHOOL)),
            ft.Segment(value="maestro", label=ft.Text("Maestro/Docente"), icon=ft.Icon(ft.Icons.SUPERVISED_USER_CIRCLE)),
        ],
        show_selected_icon=False,
        on_change=cambiar_rol
    )
    
    nombre = ft.TextField(
        label="Nombre(s)",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )
    
    apellido_paterno = ft.TextField(
        label="Apellido Paterno",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )

    apellido_materno = ft.TextField(
        label="Apellido Materno (Opcional)",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )

    # --- Campos Exclusivos para Alumnos ---
    matricula = ft.TextField(
        label="Matrícula",
        prefix_icon=ft.Icons.CARD_MEMBERSHIP_OUTLINED,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )

    grado = ft.TextField(
        label="Grado",
        prefix_icon=ft.Icons.LAYERS_OUTLINED,
        width=180,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )

    grupo = ft.TextField(
        label="Grupo",
        prefix_icon=ft.Icons.GROUP_WORK_OUTLINED,
        width=180,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )

    campos_alumno = ft.Column(
        [
            matricula,
            ft.Row([grado, grupo], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=380)
        ],
        spacing=10,
        visible=True
    )

    # --- Campo Exclusivo de Validación para Maestros ---
    # --- Campo Exclusivo de Validación para Maestros Corregido ---
    token_maestro = ft.TextField(
        label="Código de Autorización Docente",
        prefix_icon=ft.Icons.KEY_OUTLINED,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=8,
        border_color=ft.Colors.RED_300,
        focused_border_color=ft.Colors.RED_700,
    )

    campo_seguridad_maestro = ft.Column(
        [
            token_maestro,
            # Reemplazamos helper_text por un control Text nativo para evitar errores
            ft.Text(
                " * Este código es proporcionado por la dirección de la escuela.", 
                size=11, 
                color=ft.Colors.RED_600,
                italic=True
            )
        ],
        spacing=5,
        visible=False # Oculto al inicio porque arranca en modo 'alumno'
    )
    
    correo = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.MAIL_OUTLINE, 
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700,
        keyboard_type=ft.KeyboardType.EMAIL
    )
    
    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )
    
    confirm_password = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )
    
    mensaje = ft.Text("", color=ft.Colors.RED_600, weight=ft.FontWeight.W_500, size=13)
    
    def registrar_click(e):
        rol_seleccionado = list(selector_rol.selected)[0]

        if not nombre.value or not correo.value or not password.value or not confirm_password.value:
            mensaje.value = "Por favor, llena todos los campos obligatorios."
            page.update()
            return
        
        if rol_seleccionado == "alumno":
            if not apellido_paterno.value or not matricula.value:
                mensaje.value = "El apellido paterno y la matrícula son obligatorios."
                page.update()
                return
        
        if rol_seleccionado == "maestro":
            if not token_maestro.value:
                mensaje.value = "Se requiere el código de autorización docente."
                page.update()
                return
            if token_maestro.value.strip() != CLAVE_SECRET_DOCENTE:
                mensaje.value = "Código de autorización incorrecto. No puedes registrarte como Maestro."
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
        
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo.value):
            mensaje.value = "Correo electrónico inválido."
            page.update()
            return
        
        rol_final = "DOCENTE" if rol_seleccionado == "maestro" else "ALUMNO"

        nombre_guardar = nombre.value.strip()
        if rol_final == "DOCENTE" and apellido_paterno.value:
            nombre_guardar = f"{nombre.value.strip()} {apellido_paterno.value.strip()}"
            if apellido_materno.value:
                nombre_guardar += f" {apellido_materno.value.strip()}"

        usuario_data = UsuarioSchema(
            nombre=nombre_guardar,
            apellido_paterno=apellido_paterno.value.strip() if rol_seleccionado == "alumno" else None,
            apellido_materno=apellido_materno.value.strip() if (rol_seleccionado == "alumno" and apellido_materno.value) else None,
            matricula=matricula.value.strip() if rol_seleccionado == "alumno" else None,
            grado=grado.value.strip() if (rol_seleccionado == "alumno" and grado.value) else None,
            grupo=grupo.value.strip() if (rol_seleccionado == "alumno" and grupo.value) else None,
            correo=correo.value.strip(),
            password=password.value,
            rol=rol_final  
        )
        
        exito, msg = auth_controller.registrar(usuario_data)
        
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión.", ft.Colors.GREEN_600)
            nombre.value = ""
            apellido_paterno.value = ""
            apellido_materno.value = ""
            matricula.value = ""
            grado.value = ""
            grupo.value = ""
            token_maestro.value = ""
            correo.value = ""
            password.value = ""
            confirm_password.value = ""
            mensaje.value = ""
            page.update()
            page.go("/")
        else:
            mensaje.value = msg or "Error al registrar usuario."
            page.update()
    
    btn_registrar = ft.ElevatedButton(
        "Registrarse",
        width=380,
        height=50,
        on_click=registrar_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    btn_login = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión aquí",
        style=ft.ButtonStyle(color=ft.Colors.PURPLE_700),
        on_click=lambda _: page.go("/")
    )

    tarjeta_registro = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=50, color=ft.Colors.PURPLE_600),
                ft.Text("Crear Nueva Cuenta", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
                ft.Text("Completa tus datos para darte de alta en el sistema", size=13, color=ft.Colors.BLUE_GREY_400, text_align=ft.TextAlign.CENTER),
                ft.Container(height=5),
                selector_rol,
                ft.Container(height=5),
                nombre,
                apellido_paterno,
                apellido_materno,
                campos_alumno,
                campo_seguridad_maestro,
                correo,
                password,
                confirm_password,
                mensaje,
                ft.Container(height=5),
                btn_registrar,
                ft.Divider(height=25, color=ft.Colors.BLUE_GREY_100),
                btn_login
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
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
        route="/register",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_50,
        scroll=ft.ScrollMode.AUTO, 
        appbar=ft.AppBar(
            title=ft.Text("ScanClass", weight=ft.FontWeight.W_500, size=20),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            elevation=2,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=lambda _: page.go("/"))
        ),
        controls=[
            ft.Container(content=tarjeta_registro, padding=ft.Padding(0, 20, 0, 20))
        ]
    )