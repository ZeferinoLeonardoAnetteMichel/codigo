import flet as ft
from controllers.userController import AuthController
from views.loginView import LoginView
from views.registroView import RegisterView 
from views.dashboardView import DashboardView
from views.asistenciaView import AsistenciaView      

def start(page: ft.Page):
    # Configuración inicial de la ventana (Estilo Teléfono / App Móvil)
    page.title = "Sistema SIGE - ScanClass"
    page.window_width = 450
    page.window_height = 700
    
    # Inicializamos el controlador de autenticación
    auth_ctrl = AuthController()

    # --- MANEJADOR DE RUTAS (Navegación limpia) ---
    def route_change(e):
        page.views.clear()

        # 1. Pantalla de Inicio de Sesión
        if page.route == "/":
            page.views.append(LoginView(page, auth_ctrl))
            
        # 2. Pantalla de Registro
        elif page.route == "/register": 
            page.views.append(RegisterView(page, auth_ctrl))
            
        # 3. Panel de Control (Dedicado y protegido por Roles)
        elif page.route == "/dashboard":
            rol = getattr(page, "user_role", None)
            
            if rol == "maestro":
                page.views.append(AsistenciaView(page))
            elif rol == "alumno":
                page.views.append(DashboardView(page))
            else:
                # Si intentan forzar la URL /dashboard sin loguearse, limpieza total y al Login
                page.route = "/"
                page.views.append(LoginView(page, auth_ctrl))
                
        # 4. Manejo de errores por si colapsa una ruta o queda vacía
        if not page.views:
            page.views.append(
                ft.View("/error", [ft.Text("Error: Ruta no encontrada o vista vacía")])
            )

        page.update()
        
    # --- MANEJADOR DEL BOTÓN ATRÁS NATIVO / REGRESAR ---
    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
            
    # Asignamos los eventos a la página
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Arrancamos la aplicación siempre apuntando a la raíz (Login)
    if page.route == "/":
        route_change(None)
    else:
        page.go("/")
    
def main():
    # Lanzamos la aplicación Flet
    ft.app(target=start)

if __name__ == "__main__":
    main()