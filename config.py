import os
import copy
import shlex
import subprocess
from pathlib import Path

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.core.manager import Qtile
from libqtile.utils import guess_terminal

import widgets
from utils import funcs, sizes, cmds
from utils.cmds import Commands
from keys import keys, mouse, groups
from utils.sizes import Sizes
from utils.palette import palette

# * config by environment variables
QTILE_USE_POLYBAR = os.environ.get("QTILE_USE_POLYBAR", "True").strip().lower() in ["1", "true", "on"]

os.environ.update(cmds.my_set_env())


qtile_path = Path(__file__).parent.expanduser().absolute()

layout_config = config = {
    "border_focus": palette.teal,
    "border_normal": palette.base,
    "border_width": Sizes.window_border_width,
    "margin": Sizes.window_margin,
    "single_border_width": 0,
    "single_margin": Sizes.window_single_margin,
}

layouts = [
    layout.MonadTall(
        **layout_config,
        change_ratio=0.02,
        min_ratio=0.30,
        max_ratio=0.70,
    ),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], **layout_config),
    layout.Max(**layout_config),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(**layout_config),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=Sizes.widget_font_size,
    padding=Sizes.widget_default_padding,
)
extension_defaults = widget_defaults.copy()

if not QTILE_USE_POLYBAR:
    screens = widgets.MyWidgets().init_screen()
else:
    screens = [widgets.Screen()]


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def startup_once():
    subprocess.run(
        shlex.split(f'/usr/bin/bash {str(qtile_path.joinpath("autostart.sh"))}')
    )


@hook.subscribe.startup
def startup():
    # my_screen.bottom.show(True)
    # my_spawn("killall -9 polybar")
    wheight = sizes.Sizes.wheight
    if wheight > 2000:
        subprocess.run(
            shlex.split(f'/usr/bin/bash {str(qtile_path.joinpath("autostart_reload_4k.sh"))}')
        )
    else:
        subprocess.run(
            shlex.split(f'/usr/bin/bash {str(qtile_path.joinpath("autostart_reload.sh"))}')
        )
        # subprocess.call(shlex.split("/usr/bin/polybar -r mybar&"))

    # file = qtile_path.joinpath("autostart_reload_default.sh")
    # if file.exists():
    #     subprocess.run(
    #         shlex.split(f'/usr/bin/bash -c {file.as_posix()}')
    #     )
