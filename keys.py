# -*- coding: utf-8; -*-

from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy


from utils import funcs, sizes, cmds
from utils.cmds import Commands

mod = "mod4"  # super key
mod1 = "mod1"
# mod = "mod1"                    # alt key
# mod = "mod3"
# "mod1"：Alt键（按键符号为"Mod1"）
# "mod2"：Num Lock键（按键符号为"Mod2"）
# "mod3"：Caps Lock键（按键符号为"Mod3"）
# "mod4"：Windows键（按键符号为"Mod4"）
# "mod5"：Scroll Lock键（按键符号为"Mod5"）


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key(
        [mod], "space", funcs.my_next_keyboard, desc="Move window focus to other window"
    ),
    Key([mod], "o", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "w", cmds.spawn("xkill"), desc="force to kill window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # spawn
    Key(
        [mod],
        "r",
        cmds.spawn(Commands.rofi()),
        desc="Spawn a command using a prompt widget",
    ),
    Key([mod], "p", cmds.spawn("/usr/bin/dmenu_run -l 15"), desc="dmenu"),
    # * applications
    # qtile lock
    Key([mod, "mod1"], "l", cmds.spawn(Commands.lockscreen()), desc="lock screen"),
    # power menu
    Key([mod, "mod1"], "p", cmds.spawn(Commands.powermenu()), desc="powermenu"),
    # terminal
    Key([mod], "Return", lazy.spawn(Commands.terminal()), desc="Launch terminal"),
    Key([mod, "control"], "t", lazy.spawn(Commands.terminal()), desc="Launch terminal"),
    # move window to screen: Mod + ctrl
    Key(
        [mod, "control"],
        "m",
        funcs.window_to_next_screen,
    ),
    Key(
        [mod, "control"],
        "period",
        funcs.window_to_previous_screen,
    ),
    Key(
        [mod, "control"],
        "o",
        funcs.window_switch_screen,
    ),
    # move window to left/right group(workspace)
    Key(
        [mod, "control"],
        "p",
        funcs.window_to_prev_group,
    ),
    Key(
        [mod, "control"],
        "n",
        funcs.window_to_next_group,
    ),
    Key(
        [mod, "control"],
        "Left",
        funcs.window_to_prev_group,
    ),
    Key(
        [mod, "control"],
        "Right",
        funcs.window_to_next_group,
    ),
    # switch focus group: mod + shift
    Key(
        [mod, "shift"],
        "o",
        # lazy.function(latest_group),
        lazy.screen.toggle_group(),
    ),
    Key(
        [mod, "shift"],
        "p",
        # lazy.screen.prev_group(skip_empty=True, skip_managed=True),
        funcs.goto_prev_group,
    ),
    Key(
        [mod, "shift"],
        "n",
        # lazy.screen.next_group(skip_empty=True, skip_managed=True),
        funcs.goto_next_group,
    ),
    Key(
        [mod, "shift"],
        "Left",
        funcs.goto_prev_group,
    ),
    Key(
        [mod, "shift"],
        "Right",
        funcs.goto_next_group,
    ),

    # focus: go next screen
    Key(
        [mod, "shift"],
        "comma",
        funcs.goto_next_screen,
    ),
    Key(
        [mod],
        "comma",
        funcs.goto_next_screen,
    ),


    # bar hide show
    Key([mod, "control"], "x", lazy.hide_show_bar()),
]


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "terminal",
                # "alacritty",
                Commands.kitty(),
                height=0.6,
                width=0.6,
                x=0.2,
                y=0.2,
                on_focus_lost_hide=True,
                opacity=0.85,
                warp_pointer=False,
            )
        ],
    )
)

keys.extend(
    [
        # mod1 -> alt key
        Key(
            [mod],
            "slash",
            lazy.group["scratchpad"].dropdown_toggle("terminal"),
        ),
    ]
)

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]
