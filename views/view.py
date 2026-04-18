import flet as ft

class View:
    def __init__(self, page):
        self.page = page

        self.content = ft.Container(
            expand=True,
            padding=20,
            border_radius=10,

        )

    def render(self):
        return ft.Container()
