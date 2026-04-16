import flet as ft


class CustomNavRail(ft.Container):
    def __init__(
        self,
        destinations: list[dict],
        on_change=None,
        selected_index: int = 0,
        # Layout
        gap: int = 8,
        button_height: int = 48,        # altura fixa em px
        # Cores do botão
        bgcolor: str = "#AF1E23",
        bg_normal: str = "transparent",
        bg_hover: str = "#C42A30",
        bg_selected: str = "#831E23",
        text_color: str = ft.Colors.WHITE,
        icon_color: str = ft.Colors.WHITE,
        **kwargs,
    ):
        self.destinations = destinations
        self.on_change = on_change
        self.selected_index = selected_index
        self.gap = gap
        self.button_height = button_height
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self.bg_selected = bg_selected
        self.text_color = text_color
        self.icon_color = icon_color

        self._buttons: list[ft.Container] = []
        self._col = ft.Column(
            controls=[],
            spacing=gap,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        super().__init__(
            bgcolor=bgcolor,
            padding=ft.padding.symmetric(vertical=16, horizontal=0),
            content=self._col,
            **kwargs,
        )

        self._build_buttons()

    def _build_buttons(self):
        self._buttons.clear()
        for i, dest in enumerate(self.destinations):
            self._buttons.append(self._make_button(i, dest))
        self._col.controls = self._buttons

    def _make_button(self, index: int, dest: dict) -> ft.Container:
        is_selected = index == self.selected_index
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(dest["icon"], color=self.icon_color, size=20),
                    ft.Text(dest["label"], color=self.text_color, size=13, weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8,
            ),
            bgcolor=self.bg_selected if is_selected else self.bg_normal,
            border_radius=8,
            height=self.button_height,
            padding=ft.padding.symmetric(vertical=0, horizontal=16),
            margin=ft.margin.symmetric(horizontal=8),
            on_click=lambda e, i=index: self._handle_click(i),
            on_hover=lambda e, i=index: self._handle_hover(e, i),
        )

    def _handle_click(self, index: int):
        self.selected_index = index
        self._refresh_colors()
        if self.on_change:
            self.on_change(index)

    def _handle_hover(self, e, index: int):
        if index == self.selected_index:
            return
        self._buttons[index].bgcolor = self.bg_hover if e.data == "true" else self.bg_normal
        self._buttons[index].update()

    def _refresh_colors(self):
        for i, btn in enumerate(self._buttons):
            btn.bgcolor = self.bg_selected if i == self.selected_index else self.bg_normal
            btn.update()