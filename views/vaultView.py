import flet as ft
from views.view import View
from src.dialogs.enterMasterPassword import EnterMasterPasswordDialog
from src.dialogs.newPassword import NewPasswordDialog

class VaultView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        self.contas = self.passwordhandler.list_sites()
        print(self.contas)
        self.content = ft.ListView(expand=True)
        
        self.update_list(self.contas)

        self.passworddialogue = EnterMasterPasswordDialog(self.page, self.theme)
        self.newpassworddialogue = NewPasswordDialog(self.page, self.theme)

    def search(self, e):
        termo = e.control.value.lower()

        filtradas = [c for c in self.contas if termo in c["Site"].lower() or termo in c["User"].lower()]
        self.update_list(filtradas)
        print(self.content.controls)

    def update_list(self, contas):
        self.content.controls = [self.build_item(c) for c in contas]
        self.page.update()

    def build_item(self, conta):
        visible = False

        password_button = ft.ElevatedButton(
            text="**********",
            color=self.theme['text_color'], 
            bgcolor=self.theme['secondary_color'],
            elevation=0,
        )
        password_button.on_click = lambda e: self.page.set_clipboard(password_button.text)

        def toggle_password(e):
            nonlocal visible, conta

            print(f"Visualizando senha de {conta['Site']}")

            if self.passwordhandler.IS_MASTER_PASSWORD_VALID:
                print(f"Senha de {conta['Site']}: {conta['Senha']}")
            else:
                self.passworddialogue.open_dialog()
            #password_button.text = conta['Senha']
            visible = not visible

            password_button.text = conta["Senha"] if visible else "**********"
            password_button.update()

        return ft.Container(
            content=ft.Row([
                ft.Column(
                    [
                        ft.Text(conta["Site"], weight=ft.FontWeight.BOLD, color=self.theme['text_color']),
                        ft.Text(conta["User"], size=12, color=self.theme['text_color']),
                    ],
                    expand=True
                ),
                password_button,
                ft.IconButton(
                    icon=ft.Icons.LOCK,
                    icon_color=self.theme['primary_color'],
                    tooltip="Ver senha",
                    on_click=lambda e: toggle_password(conta), 
                    bgcolor=ft.Colors.TRANSPARENT,
                ),
            ]),
            padding=10,
            border_radius=10,
            margin=5,
        )

    def add(self, e):
        self.newpassworddialogue.open_dialog()
        self.update_list(self.passwordhandler.list_sites())
        print(self.content.controls)

    def render(self):
        return ft.Container(
            content=ft.Column(
                    [
                        ft.Text("Cofre de Senhas", size=30, weight=ft.FontWeight.BOLD, color=self.theme['text_color']),
                        ft.Row(
                            [
                                ft.SearchBar(
                                    bar_hint_text="Pesquisar cadastros...",
                                    on_change=self.search,
                                    expand=7,
                                    height=45,
                                ),
                                ft.ElevatedButton(
                                    text="Nova senha",
                                    icon=ft.Icons.ADD,
                                    bgcolor=ft.Colors.GREEN,
                                    on_click=self.add,
                                    expand=3,
                                    height=45,
                                )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        self.content,
                    ]
                ),
            expand=True,
            padding=20,
        )
