import flet as ft
from src import pallete
from app.masterPasswordHandler import MasterPasswordHandler

class View:
    def __init__(self, page):
        self.page = page
        self.passwordhandler = MasterPasswordHandler()
        self.theme = pallete.day_mode
        self.password = '**********'

        self.content = ft.Container(
            expand=True,
            padding=20,
            border_radius=10,

        )

    def render(self):
        return ft.Container()
