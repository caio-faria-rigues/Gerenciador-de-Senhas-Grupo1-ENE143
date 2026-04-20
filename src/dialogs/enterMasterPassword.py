import flet as ft

class EnterMasterPasswordDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, pallete):
        super().__init__(
            title=ft.Text("Digite a senha-mestra", color=pallete['text_color']),
            bgcolor=pallete['secondary_color'],
            content=ft.TextField(
                label=ft.Text("Insira a senha-mestra", color=pallete['primary_color']),
                bgcolor=pallete["app_bgcolor"],
                color=pallete['secondary_color'],
                password=True,
                can_reveal_password=True,
                border_color=pallete['primary_color'],
                on_submit=self._handle_master_password,
                height=45,
                expand=True,
                ),
            actions=[
                ft.ElevatedButton("Cancelar", color=pallete['primary_color'], bgcolor=pallete['secondary_color'], on_click=self.on_cancel, elevation=0),
                ft.ElevatedButton("Verificar", color=pallete['primary_color'], bgcolor=pallete['secondary_color'], on_click=self.on_verify, elevation=0),
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
    
    def on_verify(self, e):
        ##self.view.passwordhandler.set_master_password(self.password)
        self.close_dialog()

    def _handle_master_password(self, e):
        # Aqui você pode implementar a lógica para verificar a senha-mestra
        # Por exemplo, comparar com uma senha pré-definida ou verificar em um banco de dados
        pass