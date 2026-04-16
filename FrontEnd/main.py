import flet as ft
from views.home_view import HomeView
from views.crud_view import CrudView
from views.analytics_view import AnalyticsView

def main(page: ft.Page):
    page.title = "Gestión de Clientes Empresa Amiga"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.CYAN_ACCENT_400,
            secondary=ft.colors.BLUE_GREY_700,
            background="#20232A",
            surface="#2D3038",
            on_primary=ft.colors.BLACK,
            on_secondary=ft.colors.WHITE,
            on_surface=ft.colors.WHITE70,
        ),
        
    )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "/crud":
            page.views.append(CrudView(page))
        elif page.route == "/analytics":
            page.views.append(AnalyticsView(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=8501, assets_dir="assets")
