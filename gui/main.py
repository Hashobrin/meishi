import flet as ft


def main(page: ft.Page):
    """
    main function
    """
    page.title = 'Meishi'

    page.window_width = 1000
    page.window_height = 500
    page.window_minimizable = True
    page.window_maximizable = True
    page.window_resizable = True
    page.bgcolor = ft.colors.GREEN
    page.window_opacity = 0.0

    page.update()


if __name__ == '__main__':
    ft.app(target=main)
