import flet as ft
import re

def RegisterView(page: ft.Page, auth_controller):
    
    # --- COMPONENTES DE ENTRADA (TextFields) ---
    matricula = ft.TextField(
        label="Matrícula",
        prefix_icon=ft.Icons.CARD_MEMBERSHIP,
        width=400,
        border_radius=10,
        border_color="purple",
        keyboard_type=ft.KeyboardType.NUMBER  # Optimizado para números
    )

    nombre = ft.TextField(
        label="Nombre(s)",
        prefix_icon=ft.Icons.PERSON,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    apellido = ft.TextField(
        label="Apellidos",
        prefix_icon=ft.Icons.PERSON,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    email = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.EMAIL,
        width=400,
        border_radius=10,
        border_color="purple",
        keyboard_type=ft.KeyboardType.EMAIL
    )
    
    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    confirm_password = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=10,
        border_color="purple"
    )
    
    mensaje = ft.Text("", color="red", size=12)
    
    # --- FUNCIONES AUXILIARES DE INTERFAZ ---
    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()
        
    def ir_login(e):
        page.go("/")
    
    # --- MANEJADOR DEL EVENTO CLICK REGISTRAR ---
    def registrar_click(e):
        # 1. Validaciones básicas (Ahora incluye matrícula)
        if not matricula.value or not nombre.value or not email.value or not password.value or not confirm_password.value:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = "red"
            page.update()
            return
        
        # 2. Validación de coincidencia de contraseñas
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = "red"
            page.update()
            return
        
        # 3. Validación de longitud de contraseña
        if len(password.value) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres"
            mensaje.color = "red"
            page.update()
            return
        
        # 4. Validación por Expresión Regular del correo electrónico
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.value):
            mensaje.value = "Correo electrónico inválido"
            mensaje.color = "red"
            page.update()
            return
        
        # ---------------------------------------------------------------------
        # ¡SOLUCIÓN!: Ahora sí enviamos la 'matricula' requerida por el controlador
        # ---------------------------------------------------------------------
        exito, msg = auth_controller.registrar(
            matricula=matricula.value.strip(),
            nombre=nombre.value.strip(),
            correo=email.value.strip(),
            password=password.value
        )
        
        # 5. Respuesta del Servidor / Base de Datos
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión", ft.Colors.GREEN)
            # Limpieza total del formulario
            matricula.value = ""
            nombre.value = ""
            apellido.value = ""  
            email.value = ""
            password.value = ""
            confirm_password.value = ""
            mensaje.value = ""
            page.update()
            
            # Redirección inmediata al Login
            page.go("/")
        else:
            mensaje.value = msg or "Error al registrar usuario"
            mensaje.color = "red"
            page.update()
            
    # --- BOTONES DE ACCIÓN ---
    btn_registrar = ft.ElevatedButton(
        "Registrarse",
        width=250,
        on_click=registrar_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_200,
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
            bgcolor=ft.Colors.PURPLE_200,
            color=ft.Colors.WHITE,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"))
        ),
        controls=[
            ft.ListView([  # Cambiado a ListView para evitar desbordes en pantallas chicas al añadir más inputs
                ft.Column(
                    [
                        ft.Text("Crear Nueva Cuenta", size=35, weight="bold", color="purple"),
                        ft.Container(height=10),
                        matricula,  # Agregado visualmente
                        nombre,
                        apellido,
                        email,
                        password,
                        confirm_password,
                        mensaje,
                        ft.Container(height=10),
                        btn_registrar,
                        ft.Container(height=10),
                        btn_login
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                    spacing=15
                )
            ], expand=True)
        ]
    )