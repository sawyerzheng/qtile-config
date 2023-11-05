# -*- coding: utf-8; -*-
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy

from . import cmds

next_keyboard_layout = "cn"

@lazy.function
def my_next_keyboard(qtile):
    # subprocess.run(shlex.split('/usr/bin/bash -c "echo $(date) >> /tmp/test.txt"'))
    global next_keyboard_layout
    if next_keyboard_layout == "us":
        cmds.call("/usr/bin/setxkbmap us")
        cmds.call("/usr/bin/ibus engine xkb:us::eng")
        next_keyboard_layout = "cn"
    else:
        cmds.call("/usr/bin/setxkbmap cn")
        cmds.call("/usr/bin/ibus engine rime")
        # ref: https://askubuntu.com/questions/779558/terminal-command-for-changing-ibus-keyboard-layout
        next_keyboard_layout = "us"

@lazy.function(switch_screen=True)
def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


@lazy.function(switch_screen=True)
def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

@lazy.function(switch_screen=True)
def window_switch_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    i += 1
    next_i = i % len(qtile.screens)

    group = qtile.screens[next_i].group.name
    qtile.current_window.togroup(group, switch_group=switch_group)
    if switch_screen == True:
        qtile.cmd_to_screen(next_i)


@lazy.function
def latest_group(qtile):
    """Switch focus between last and current group"""
    qtile.current_screen.set_group(qtile.current_screen.previous_group)

@lazy.function
def window_to_prev_group(qtile: Qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 0:
        qtile.current_window.togroup(qtile.groups[i - 1].name)
        qtile.current_screen.set_group(qtile.groups[i - 1])

@lazy.function
def window_to_next_group(qtile):
    i = qtile.groups.index(qtile.current_group)

    if qtile.current_window is not None and i < len(qtile.groups) - 1:
        qtile.current_window.togroup(qtile.groups[i + 1].name)
        qtile.current_screen.set_group(qtile.groups[i + 1])


@lazy.function
def goto_prev_group(qtile: Qtile):
    i = qtile.groups.index(qtile.current_group)
    if i != 0:
        qtile.current_screen.set_group(qtile.groups[i - 1])


@lazy.function
def goto_next_group(qtile):
    i = qtile.groups.index(qtile.current_group)

    if i < len(qtile.groups) - 1:
        qtile.current_screen.set_group(qtile.groups[i + 1])

@lazy.function(switch_screen=True)
def goto_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    i += 1
    next_i = i % len(qtile.screens)

    group = qtile.screens[next_i].group.name
    if switch_screen == True:
        qtile.cmd_to_screen(next_i)
