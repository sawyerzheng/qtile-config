import os
import shlex
import subprocess
from pathlib import Path

from libqtile.lazy import lazy

from .sizes import Sizes


def my_set_env():
    wheight = Sizes.wheight
    envs = os.environ.copy()

    # ibus
    envs["GTK_IM_MODULE"] = "ibus"
    envs["QT_IM_MODULE"] = "ibus"
    envs["XMODIFIERS"] = "@im=ibus"
    # locale
    envs["LANG"] = "zh_CN.UTF-8"
    envs["LANGUAGE"] = "zh_CN:en_US"

    if wheight > 2000:
        envs["GDK_DPI_SCALE"] = "1"
        envs["GDK_SCALE"] = "2"
    else:
        envs["GDK_DPI_SCALE"] = "1"
        envs["GDK_SCALE"] = "1"
    return envs


def spawn(cmd):
    @lazy.function
    def wrapper(*args, **kwargs):
        subprocess.call(shlex.split(cmd), env=my_set_env())

    return wrapper

def call(cmd):
    return subprocess.call(shlex.split(cmd), env=my_set_env())

class Commands:
    wheight = Sizes.wheight

    @classmethod
    def terminal(cls):
        return "alacritty"

    @classmethod
    def rofi(cls):
        if cls.wheight > 2000:
            cmd = "~/.config/rofi/launchers/type-7-4k/launcher.sh"
        else:
            cmd = "~/.config/rofi/launchers/type-7/launcher.sh"
        if Path(cmd).expanduser().exists():
            return "/usr/bin/bash " + str(Path(cmd).expanduser())
        return "/usr/bin/rofi -show combi"

    @classmethod
    def window_rofi(cls):
        if cls.wheight > 2000:
            cmd = "~/.config/rofi/launchers/type-7-4k/window.sh"
        else:
            cmd = "~/.config/rofi/launchers/type-7/window.sh"
        if Path(cmd).expanduser().exists():
            return "/usr/bin/bash " + str(Path(cmd).expanduser())
        return "/usr/bin/rofi -show window"

    @classmethod
    def select_mode_rofi(cls):
        if cls.wheight > 2000:
            cmd = "~/.config/rofi/launchers/type-7-4k/select.sh"
        else:
            cmd = "~/.config/rofi/launchers/type-7/select.sh"
        if Path(cmd).expanduser().exists():
            return "/usr/bin/bash " + str(Path(cmd).expanduser())
        return '/usr/bin/bash -c echo -e "window\nrun\ndrun\nssh" | rofi -dmenu | xargs -n1  -I {} rofi -show {}'

    @classmethod
    def powermenu(cls):
        if cls.wheight > 2000:
            return str(Path("~/.config/rofi/powermenu/type-1-4k/powermenu.sh").expanduser())
        else:
            return str(Path("~/.config/rofi/powermenu/type-1/powermenu.sh").expanduser())

    @classmethod
    def lockscreen(cls):
        return "betterlockscreen -l"

    @classmethod
    def kitty(cls):
        if cls.wheight > 2000:
            return "kitty -c " + str(Path("~/.config/kitty/kitty-4k.conf").expanduser().absolute())

        return "kitty"
