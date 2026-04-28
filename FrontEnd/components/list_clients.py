import flet as ft
from flet import icons
from components.form_cliente import ClientForm
from services.api_service import get_clients, delete_client


class ClientsList(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page

        # Variables de paginación
        self.page_size = 10
        self.current_page = 1
        self.all_clients = []

        # Tabla de clientes
        self.client_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color="grey_300")),
                ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD, color="grey_300")),
                ft.DataColumn(ft.Text("Edad", weight=ft.FontWeight.BOLD, color="grey_300")), # NUEVO
                ft.DataColumn(ft.Text("Género", weight=ft.FontWeight.BOLD, color="grey_300")), # NUEVO
                ft.DataColumn(ft.Text("Ubicación", weight=ft.FontWeight.BOLD, color="grey_300")), # NUEVO
                ft.DataColumn(ft.Text("Email", weight=ft.FontWeight.BOLD, color="grey_300")),
                ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD, color="grey_300")),
            ],
            rows=[],
        )

        # Contenedor con scroll
        self.table_container = ft.Container(
            content=ft.ListView(
                controls=[self.client_table],
                expand=True,
                spacing=5,
                auto_scroll=False
            ),
            height=600,
            bgcolor="#2D3038",
            padding=10,
            border_radius=8,
        )

        # Botón nuevo cliente
        self.new_client_button = ft.ElevatedButton(
            "➕ Nuevo Cliente", on_click=self.show_form,
            bgcolor="blue_grey_700", color="white", icon=icons.ADD
        )

        # Selector de cantidad por página
        self.page_size_dropdown = ft.Dropdown(
            label="Registros por página",
            value="10",
            options=[
                ft.dropdown.Option("10"),
                ft.dropdown.Option("25"),
                ft.dropdown.Option("50"),
                ft.dropdown.Option("100"),
            ],
            on_change=self.change_page_size,
            width=180,
        )

        # Texto de página
        self.page_label = ft.Text("Página 1 de 1", size=14, color="white", weight=ft.FontWeight.BOLD)

        # Botones de navegación
        self.prev_button = ft.IconButton(icon=icons.ARROW_BACK, tooltip="Anterior", on_click=self.prev_page)
        self.next_button = ft.IconButton(icon=icons.ARROW_FORWARD, tooltip="Siguiente", on_click=self.next_page)

        # Barra de paginación
        self.pagination_controls = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.page_size_dropdown,
                    ft.Row([self.prev_button, self.page_label, self.next_button], alignment=ft.MainAxisAlignment.CENTER),
                ],
            ),
            padding=10,
            bgcolor="#1E1E1E",
            border_radius=8,
        )

        # Formulario oculto
        self.form_container = ft.Column(visible=False)

        # Estructura principal
        self.controls = [
            ft.Row([self.new_client_button], alignment=ft.MainAxisAlignment.END),
            self.form_container,
            self.table_container,
            self.pagination_controls,
        ]

    def did_mount(self):
        self.load_data()

    # Cargar clientes desde API
    def load_data(self):
        try:
            self.all_clients = get_clients() or []
            self.current_page = 1
            self.show_page()
        except Exception as e:
            print(f"Error en load_data (list_clients): {type(e).__name__}: {e}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al cargar datos: {e}"), bgcolor="Red")
            self.page.snack_bar.open = True
            self.page.update()

    # Mostrar página actual
    def show_page(self):
        self.client_table.rows.clear()

        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_clients = self.all_clients[start:end]

        for client in page_clients:
            # Lógica para mostrar Género bonito
            gen = client.get("genero_id")
            genero_texto = "Masculino" if gen == 0 else "Femenino" if gen == 1 else "N/A"
            
            # Lógica para Ubicación
            ubicacion = f"{client.get('codigo_ciudad', '')}, {client.get('codigo_pais', '')}"

            self.client_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(client["id"]), color="white")),
                        ft.DataCell(ft.Text(f"{client.get('nombre', '')} {client.get('apellido', '')}", color="white")),
                        ft.DataCell(ft.Text(str(client.get("edad", "N/A")), color="white")), # NUEVO
                        ft.DataCell(ft.Text(genero_texto, color="white")), # NUEVO
                        ft.DataCell(ft.Text(ubicacion, color="white")), # NUEVO
                        ft.DataCell(ft.Text(client.get("email", ''), color="white")),
                        ft.DataCell(
                            ft.Row([
                                # ... (mantener los botones de editar y eliminar igual)
                                ft.IconButton(
                                    icon=icons.EDIT, tooltip="Editar", icon_color="amber",
                                    on_click=lambda e, c=client: self.edit_client(c)
                                ),
                                ft.IconButton(
                                    icon=icons.DELETE, tooltip="Eliminar", icon_color="red_400",
                                    on_click=lambda e, c_id=client["id"]: self.delete_client_confirm(c_id)
                                )
                            ])
                        )
                    ]
                )
            )

        if not page_clients:
            self.client_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No hay clientes en esta página.", italic=True, color="white54")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text(""))
                ])
            )

        # Actualizar indicador de página
        total_pages = max(1, (len(self.all_clients) + self.page_size - 1) // self.page_size)
        self.page_label.value = f"Página {self.current_page} de {total_pages}"

        # Deshabilitar botones cuando no aplican
        self.prev_button.disabled = self.current_page <= 1
        self.next_button.disabled = self.current_page >= total_pages

        self.update()

    # Botón siguiente
    def next_page(self, e):
        total_pages = max(1, (len(self.all_clients) + self.page_size - 1) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self.show_page()

    # Botón anterior
    def prev_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.show_page()

    # Cambiar registros por página
    def change_page_size(self, e):
        self.page_size = int(self.page_size_dropdown.value)
        self.current_page = 1
        self.show_page()

    def show_form(self, e):
        self.client_form = ClientForm(page=self.page, on_success=self.refresh_table)
        self.form_container.controls.clear()
        self.form_container.controls.append(self.client_form)
        self.form_container.visible = True
        self.update()

    def refresh_table(self, message: str = "Operación exitosa"):
        self.load_data()
        self.form_container.controls.clear()
        self.form_container.visible = False
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor="green_800")
        self.page.snack_bar.open = True
        self.page.update()

    def edit_client(self, client):
        self.client_form = ClientForm(page=self.page, client=client, on_success=self.refresh_table)
        self.form_container.controls.clear()
        self.form_container.controls.append(self.client_form)
        self.form_container.visible = True
        self.update()

    def delete_client_confirm(self, client_id):
        def on_confirm(e):
            try:
                delete_client(client_id)
                self.refresh_table(f"Cliente {client_id} eliminado correctamente.")
            except Exception as ex:
                print(f"Error en delete_client_confirm: {type(ex).__name__}: {ex}")
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"), bgcolor="red_800")
                self.page.snack_bar.open = True
                self.update()
            close_dialog(e)

        def close_dialog(e):
            confirm_dialog.open = False
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar eliminación", color="white"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar al cliente con ID {client_id}?", color="white70"),
            actions=[
                ft.TextButton("Sí, eliminar", on_click=on_confirm, style=ft.ButtonStyle(color="red_400")),
                ft.TextButton("Cancelar", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D3038"
        )
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()
