import flet as ft

class EnterMasterPasswordDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, pallete):
        self.master_password_field = ft.TextField(
            label=ft.Text("Insira a senha-mestra", color=pallete['primary_color']),
            bgcolor=pallete["app_bgcolor"],
            color=pallete['secondary_color'],
            password=True,
            can_reveal_password=True,
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
        self.page.overlay.append(self)

    def open_dialog(self):
        self.submitted = False
        self.open = True
        self.page.update()

    def close_dialog(self):
        self.open = False
        self.page.update()
    
    def on_cancel(self, e=None):
        self.close_dialog()
    
    def on_verify(self, e=None):
        self.close_dialog()
        self.submitted = True
    
    def return_password(self):
        print(f"senha-mestra inserida:({self.master_password_field.value})")
        return self.master_password_field.value
        