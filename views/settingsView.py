import flet as ft

def view():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Configurações")
            ],
            expand=True
        ),
        expand=True
    )