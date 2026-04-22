import flet as ft

class EnterMasterPasswordDialog(ft.AlertDialog):
    """
    Caixa de diálogo para solicitar a senha-mestra do usuário. 
    O método `open_dialog` aceita um callback `on_submit` que é chamado quando o usuário clica em "Verificar". 
    O método `return_password` pode ser usado para obter a senha inserida, e o campo é limpo após cada submissão ou cancelamento.
    """
    def __init__(self, page: ft.Page, pallete):
        self.master_password_field = ft.TextField(
            label=ft.Text("Insira a senha-mestra", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            password=True,
            can_reveal_password=True,
            autocorrect=False,
            enable_suggestions=False,
            on_submit=self.on_verify,
            border_color=pallete['primary_color'],
            height=45,
            expand=True,
        )
        super().__init__(
            title=ft.Text("Digite a senha-mestra", color=pallete['text_color']),
            bgcolor=pallete['secondary_color'],
            content=self.master_password_field,
            actions=[
                ft.ElevatedButton("Cancelar", color=pallete['primary_color'], bgcolor=pallete['secondary_color'], on_click=self.on_cancel, elevation=0),
                ft.ElevatedButton("Verificar", color=pallete['primary_color'], bgcolor=pallete['secondary_color'], on_click=self.on_verify, elevation=0),
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
    
    def on_verify(self, e=None):
        self.submitted = True
        self.close_dialog()
        if self.on_submit:
            self.on_submit()
    
    def return_password(self):
        print(f"senha-mestra inserida")
        senha_mestra = self.master_password_field.value
        self.master_password_field.value = ""
        return senha_mestra