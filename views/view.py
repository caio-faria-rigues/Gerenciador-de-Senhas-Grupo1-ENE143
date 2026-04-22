import flet as ft
from src import pallete
from app.masterPasswordHandler import MasterPasswordHandler

class View:
    """
    Classe base para gerenciar informações comuns entre as telas, como o handler da senha mestra e o tema.
    """
    def __init__(self, page, password_handler):
        self.page = page
        self.passwordhandler = password_handler
        self.theme = pallete.day_mode
        self.password = '**********'

        self.content = ft.Container(
            expand=True,
            padding=20,
            border_radius=10,

        )

    def render(self):
        return ft.Container()
