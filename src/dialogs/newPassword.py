import flet as ft
from app.masterPasswordHandler import MasterPasswordHandler

class NewPasswordDialog(ft.AlertDialog):
    """
    Caixa de diálogo para adicionar uma nova senha. 
    O método `open_dialog` aceita um callback `on_submit` que é chamado quando o usuário clica em "Adicionar". 
    Os campos são limpos após cada submissão ou cancelamento.
    """
    def __init__(self, page: ft.Page, pallete, master_password_handler):
        self.master_password_handler = master_password_handler

        self.site = ft.TextField(
            label=ft.Text("Site/App/Serviço", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            border_color=pallete['primary_color'],
            height=45,
            expand=True,
            autocorrect=False,
            enable_suggestions=False,
        )
        self.user = ft.TextField(
            label=ft.Text("Usuário/Email", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            border_color=pallete['primary_color'],
            height=45,
            expand=True,
            autocorrect=False,
            enable_suggestions=False,
        )
        self.senha = ft.TextField(
            label=ft.Text("Senha", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            password=True,
            can_reveal_password=True,
            border_color=pallete['primary_color'],
            height=45,
            autocorrect=False,
            enable_suggestions=False,
        )
        self.senha_mestra = ft.TextField(
            label=ft.Text("Senha Mestra", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            password=True,
            can_reveal_password=True,
            border_color=pallete['primary_color'],
            height=45,
            autocorrect=False,
            enable_suggestions=False,
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
        self.submitted = False
        self.on_submit = None
        self.page.overlay.append(self)

    def open_dialog(self, on_submit=None):
        self.submitted = False
        self.on_submit = on_submit
        self.open = True
        self.page.update()

    def close_dialog(self):
        self.open = False
        self.page.update()

    def on_cancel(self, e=None):
        self.close_dialog()

    def on_add(self, e):
        if not self.site.value or not self.user.value or not self.senha.value or not self.senha_mestra.value:
            print("Campos não preenchidos")
            self.page.open(ft.SnackBar(content=ft.Text("Campos não preenchidos...", color=self.pallete['secondary_color']),bgcolor=self.pallete['primary_color']))
            return
        if not self.master_password_handler.verify_master_password(self.senha_mestra.value):
            print("Senha-mestra incorreta!")
            self.page.open(ft.SnackBar(content=ft.Text("Senha-mestra incorreta!", color=self.pallete['secondary_color']),bgcolor=self.pallete['primary_color']))
            return
        self.page.open(ft.SnackBar(content=ft.Text("Senha adicionada com sucesso!", color=self.pallete['secondary_color']),bgcolor=self.pallete['primary_color']))

        self.submitted = True
        self.close_dialog()
        self.site.value = ""
        self.user.value = ""
        self.senha.value = ""
        self.senha_mestra.value = ""
        if self.on_submit:
            self.on_submit()