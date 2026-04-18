import flet as ft
from views.view import View

class VaultView(View):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        self.contas = [
            {"nome": "Google", "usuario": "fulano@gmail.com"},
            {"nome": "Facebook", "usuario": "fulano.fb"},
            {"nome": "GitHub", "usuario": "fulano@gmail.com"},
            {"nome": "Banco", "usuario": "fulano.banco@yahoo.com"},
            {"nome": "Twitter", "usuario": "fulaninhodetal058"},
            {"nome": "Steam", "usuario": "fulanoGames55"},
            {"nome": "Americanas", "usuario": "ful.ano@outlook.com"},
            {"nome": "SIGA", "usuario": "128937129873"},
            {"nome": "CEMIG", "usuario": "fulano@gmail.com"},
        ]
        self.content = ft.ListView(expand=True)
        self.update_list(self.contas)

    def search(self, e):
        termo = e.control.value.lower()

        filtradas = [c for c in self.contas if termo in c["nome"].lower() or termo in c["usuario"].lower()]
        self.update_list(filtradas)

    def update_list(self, contas):
        self.content.controls = [self.build_item(c) for c in contas]
        self.page.update()

    def build_item(self, conta):
        return ft.Container(
            content=ft.Row([
                ft.Column(
                    [
                        ft.Text(conta["nome"], weight=ft.FontWeight.BOLD),
                        ft.Text(conta["usuario"], size=12),
                    ],
                    expand=True
                ),
                ft.Icon(ft.Icons.LOCK),
            ]),
            padding=10,
            border_radius=10,
            margin=5,
        )

    def add(self, e):
        pass

    def render(self):
        return ft.Container(
            content=ft.Column(
                    [
                        ft.Text("Cofre de Senhas", size=30, weight=ft.FontWeight.BOLD),
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
