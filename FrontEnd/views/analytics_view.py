import flet as ft
from services.api_service import get_analytics_summary

class AnalyticsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/analytics"
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.appbar = ft.AppBar(
            title=ft.Text("Analíticas de Ventas"),
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: self.page.go("/")
            ),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        self.summary_cards = ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND)
        self.products_chart = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )

        # Simple on-screen log viewer
        self.log_list = ft.ListView(expand=False, height=120, spacing=2, auto_scroll=True)
        self.logs_panel = ft.ExpansionTile(
            title=ft.Text("Logs"),
            initially_expanded=False,
            controls=[
                ft.Container(
                    content=self.log_list,
                    bgcolor=ft.colors.with_opacity(0.06, ft.colors.WHITE),
                    border_radius=6,
                    padding=10,
                )
            ],
        )

        self.controls = [
            ft.Row([
                ft.Text("Resumen General", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Actualizar", icon=ft.icons.REFRESH, on_click=lambda _: self.load_data())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=900),
            self.summary_cards,
            ft.Container(height=20),
            ft.Text("Top 5 Productos Más Vendidos", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=self.products_chart,
                height=400,
                width=700,
                padding=10,
            ),
            self.logs_panel,
        ]
        # Mount state
        self._mounted = False

    def did_mount(self):
        # Called by Flet when the control is added to the page
        self._mounted = True
        self.log("View mounted; loading data...")
        self.load_data()

    def load_data(self):
        try:
            summary = get_analytics_summary()
            self.log(f"API Response: {summary}")
            self.update_summary_cards(summary)

            # Get products data (limit to top 5)
            products_data = summary.get("productos_mas_vendidos", [])[:5]
            self.log(f"Products data: {products_data}")

            # If no data from API, use test data to verify chart works
            if not products_data:
                self.log("No products data from API, using test data")
                products_data = [
                    {"nombre": "Producto A", "total_vendido": 150},
                    {"nombre": "Producto B", "total_vendido": 120},
                    {"nombre": "Producto C", "total_vendido": 100},
                    {"nombre": "Producto D", "total_vendido": 80},
                    {"nombre": "Producto E", "total_vendido": 60}
                ]

            self.update_horizontal_bars(products_data)
            if self._mounted and self.products_chart.page is not None:
                self.products_chart.update()
        except Exception as e:
            self.log(f"Error in load_data: {e}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al cargar analíticas: {e}"), bgcolor="Red")
            self.page.snack_bar.open = True
            self.page.update()

    def update_summary_cards(self, summary):
        self.summary_cards.controls = [
            self.create_card("Total Clientes", summary.get("total_clientes", 0), ft.icons.PEOPLE),
            self.create_card("Total Ventas (Cantidad)", summary.get("total_ventas_cantidad", 0), ft.icons.SHOPPING_CART),
            self.create_card("Ingresos Totales", f"${summary.get('total_ventas_ingresos', 0):,.0f}", ft.icons.ATTACH_MONEY),
        ]
        self.update()

    def create_card(self, title, value, icon):
        return ft.Card(
            content=ft.Container(
                padding=20,
                width=250,
                content=ft.Column([
                    ft.Row([ft.Icon(icon), ft.Text(title, weight=ft.FontWeight.BOLD)]),
                    ft.Text(str(value), size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                ])
            )
        )

    def update_horizontal_bars(self, top_products):
        self.log(f"Received {len(top_products) if top_products else 0} products")
        if top_products:
            for p in top_products:
                self.log(f"Product {p.get('nombre')} - Sales: {p.get('total_vendido')}")
        
        self.products_chart.controls.clear()
        
        if not top_products:
            self.products_chart.controls = [ft.Text("No hay datos disponibles", size=16, color=ft.colors.WHITE70)]
            if self._mounted and self.products_chart.page is not None:
                self.products_chart.update()
            return

        colors = [ft.colors.CYAN_ACCENT_400, ft.colors.BLUE_400, ft.colors.INDIGO_400, ft.colors.PURPLE_400, ft.colors.PINK_400]
        max_value = max(p['total_vendido'] for p in top_products) if top_products else 1
        self.log(f"Max value: {max_value}")
        
        for i, product in enumerate(top_products):
            color = colors[i % len(colors)]
            percentage = (product['total_vendido'] / max_value)
            bar_width = max(80, int(500 * percentage))  # Min 80px, max 500px for better visibility
            
            # Create a simple bar with text
            bar_container = ft.Container(
                content=ft.Column([
                    # Product name and value row
                    ft.Row([
                        ft.Text(f"{i+1}. {product['nombre']}", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Text(f"{product['total_vendido']:,}", size=14, weight=ft.FontWeight.BOLD, color=color)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    # Bar
                    ft.Container(
                        width=bar_width,
                        height=20,
                        bgcolor=color,
                        border_radius=3,
                        content=ft.Text(f"{percentage*100:.0f}%", size=10, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center
                    )
                ], spacing=5),
                padding=ft.padding.symmetric(vertical=8, horizontal=10),
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                border_radius=5,
                margin=ft.margin.only(bottom=5)
            )
            self.products_chart.controls.append(bar_container)
            self.log(f"Added bar for {product['nombre']} with width {bar_width}")
        
        if self._mounted and self.products_chart.page is not None:
            self.products_chart.update()
        self.log("Chart updated")

    def log(self, message: str):
        # Print to console (for dev) and also to on-screen log
        try:
            print(f"DEBUG: {message}")
        except Exception:
            pass
        # If view is not mounted yet, avoid updating controls
        if not getattr(self, "_mounted", False) or self.log_list.page is None:
            return
        self.log_list.controls.append(ft.Text(str(message), size=11, color=ft.colors.GREY_400))
        # Avoid excessive page updates by updating only the list
        self.log_list.update()
