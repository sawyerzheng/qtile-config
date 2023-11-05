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

    if wheight > 2000:
        bar_size = 38
        group_name_size = 28
        font_size = 32
        padding = 4
        sep_size = 65

        window_border_width = 4

        # window arangement sizes
        window_margin = 20 
        window_single_margin = 20

    else:  # wheight == 1920:
        bar_size = 20
        group_name_size = 10
        font_size = 14
        sep_size = 37
        padding = 2
        window_border_width = 4

        # window arangement sizes
        margin = 10
        single_margin = 10
