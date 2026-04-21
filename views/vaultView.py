import flet as ft
from views.view import View
from src.dialogs.enterMasterPassword import EnterMasterPasswordDialog
from src.dialogs.newPassword import NewPasswordDialog

class VaultView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        self.todas_contas = self.passwordhandler.list_sites()
        self.content = ft.ListView(expand=True)
        
        self.update_list(self.todas_contas)

        self.passworddialogue = EnterMasterPasswordDialog(self.page, self.theme)
        self.newpassworddialogue = NewPasswordDialog(self.page, self.theme)

    def search(self, e):
        termo = e.control.value.lower()
        filtradas = [c for c in self.todas_contas if termo in c["Site"].lower() or termo in c["User"].lower()]
        self.content.controls = [self.build_item(c) for c in filtradas]
        self.page.update()

    def update_list(self, contas=None):
        if contas is None:
            contas = self.passwordhandler.list_sites()
        self.todas_contas = contas
        self.content.controls = [self.build_item(c) for c in contas]
        self.page.update()
        print("aqui tem ", len(contas), " itens: ")

    def build_item(self, conta):
        password_button = ft.ElevatedButton(
            text="**********",
            color=self.theme['text_color'], 
            bgcolor=self.theme['secondary_color'],
            elevation=0,
            tooltip="Copiar senha",
        )
        password_button.on_click = lambda e: self.page.set_clipboard(password_button.text)

        def reveal_password():
            if self.passworddialogue.submitted:
                password = self.passwordhandler.decrypt_password(
                    self.passwordhandler.list_sites().index(conta),
                    self.passworddialogue.return_password()
                )
                print(password)
                if password == 0:
                    print("Senha-mestra incorreta!")
                    password_button.text = "**********"
                else:
                    password_button.text = password
                password_button.update()
                self.update_list(self.passwordhandler.list_sites())

        def toggle_password(e):
            print(f"Visualizando senha de {conta['Site']}")
            if self.passwordhandler.IS_MASTER_PASSWORD_VALID:
                self.passworddialogue.submitted = True
                reveal_password()
            else:
                self.passworddialogue.open_dialog(on_submit=reveal_password)
        
        def delete_password(e):
            self.passwordhandler.delete_password(self.passwordhandler.list_sites().index(conta))
            print(f"Conta de {conta['Site']} excluída.")
            self.update_list(self.passwordhandler.list_sites())

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
                    on_click=toggle_password, 
                    bgcolor=ft.Colors.TRANSPARENT,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_FOREVER,
                    icon_color=self.theme['primary_color'],
                    tooltip="Excluir senha",
                    on_click=lambda e: delete_password(conta),
                    bgcolor=ft.Colors.TRANSPARENT,
                )
            ]),
            padding=10,
            border_radius=10,
            margin=5,
        )

    def _on_password_added(self):
        contas = self.passwordhandler.list_sites()
        print("após adicionar, tem ", len(contas), " itens")
        self.update_list(contas)

    def add(self, e):
        print("antes tinham ", len(self.passwordhandler.list_sites()), " itens")
        self.newpassworddialogue.open_dialog(on_submit=self._on_password_added)

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
                                    bar_bgcolor=self.theme["app_bgcolor"],
                                    bar_hint_text_style=ft.TextStyle(color=self.theme['primary_color']),
                                    bar_text_style=ft.TextStyle(color=self.theme['secondary_color']),
                                    bar_border_side=ft.BorderSide(color=self.theme['primary_color'], width=1),
                                ),
                                ft.ElevatedButton(
                                    text="Nova senha",
                                    icon=ft.Icons.ADD,
                                    color=self.theme['secondary_color'],
                                    bgcolor=self.theme['primary_color'],
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