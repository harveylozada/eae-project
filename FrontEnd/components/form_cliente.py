import flet as ft
from flet import icons
from services.api_service import create_client, update_client

class ClientForm(ft.Container):
    def __init__(self, page, client=None, on_success=None):
        super().__init__()
        self.page = page
        self.client = client
        self.on_success = on_success

        form_title = "Editar Cliente" if self.client else "Crear Nuevo Cliente"
        self.name_field = ft.TextField(label="Nombre*", value=self.client.get("nombre", "") if self.client else "", bgcolor="white10", color="white")
        self.lastname_field = ft.TextField(label="Apellido", value=self.client.get("apellido", "") if self.client else "", bgcolor="white10", color="white")
        self.email_field = ft.TextField(label="Email*", value=self.client.get("email", "") if self.client else "", bgcolor="white10", color="white")
        self.phone_field = ft.TextField(label="Teléfono", value=self.client.get("telefono", "") if self.client else "", bgcolor="white10", color="white")
        self.address_field = ft.TextField(label="Dirección", value=self.client.get("direccion", "") if self.client else "", multiline=True, bgcolor="white10", color="white")

        self.save_button = ft.ElevatedButton(
            text="Guardar", on_click=self.save_client,
            bgcolor="blue_700", color="white", icon=icons.SAVE
        )
        self.cancel_button = ft.ElevatedButton(
            text="Cancelar", on_click=self.cancel_form,
            bgcolor="white12", color="white"
        )

        self.content = ft.Column([
            ft.Text(form_title, size=20, weight=ft.FontWeight.BOLD, color="cyan_accent_400"),
            self.name_field, self.lastname_field, self.email_field,
            self.phone_field, self.address_field,
            ft.Row([self.cancel_button, self.save_button], alignment=ft.MainAxisAlignment.END),
        ])
        self.padding = 20
        self.border_radius = 10
        self.bgcolor = "#2D3038"

    def cancel_form(self, e):
        if self.on_success:
            self.on_success("Operación cancelada.")

    def validate_fields(self):
        is_valid = True
        if not self.name_field.value:
            self.name_field.error_text = "El nombre es obligatorio"
            is_valid = False
        else:
            self.name_field.error_text = None
        if not self.email_field.value:
            self.email_field.error_text = "El email es obligatorio"
            is_valid = False
        else:
            self.email_field.error_text = None
        self.update()
        return is_valid

    def save_client(self, e):
        if not self.validate_fields():
            return
        data = {
            "nombre": self.name_field.value, "apellido": self.lastname_field.value,
            "email": self.email_field.value, "telefono": self.phone_field.value,
            "direccion": self.address_field.value
        }
        try:
            if self.client:
                client_id = self.client.get("id")
                update_client(client_id, data)
                message = f"Cliente {client_id} actualizado correctamente."
            else:
                create_client(data)
                message = "Cliente creado correctamente."
            if self.on_success:
                self.on_success(message)
        except Exception as e:
            print(f"Error en save_client: {type(e).__name__}: {e}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {e}"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
