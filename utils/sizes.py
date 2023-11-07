def screen_size():
    # from tkinter import Tk
    # wheight = Tk().winfo_screenheight()
    try:
        import tkinter as tk

        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        wheight = screen_height
    except Exception:
        wheight = 2160
    return wheight


class Sizes:
    wheight = screen_size()

    # wheight == 1920:
    bar_size = 20
    widget_padding = 4
    widget_logo_padding = 20

    group_name_size = 10
    widget_font_size = 14
    widget_sep_size = 37
    widget_default_padding = 2

    # window arangement sizes
    window_border_width = 1
    window_margin = 8
    window_single_margin = 4

    if wheight > 2000:
        bar_size = 38
        widget_padding = 4
        widget_logo_padding = 20

        group_name_size = 28
        widget_font_size = 32
        widget_sep_size = 65
        widget_default_padding = 4

        # window arangement sizes
        window_border_width = 2
        window_margin = 20
        window_single_margin = 20
