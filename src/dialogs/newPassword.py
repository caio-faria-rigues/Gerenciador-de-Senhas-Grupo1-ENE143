import flet as ft
from app.masterPasswordHandler import MasterPasswordHandler

class NewPasswordDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, pallete):
        self.master_password_handler = MasterPasswordHandler()

        self.site = ft.TextField(
            label=ft.Text("Site/App/Serviço", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            border_color=pallete['primary_color'],
            height=45,
            expand=True,
            )
        self.user = ft.TextField(
            label=ft.Text("Usuário/Email", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            border_color=pallete['primary_color'],
            height=45,
            expand=True,
        )
        self.senha = ft.TextField(
            label=ft.Text("Senha", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            password=True,
            can_reveal_password=True,
            border_color=pallete['primary_color'],
            height=45,
        )
        self.senha_mestra = ft.TextField(
            label=ft.Text("Senha Mestra", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            password=True,
            can_reveal_password=True,
            border_color=pallete['primary_color'],
            height=45,
        )

        super().__init__(
            title=ft.Text("Adicione uma nova senha:", color=pallete['text_color']),
            bgcolor=pallete['secondary_color'],
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.site,
                            self.user,
                        ]
                    ),
                    self.senha,
                    self.senha_mestra,
                ],
                spacing=15,
                tight=True,
                width=400,
            ),
            actions=[
                ft.ElevatedButton("Cancelar", color=pallete['primary_color'], bgcolor=pallete['secondary_color'], on_click=self.on_cancel, elevation=0),
                ft.ElevatedButton("Adicionar", color=pallete['primary_color'], bgcolor=pallete['secondary_color'], on_click=self.on_add, elevation=0),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self.on_cancel
        )
        self.page = page
        self.pallete = pallete
        self.password = ""

        self.page.overlay.append(self)

    def open_dialog(self):
        self.open = True
        self.page.update()

    def close_dialog(self):
        self.open = False
        self.page.update()
    
    def on_cancel(self, e=None):
        self.close_dialog()
    
    def on_add(self, e):
        print(
            self.master_password_handler.new_login(
                self.site.value,
                self.user.value,
                self.senha.value,
                self.senha_mestra.value
            )
        )

        self.close_dialog()

    def _handle_new_password(self, e):
        pass