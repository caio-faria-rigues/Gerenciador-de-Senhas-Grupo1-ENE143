import flet as ft
from views.view import View

class SettingsView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        

    def render(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configurações")
                ]
            ),
            expand=True,
        )