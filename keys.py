# -*- coding: utf-8; -*-

from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy


from utils import funcs, sizes, cmds
from utils.cmds import Commands

win = "mod4"  # super key
alt = "mod1"
# "mod1"：Alt键（按键符号为"Mod1"）
# "mod2"：Num Lock键（按键符号为"Mod2"）
# "mod3"：Caps Lock键（按键符号为"Mod3"）
# "mod4"：Windows键（按键符号为"Mod4"）
# "mod5"：Scroll Lock键（按键符号为"Mod5"）


# * kyes
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # fmt: off

# ** 输入法 input method toggle

    # Toggle between different layouts as defined below
    Key([win], "Tab", lazy.next_layout(), desc="Toggle between layouts"),


# ** layout

# *** change layout method
    Key([win], "space", funcs.my_next_keyboard, desc="Move window focus to other window"),


# *** vertial vs horizontal layout
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([win, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),


# ** windows

# *** window focus
    Key([win], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([win], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([win], "j", lazy.layout.down(), desc="Move focus down"),
    Key([win], "k", lazy.layout.up(), desc="Move focus up"),

    Key([win, alt], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([win, alt], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([win, alt], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([win, alt], "Up", lazy.layout.up(), desc="Move focus up"),



# *** switch window no direction
    Key([win], "o", lazy.layout.next(), desc="Move window focus to other window"),
    Key([alt], "Tab", cmds.spawn(Commands.window_rofi()), desc="Move window focus to other window"),
    # Key([alt], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Key([alt, "shift"], "Tab", lazy.layout.previous(), desc="Move window focus to other window"),


# *** move window
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([win, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([win, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([win, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([win, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

# *** resize window
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([win, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([win, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([win, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([win, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([win], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([win], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([win, "shift"], "w", cmds.spawn("xkill"), desc="force to kill window"),
    Key([win], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([win], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([win, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([win, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

# ** spawn
    Key([win], "r", cmds.spawn(Commands.rofi()), desc="Spawn a command using a prompt widget"),

    Key([win, "shift"], "r", cmds.spawn(Commands.select_mode_rofi()), desc="Spawn a command using a prompt widget"),
    Key([win], "p", cmds.spawn("/usr/bin/dmenu_run -l 15"), desc="dmenu"),

# ** applications
    # qtile lock
    Key([win, alt], "l", cmds.spawn(Commands.lockscreen()), desc="lock screen"),
    # power menu
    Key([win, alt], "p", cmds.spawn(Commands.powermenu()), desc="powermenu"),
    # terminal
    Key([win], "Return", lazy.spawn(Commands.terminal()), desc="Launch terminal"),
    Key([win, "control"], "t", lazy.spawn(Commands.terminal()), desc="Launch terminal"),

# ** group
# *** switch focus group: mod + ctrol
    Key([win, "control"], "o", lazy.screen.toggle_group()),
    Key([win, "control"], "p", funcs.goto_prev_group),
    Key([win, "control"], "n", funcs.goto_next_group),
    Key([win, "control"], "Left", funcs.goto_prev_group),
    Key([win, "control"], "Right", funcs.goto_next_group),

# *** group move window to left/right group(workspace)
    Key([win, "shift"], "p", funcs.window_to_prev_group),
    Key([win, "shift"], "n", funcs.window_to_next_group),
    Key([win, "control", "shift"], "Left", funcs.window_to_prev_group),
    Key([win, "control", "shift"], "Right", funcs.window_to_prev_group),


# ** screen
# *** screen toggle, focus: go next screen
    Key([win, "control"], "comma", funcs.goto_next_screen),
    Key([win], "comma", funcs.goto_next_screen),

# *** screen, move window to screen: Mod + shift, shift -> move
    Key([win, "shift"], "m", funcs.window_to_next_screen),
    Key([win, "shift"], "period", funcs.window_to_previous_screen),
    Key([win, "shift"], "o", funcs.window_switch_screen),
    Key([win, "shift"], "Left", funcs.window_to_previous_screen),
    Key([win, "shift"], "Right", funcs.window_to_next_screen),



# ** bar hide show
    Key([win, "control"], "x", lazy.hide_show_bar()),
    # fmt: on
]

# * groups
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [win],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [win, "shift"],
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
            [win],
            "slash",
            lazy.group["scratchpad"].dropdown_toggle("terminal"),
        ),
    ]
)

# Drag floating layouts.
mouse = [
    Drag(
        [win],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [win],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([win], "Button2", lazy.window.bring_to_front()),
]
