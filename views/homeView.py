import flet as ft
from views.view import View

class HomeView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)

    def render(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Bem-vindo ao Gerenciador de Senhas!", size=30, weight=ft.FontWeight.BOLD, color=self.theme['text_color']),
                    ft.Text("Use a barra lateral para navegar entre as seções do aplicativo.", size=16, color=self.theme['text_color']),
                    ft.Divider(color=self.theme['primary_color']),
                    ft.Row(
                        [
                            ft.TextField(
                                label=ft.Text("Insira a senha-mestra", color=self.theme['primary_color']),
                                bgcolor=self.theme["app_bgcolor"],
                                color=self.theme['secondary_color'],
                                password=True,
                                can_reveal_password=True,
                                border_color=self.theme['primary_color'],
                                on_submit=self._handle_master_password,
                                height=45,
                                expand=0.5,
                            ),
                            ft.ElevatedButton(
                                text="Verificar senha-mestra",
                                color=self.theme['secondary_color'],
                                bgcolor=self.theme['primary_color'],
                                on_click=self._handle_master_password,
                                height=45,
                                expand=0.2,
                            )
                        ],
                    )
                ]
            ),
            expand=True,
            bgcolor=self.theme['secondary_color'],
        )
    
    def _handle_master_password(self, e):
        # Aqui você pode implementar a lógica para verificar a senha-mestra
        # Por exemplo, comparar com uma senha pré-definida ou verificar em um banco de dados
        pass