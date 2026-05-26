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

    email = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.EMAIL,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700,
        keyboard_type=ft.KeyboardType.EMAIL
    )
    
    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )
    
    confirm_password = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )
    
    mensaje = ft.Text("", color="red", size=12)

    # --- CONTENEDORES DINÁMICOS SEGÚN EL ROL ---
    
    # Campo exclusivo de Alumnos: Matrícula
    matricula = ft.TextField(
        label="Matrícula",
        prefix_icon=ft.Icons.CARD_MEMBERSHIP,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700,
        keyboard_type=ft.KeyboardType.NUMBER  
    )
    
    campos_alumno = ft.Column([matricula], visible=True, spacing=10)

    # Campo exclusivo de Maestros: Código de Seguridad
    codigo_token = ft.TextField(
        label="Código de Seguridad Docente",
        prefix_icon=ft.Icons.SECURITY,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=8,
        border_color=ft.Colors.PURPLE_300,
        focused_border_color=ft.Colors.PURPLE_700
    )
    
    campo_seguridad_maestro = ft.Column([codigo_token], visible=False, spacing=10)

    # --- MANEJADOR DEL EVENTO CLICK REGISTRAR ---
    def registrar_click(e):
        rol_actual = list(selector_rol.selected)[0]

        # 1. Validaciones generales obligatorias
        if not nombre.value or not apellido_paterno.value or not email.value or not password.value or not confirm_password.value:
            mensaje.value = "Por favor, llena todos los campos obligatorios."
            mensaje.color = "red"
            page.update()
            return
        
        # 2. Validación específica de Alumno (Matrícula obligatoria)
        if rol_actual == "alumno" and not matricula.value:
            mensaje.value = "La matrícula es obligatoria para alumnos."
            mensaje.color = "red"
            page.update()
            return

        # 3. Validación específica de Maestro (Filtro por Token Secreto)
        if rol_actual == "maestro":
            if not codigo_token.value:
                mensaje.value = "Introduce el código de autorización docente."
                mensaje.color = "red"
                page.update()
                return
            if codigo_token.value.strip() != CLAVE_SECRET_DOCENTE:
                mensaje.value = "Código docente inválido. No tienes autorización."
                mensaje.color = "red"
                page.update()
                return
        
        # 4. Validación de coincidencia de contraseñas
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden."
            mensaje.color = "red"
            page.update()
            return
        
        # 5. Validación de longitud de contraseña
        if len(password.value) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres."
            mensaje.color = "red"
            page.update()
            return
        
        # 6. Validación por Expresión Regular del correo electrónico
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.value):
            mensaje.value = "Correo electrónico inválido."
            mensaje.color = "red"
            page.update()
            return

        # Construcción del nombre completo o envío estructurado
        apellido_completo = f"{apellido_paterno.value.strip()} {apellido_materno.value.strip()}".strip()
        
        # Si es maestro, enviamos un valor vacío o None a la matrícula para que el controlador no proteste
        matricula_envio = matricula.value.strip() if rol_actual == "alumno" else "DOCENTE"

        # 7. Envío de parámetros limpios al controlador
        exito, msg = auth_controller.registrar(
            matricula=matricula_envio,
            nombre=nombre.value.strip(),
            correo=email.value.strip(),
            password=password.value
        )
        
        # 8. Respuesta del Controlador / Base de Datos
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión", ft.Colors.GREEN_600)
            
            # Limpieza absoluta de todo el formulario
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
            mensaje.color = "red"
            page.update()
            
    # --- BOTONES DE ACCIÓN ---
    btn_registrar = ft.ElevatedButton(
        "Registrarse",
        width=250,
        on_click=registrar_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    btn_login = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión",
        on_click=ir_login
    )
    
    # --- RETORNO DE LA VISTA ESTRUCTURADA ---
    return ft.View(
        route="/register",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("SIGE - Registro"),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"))
        ),
        controls=[
            ft.ListView([ 
                ft.Column(
                    [
                        ft.Text("Crear Nueva Cuenta", size=32, weight="bold", color="purple"),
                        ft.Container(height=5),
                        selector_rol,
                        ft.Container(height=10),
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        campos_alumno,            # Aparece si es Alumno
                        campo_seguridad_maestro,  # Aparece si es Maestro
                        email,
                        password,
                        confirm_password,
                        mensaje,
                        ft.Container(height=10),
                        btn_registrar,
                        ft.Container(height=5),
                        btn_login
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                    spacing=12
                )
            ], expand=True, padding=20)
        ]
    )