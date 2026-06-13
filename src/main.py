import flet as ft
from controllers.userController import AuthController
from views.loginView import LoginView
from views.registroView import RegisterView 
from views.dashboardView import DashboardView
from views.asistenciaView import AsistenciaView      

def start(page: ft.Page):
    page.title = "Escaner Dinamico - ScanClass"
    page.window_width = 450
    page.window_height = 700    
    auth_ctrl = AuthController()
    page.auth_ctrl = auth_ctrl 

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(LoginView(page, auth_ctrl))            
        elif page.route == "/register": 
            page.views.append(RegisterView(page, auth_ctrl))            
        elif page.route == "/asistencia":
            page.views.append(AsistenciaView(page, auth_ctrl))
        elif page.route == "/dashboard":
            rol = getattr(page, "user_role", None)
            if rol == "maestro":
                page.views.append(AsistenciaView(page, auth_controller=auth_ctrl))
            elif rol == "alumno":
                page.views.append(DashboardView(page, auth_controller=auth_ctrl))
            else:
                page.route = "/"
                page.views.append(LoginView(page, auth_ctrl))                
        if not page.views:
            page.views.append(
                ft.View("/error", [ft.Text("Error: Ruta no encontrada o vista vacía")])
            )

        page.update()
        
    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)            
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    if page.route == "/":
        route_change(None)
    else:
        page.go("/")
    
def main():
    ft.app(target=start)

if __name__ == "__main__":
    main()