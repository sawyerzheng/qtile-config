import os

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

try:
    env_wheight = int(os.environ.get("QTILE_WINDOW_HEIGHT"))
except Exception:
    env_wheight = screen_size()


class Sizes:
    wheight = env_wheight
    # * 1920x1080
    # ** window arangement sizes
    window_border_width = 1
    window_margin = 8
    window_single_margin = 4

    # ** widgets
    # wheight == 1920:
    bar_size = 20
    group_name_size = 10

    widget_padding = 4
    widget_logo_padding = 20
    widget_sep_padding = 5

    widget_font_size = 14
    widget_sep_size = 37
    widget_default_padding = 2
    widget_icon_padding = 15
    widget_icon_text_padding = 5
    # for check update
    widget_icon_update_padding = 10
    widget_icon_text_update_padding = 10
    widget_icon_text_ram_padding = -3
    widget_spacer_len = int(window_single_margin*1.5)
    # for clock
    widget_icon_clock_padding = 5


    powerline_size = 10
    rectangle_parameter = 8

    # * 4k screen
    if wheight > 2000:
        
        # ** window arangement sizes
        window_border_width = 2
        window_margin = 20
        window_single_margin = 20

        # ** widgets
        bar_size = 38
        group_name_size = 28
        widget_padding = 4
        widget_logo_padding = 25
        widget_icon_padding = 15
        widget_icon_text_padding = 10
        widget_sep_padding = 10
        # for check update
        widget_icon_update_padding = 15
        widget_icon_text_update_padding = 10
        widget_icon_text_ram_padding = -3
        widget_spacer_len = int(window_single_margin*1.5)
        # for clock
        widget_icon_clock_padding = 10

        widget_font_size = 32
        widget_sep_size = 65
        widget_default_padding = 4

        powerline_size = 20
        rectangle_parameter = 20

