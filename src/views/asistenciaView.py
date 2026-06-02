import flet as ft
import datetime
import hashlib
import threading
import qrcode
import os

def AsistenciaView(page: ft.Page, auth_controller=None):
    if auth_controller is None:
        auth_controller = getattr(page, "auth_ctrl", None)

    # -------------------------------------------------------------------------
    # LÓGICA GENERADORA DEL QR DINÁMICO LOCAL (Cada 5 minutos)
    # -------------------------------------------------------------------------
    def generar_codigo_temporal():
        ahora = datetime.datetime.now()
        # Dividimos los minutos entre 5 para crear 12 bloques únicos por hora
        bloque_5min = ahora.minute // 5
        
        # Creamos una cadena única combinando la fecha, hora y el bloque de 5 min
        semilla = f"ScanClass_Secret_Salt_{ahora.strftime('%Y-%m-%d_%H')}_{bloque_5min}"
        
        # Generamos un Hash MD5 corto (primeros 8 caracteres) para el QR
        codigo_hash = hashlib.md5(semilla.encode()).hexdigest()[:8]
        return codigo_hash

    # Componente visual donde se renderizará el QR
    qr_imagen = ft.Image(src="", width=200, height=200, fit="contain")
    txt_contador = ft.Text("El código cambia automáticamente cada 5 minutos.", size=12, color=ft.Colors.BLUE_GREY_400)

    def actualizar_qr_periodicamente():
        try:
            token_actual = generar_codigo_temporal()
            # Guardamos el token activo en la página del maestro por si se requiere validar
            page.token_qr_actual = token_actual 
            
            # 1. Crear el objeto QR con la librería local
            qr = qrcode.QRCode(version=1, box_size=10, border=1)
            qr.add_data(token_actual)
            qr.make(fit=True)
            
            # 2. Renderizar la matriz de pixeles a una imagen nativa
            img_qr = qr.make_image(fill_color="black", back_color="white")
            
            # 3. Definir ruta física dentro del directorio del proyecto (src/assets)
            ruta_dir = os.path.join("src", "assets")
            os.makedirs(ruta_dir, exist_ok=True)
            ruta_archivo = os.path.join(ruta_dir, "qr_temp.png")
            
            # 4. Guardar/Sobrescribir el archivo en disco
            img_qr.save(ruta_archivo)
            
            # 5. TRUCO ANTICACHÉ: Agregamos una estampa de tiempo (?v=HHMMSS) al string de la ruta.
            # Esto fuerza a Flet a refrescar el render visual cada vez que el archivo se modifica.
            marca_tiempo = datetime.datetime.now().strftime("%H%M%S")
            qr_imagen.src = f"{ruta_archivo}?v={marca_tiempo}"
            page.update()
            
        except Exception as ex:
            print("Error al actualizar el QR local:", ex)
        
        # Programamos la revisión del bloque de tiempo cada 10 segundos sin congelar la UI
        global timer_qr
        timer_qr = threading.Timer(10, actualizar_qr_periodicamente)
        timer_qr.daemon = True
        timer_qr.start()

    # Cancelar el timer si el docente decide cerrar sesión o cambiar de vista
    def limpiar_y_salir(e):
        if 'timer_qr' in globals():
            global timer_qr
            timer_qr.cancel()
        page.user_data = None
        page.user_role = None
        page.go("/")

    # Disparamos la primera generación e inicio del ciclo
    actualizar_qr_periodicamente()

    # -------------------------------------------------------------------------
    # APARTADO VISUAL EN EL DOCENTE
    # -------------------------------------------------------------------------
    apartado_qr_maestro = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.SECURITY, color=ft.Colors.PURPLE_700),
                ft.Text("Código de Acceso Dinámico (Antifraude)", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800)
            ]),
            ft.Divider(color=ft.Colors.PURPLE_100),
            ft.Container(
                content=qr_imagen,
                alignment=ft.Alignment(0, 0),
                padding=10,
                border=ft.Border(
                    top=ft.BorderSide(2, ft.Colors.PURPLE_200),
                    bottom=ft.BorderSide(2, ft.Colors.PURPLE_200),
                    left=ft.BorderSide(2, ft.Colors.PURPLE_200),
                    right=ft.BorderSide(2, ft.Colors.PURPLE_200)
                ),
                border_radius=10,
                bgcolor=ft.Colors.GREY_50
            ),
            txt_contador
        ]),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        border_radius=12,
        width=350,
    )

    return ft.View(
        route="/asistencia",
        bgcolor=ft.Colors.BLUE_GREY_50,
        appbar=ft.AppBar(
            title=ft.Text("ScanClass - Panel Docente"),
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, on_click=limpiar_y_salir)
            ]
        ),
        controls=[
            ft.Row([
                apartado_qr_maestro,
                # Aquí dejas tus contenedores actuales de Tablas (Presentes / Ausentes)
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
        ]
    )