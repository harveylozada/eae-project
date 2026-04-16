import flet as ft

class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/"
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [
            ft.Text("Bienvenido a la Aplicación de Gestión", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Seleccione una opción para comenzar", size=18, color=ft.colors.WHITE70),
            ft.Container(height=30), # Spacer
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Gestionar Clientes (CRUD)",
                        icon=ft.icons.PEOPLE,
                        on_click=lambda _: self.page.go("/crud"),
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            bgcolor=ft.colors.BLUE_GREY_700,
                        )
                    ),
                    ft.ElevatedButton(
                        text="Ver Analíticas",
                        icon=ft.icons.ANALYTICS,
                        on_click=lambda _: self.page.go("/analytics"),
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            bgcolor=ft.colors.CYAN_ACCENT_400,
                            color=ft.colors.BLACK
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ]
