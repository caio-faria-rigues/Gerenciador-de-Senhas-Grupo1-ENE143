import flet as ft

def view():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Home")
            ],
            expand=True
        ),
        expand=True
    )