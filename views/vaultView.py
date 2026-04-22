import flet as ft
from views.view import View
from src.dialogs.enterMasterPassword import EnterMasterPasswordDialog
from src.dialogs.newPassword import NewPasswordDialog

class VaultView(View):
    """
    View principal do cofre, onde as senhas são listadas e gerenciadas.
    Permite pesquisar, revelar, copiar e excluir senhas.
    """
    def __init__(self, page: ft.Page, password_handler):
        super().__init__(page, password_handler)

        self.todas_contas = self.passwordhandler.list_sites()
        self.content = ft.ListView(expand=True)
        
        self.update_list(self.todas_contas)

        self.passworddialogue = EnterMasterPasswordDialog(self.page, self.theme)
        self.newpassworddialogue = NewPasswordDialog(self.page, self.theme, self.passwordhandler)
    
    def _find_index(self, conta):
        for i, c in enumerate(self.passwordhandler.list_sites()):
            if c["Site"] == conta["Site"] and c["User"] == conta["User"]:
                return i
        return None

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
        estado = {"senha_revelada": None}

        password_button = ft.ElevatedButton(
            text="**********",
            color=self.theme['text_color'], 
            bgcolor=self.theme['secondary_color'],
            elevation=0,
            tooltip="Clique para copiar",
        )

        def on_password_click(e):
            if estado["senha_revelada"] is not None:
                self.page.set_clipboard(estado["senha_revelada"])
                estado["senha_revelada"] = None
                password_button.text = "**********"
                password_button.update()

        password_button.on_click = on_password_click

        def reveal_password():
            if self.passworddialogue.submitted:
                indice = self._find_index(conta)
                if indice is None:
                    print("Entrada não encontrada no cofre.")
                    return

                password = self.passwordhandler.decrypt_password(
                    indice,
                    self.passworddialogue.return_password()
                )
                if password == 0:
                    self.page.open(ft.SnackBar(content=ft.Text("Senha-mestra incorreta!", color=self.theme['secondary_color']),bgcolor=self.theme['primary_color']))
                    print("Senha-mestra incorreta!")
                    estado["senha_revelada"] = None
                    password_button.text = "**********"
                else:
                    estado["senha_revelada"] = password
                    password_button.text = password
                password_button.update()

        def toggle_password(e):
            if estado["senha_revelada"] is not None:
                estado["senha_revelada"] = None
                password_button.text = "**********"
                password_button.update()
                return

            if self.passwordhandler.IS_MASTER_PASSWORD_VALID:
                self.passworddialogue.submitted = True
                reveal_password()
            else:
                self.passworddialogue.open_dialog(on_submit=reveal_password)

        def delete_password(e):
            indice = self._find_index(conta)
            if indice is not None:
                self.passwordhandler.delete_password(indice)
                self.page.open(ft.SnackBar(content=ft.Text(f"Conta de {conta['Site']} excluída.", color=self.theme['secondary_color']),bgcolor=self.theme['primary_color']))
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
                    on_click=delete_password,
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