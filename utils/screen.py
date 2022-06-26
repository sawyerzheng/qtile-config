import logging
import subprocess

from libqtile.lazy import lazy


def move_window_to_screen(qtile, window, screen):
    """Moves a window to a screen and focuses it, allowing you to move it
    further if you wish."""
    window.togroup(screen.group.name)
    qtile.focus_screen(screen.index)
    screen.group.focus(window, True)


@lazy.function
def move_window_to_prev_screen(qtile):
    """Moves a window to the previous screen. Loops around the beginning and
    end."""
    index = qtile.current_screen.index
    index = index - 1 if index > 0 else len(qtile.screens) - 1
    move_window_to_screen(qtile, qtile.current_window, qtile.screens[index])


@lazy.function
def move_window_to_next_screen(qtile):
    """Moves a window to the next screen. Loops around the beginning and
    end."""
    index = qtile.current_screen.index
    index = index + 1 if index < len(qtile.screens) - 1 else 0
    move_window_to_screen(qtile, qtile.current_window, qtile.screens[index])


def get_screen_count():
    try:
        from Xlib import X, display
        from Xlib.ext import randr
        from pprint import pprint

        d = display.Display()
        s = d.screen()
        r = s.root
        res = r.xrandr_get_screen_resources()._data

        # Dynamic multiscreen! (Thanks XRandr)
        num_screens = 0
        for output in res['outputs']:
            # print("Output %d:" % (output))
            mon = d.xrandr_get_output_info(output, res['config_timestamp'])._data
            # print("%s: %d" % (mon['name'], mon['num_preferred']))
            if mon['num_preferred']:
                num_screens += 1
        return num_screens
        # print("%d screens found!" % (num_screens))
    except Exception as e:
        logging.exception(e)
        return 1

def get_screen_resolution():
    output = subprocess.Popen('xrandr | grep "\\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    return {
        'width': int(resolution[0]),
        'height': int(resolution[1])
    }
