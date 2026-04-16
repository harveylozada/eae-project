import flet as ft
from components.list_clients import ClientsList

class CrudView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/crud"
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.appbar = ft.AppBar(
            title=ft.Text("Gestión de Clientes (CRUD)"),
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: self.page.go("/")
            ),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        self.controls = [
            ft.Container(
                content=ClientsList(page=self.page),
                width=800,
                padding=10
            )
        ]
