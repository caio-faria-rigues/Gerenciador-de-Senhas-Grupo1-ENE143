import flet as ft
from src import pallete
from views import homeView, vaultView, settingsView
from src.widgets.customNav import CustomNavRail

class App:
    def __init__(self, page: ft.Page):
        self.page = page

        self.page.title = "App"
        self.page.window.resizable = True
        self.page.window.maximizable = True
        self.page.window.min_width = 900
        self.page.window.min_height = 450
        self.page.expand = True
        #self.page.bgcolor = ft.Colors.GREY_200
        self.page.bgcolor = '#BEBEBE'

        self.content = ft.Container(
            expand=80,
            bgcolor=ft.Colors.WHITE,
            padding=20,
            )

        self.navbar = CustomNavRail(
            expand=20,
            destinations=[
                {"label": "Home",          "icon": ft.Icons.HOME},
                {"label": "Cofre",         "icon": ft.Icons.LOCK},
                {"label": "Configurações", "icon": ft.Icons.SETTINGS},
            ],
            on_change=self.change_view,
            selected_index=0,
            gap=8,
            bgcolor="#AF1E23",
            bg_normal="transparent",
            bg_hover="#C42A30",
            bg_selected="#831E23",
        )

        self.page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                self.navbar,
                                ft.Divider(),
                                ft.Text("ENE143 - Grupo 1"),
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.LINK),
                                            ft.Text("Repositório")
                                        ],
                                        spacing=0
                                    ),
                                    on_click=lambda e: page.launch_url("https://github.com/caio-faria-rigues/Gerenciador-de-Senhas-Grupo1-ENE143"),
                                    ink=True
                                )
                            ],
                            spacing=0
                        ),
                        self.content,
                    ],
                    expand=True,
                    spacing=0,
                ),
                expand=True,
                border_radius=10,
            )
        )
        def on_window_event(e):
            print(e.type)
            print(f"width={self.page.window.width:.0f}  height={self.page.window.height:.0f}")
        self.page.window.on_event = on_window_event

        self.change_view(0)

    def change_view(self, index: int):
        if index == 0:
            self.content.content = homeView.view()
        elif index == 1:
            self.content.content = vaultView.view()
        elif index == 2:
            self.content.content = settingsView.view()
        self.page.update()