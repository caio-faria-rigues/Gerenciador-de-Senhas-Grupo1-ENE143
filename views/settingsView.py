import flet as ft
from views.view import View

class SettingsView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        

    def render(self):
        actual_master_password = ft.TextField(
            label=ft.Text("Insira a senha-mestra atual", color=self.theme['primary_color']),
            bgcolor=self.theme["app_bgcolor"],
            color=self.theme['secondary_color'],
            password=True,
            can_reveal_password=True,
            border_color=self.theme['primary_color'],
            height=45,
            expand=0.4,
        )
        new_master_password = ft.TextField(
            label=ft.Text("Insira a nova senha-mestra", color=self.theme['primary_color']),
            bgcolor=self.theme["app_bgcolor"],
            color=self.theme['secondary_color'],
            password=True,
            can_reveal_password=True,
            border_color=self.theme['primary_color'],
            height=45,
            expand=0.4,
        )
        submit_new_master_password = ft.ElevatedButton(
            text="Atualizar senha-mestra",
            color=self.theme['secondary_color'],
            bgcolor=self.theme['primary_color'],
            height=45,
            expand=0.2,
        )
        theme_switch = ft.Switch(
            label=ft.Text("Tema claro", color=self.theme['text_color']),
            #on_change=self.toggle_theme,
            active_color=self.theme['primary_color'],
            active_track_color=self.theme['secondary_color'],
            inactive_thumb_color=self.theme['primary_color_selected'],
            inactive_track_color=self.theme['secondary_color'],
            track_outline_color=self.theme['primary_color'],
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configurações", size=30, weight=ft.FontWeight.BOLD, color=self.theme['text_color']),
                    ft.Text("Configure os ajustes da aplicação / Trabalho em progresso.", size=16, color=self.theme['text_color']),
                    ft.Divider(color=self.theme['primary_color']),
                    ft.Text("Atualizar senha-mestra", size=16, color=self.theme['text_color']),
                    ft.Row(
                        [
                            actual_master_password,
                            new_master_password,
                            submit_new_master_password
                        ],
                    ),
                    ft.Text("Tema", size=16, color=self.theme['text_color']),
                    theme_switch,
                ]
            ),
            expand=True,
        )