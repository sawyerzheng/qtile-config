import os
from libqtile import bar, init, widget
from libqtile.lazy import lazy
from libqtile.config import Screen
from libqtile.backend.base import drawer

from utils import cmds
from utils.sizes import Sizes
from utils.palette import palette


def framed(self, border_width, border_color, pad_x, pad_y, highlight_color=None):
    return TextFrame(
        self, border_width, border_color, pad_x, pad_y, highlight_color=highlight_color
    )


class TextFrame(drawer.TextFrame):
    def __init__(
        self, layout, border_width, border_color, pad_x, pad_y, highlight_color=None
    ):
        super().__init__(
            layout, border_width, border_color, pad_x, pad_y, highlight_color
        )

    def draw(
        self, x, y, rounded=True, fill=False, line=False, highlight=False, invert=False
    ):
        self.drawer.set_source_rgb(self.border_color)
        opts = [
            x,
            y,
            self.layout.width + self.pad_left + self.pad_right,
            self.layout.height + self.pad_top + self.pad_bottom,
            self.border_width,
        ]
        if line:
            if highlight:
                self.drawer.set_source_rgb(self.highlight_color)
                self.drawer.fillrect(*opts)
                self.drawer.set_source_rgb(self.border_color)

            opts[1] = 0 if invert else self.height - self.border_width
            opts[3] = self.border_width

            self.drawer.fillrect(*opts)
        elif fill:
            if rounded:
                self.drawer.rounded_fillrect(*opts)
            else:
                self.drawer.fillrect(*opts)
        else:
            if rounded:
                self.drawer.rounded_rectangle(*opts)
            else:
                self.drawer.rectangle(*opts)
        self.drawer.ctx.stroke()
        self.layout.draw(x + self.pad_left, y + self.pad_top)

    def draw_line(self, x, y, highlighted, inverted):
        self.draw(x, y, line=True, highlight=highlighted, invert=inverted)


class GroupBox(widget.groupbox.GroupBox):
    defaults = [
        (
            "invert",
            False,
            "Invert line position when 'line' highlight method isn't highlighted.",
        ),
        (
            "rainbow",
            False,
            "If set to True, 'colors' will be used instead of '*_screen_border'.",
        ),
        (
            "colors",
            False,
            "Receive a list of strings."
            "Allows each label to have its own independent/unique color when selected, overriding the 'active' parameter.",
        ),
        (
            "icons",
            {
                "active": "",
                "empty": "○",
                "occupied": "◉",
            },
            "Will be used in the 'icon' highlight method.",
        ),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(GroupBox.defaults)

    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)
        self.layout.framed = framed.__get__(self.layout)

    def drawbox(
        self,
        offset,
        text,
        bordercolor,
        textcolor,
        highlight_color=None,
        width=None,
        rounded=False,
        block=False,
        line=False,
        highlighted=False,
        inverted=False,
    ):
        self.layout.text = self.fmt.format(text)
        self.layout.font_family = self.font
        self.layout.font_size = self.fontsize
        self.layout.colour = textcolor
        if width is not None:
            self.layout.width = width
        if line:
            pad_y = [
                (self.bar.height - self.layout.height - self.borderwidth) / 2,
                (self.bar.height - self.layout.height + self.borderwidth) / 2,
            ]
            if highlighted:
                inverted = False
        else:
            pad_y = self.padding_y

        if bordercolor is None:
            # border colour is set to None when we don't want to draw a border at all
            # Rather than dealing with alpha blending issues, we just set border width
            # to 0.
            border_width = 0
            framecolor = self.background or self.bar.background
        else:
            border_width = self.borderwidth
            framecolor = bordercolor

        framed = self.layout.framed(border_width, framecolor, 0, pad_y, highlight_color)
        y = self.margin_y
        if self.center_aligned:
            for t in widget.base.MarginMixin.defaults:
                if t[0] == "margin":
                    y += (self.bar.height - framed.height) / 2 - t[1]
                    break
        if block and bordercolor is not None:
            framed.draw_fill(offset, y, rounded)
        elif line:
            framed.draw_line(offset, y, highlighted, inverted)
        else:
            framed.draw(offset, y, rounded)

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        def color(index: int) -> str:
            try:
                return self.colors[index]
            except IndexError:
                return "FFFFFF"

        offset = self.margin_x
        for i, g in enumerate(self.groups):
            is_block = self.highlight_method == "block"
            is_line = self.highlight_method == "line"
            is_icon = self.highlight_method == "icon"
            to_highlight = False

            bw = self.box_width([g])

            if self.group_has_urgent(g) and self.urgent_alert_method == "text":
                text_color = self.urgent_text
            elif g.windows:
                text_color = color(i) if self.colors else self.active
                icon = self.icons["occupied"]
            else:
                text_color = self.inactive
                icon = self.icons["empty"]

            if g.screen:
                if self.highlight_method == "text":
                    border = None
                    text_color = self.this_current_screen_border
                elif is_icon:
                    icon = self.icons["active"]
                    border = None
                    text_color = (
                        color(i) if self.colors else self.this_current_screen_border
                    )
                else:
                    if self.block_highlight_text_color:
                        text_color = self.block_highlight_text_color

                    if self.bar.screen.group.name == g.name:
                        if self.qtile.current_screen == self.bar.screen:
                            if self.rainbow and self.colors:
                                border = color(i) if g.windows else self.inactive
                            else:
                                border = self.this_current_screen_border
                            to_highlight = True
                        else:
                            if self.rainbow and self.colors:
                                border = color(i) if g.windows else self.inactive
                            else:
                                border = self.this_screen_border
                            to_highlight = True

                    else:
                        if self.qtile.current_screen == g.screen:
                            if self.rainbow and self.colors:
                                border = color(i) if g.windows else self.inactive
                            else:
                                border = self.other_current_screen_border
                        else:
                            if self.rainbow and self.colors:
                                border = color(i) if g.windows else self.inactive
                            else:
                                border = self.other_screen_border

            elif self.group_has_urgent(g) and self.urgent_alert_method in (
                "border",
                "block",
                "line",
            ):
                border = self.urgent_border
                if self.urgent_alert_method == "block":
                    is_block = True
                elif self.urgent_alert_method == "line":
                    is_line = True
            else:
                border = None

            self.drawbox(
                offset,
                icon if is_icon else g.label,
                border,
                text_color,
                highlight_color=self.highlight_color,
                width=bw,
                rounded=self.rounded,
                block=is_block,
                line=is_line,
                highlighted=to_highlight,
                inverted=self.invert,
            )
            offset += bw + self.spacing
        self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.width)


class MyWidgets:
    def __init__(self):
        self.colors = [
            ["#292d3e", "#292d3e"],  # panel background
            # background for current screen tab
            ["#434758", "#434758"],
            ["#ffffff", "#ffffff"],  # font color for group names
            # border line color for current tab
            ["#bc13fe", "#bc13fe"],  # Group down color
            # border line color for other tab and odd widgets
            ["#8d62a9", "#8d62a9"],
            ["#668bd7", "#668bd7"],  # color for the even widgets
            ["#e1acff", "#e1acff"],  # window name
            ["#000000", "#000000"],
            ["#AD343E", "#AD343E"],
            ["#f76e5c", "#f76e5c"],
            ["#F39C12", "#F39C12"],
            ["#F7DC6F", "#F7DC6F"],
            ["#f1ffff", "#f1ffff"],
            ["#4c566a", "#4c566a"],
        ]

        self.termite = "alacritty"

    def init_widgets_list_simple(self):
        """
        Function that returns the desired widgets in form of list
        """
        widgets_list = [
            widget.Sep(
                linewidth=0,
                padding=6,
                foreground=self.colors[2],
                background=self.colors[0],
            ),
            widget.Image(
                filename="~/.config/qtile/icons/terminal-iconx14.png",
                mouse_callbacks={
                    "Button1": lambda: cmds.call('dmenu_run -l 15 -p "Run: "')
                },
            ),
            widget.Sep(
                linewidth=0,
                padding=5,
                foreground=self.colors[2],
                background=self.colors[0],
            ),
            widget.GroupBox(
                font="Ubuntu Bold",
                fontsize=Sizes.group_name_size,
                margin_y=2,
                margin_x=0,
                padding_y=5,
                padding_x=3,
                borderwidth=3,
                active=self.colors[-2],
                inactive=self.colors[-1],
                # rounded=True,
                rounded=False,
                # highlight_color=self.colors[9],
                # highlight_method="line",
                highlight_method="block",
                urgent_alert_method="block",
                # urgent_border=self.colors[9],
                this_current_screen_border=self.colors[9],
                this_screen_border=self.colors[4],
                other_current_screen_border=self.colors[0],
                other_screen_border=self.colors[0],
                foreground=self.colors[2],
                background=self.colors[0],
                disable_drag=True,
            ),
            widget.Prompt(
                prompt=lazy.spawncmd(),
                font="Ubuntu Mono",
                padding=10,
                foreground=self.colors[3],
                background=self.colors[1],
            ),
            widget.Sep(
                linewidth=0,
                padding=40,
                foreground=self.colors[2],
                background=self.colors[0],
            ),
            widget.WindowName(
                foreground=self.colors[6], background=self.colors[0], padding=0
            ),
            widget.Systray(background=self.colors[0], padding=5),
            widget.TextBox(
                text="",
                background=self.colors[0],
                foreground=self.colors[11],
                padding=0,
                fontsize=Sizes.widget_sep_size,
            ),
            widget.TextBox(
                text=" 🖬",
                foreground=self.colors[7],
                background=self.colors[11],
                padding=0,
                # fontsize=14,
            ),
            widget.Memory(
                foreground=self.colors[7],
                background=self.colors[11],
                mouse_callbacks={
                    "Button1": lambda qtile: qtile.cmd_spawn(self.termite + " -e htop")
                },
                padding=50,
            ),
            widget.TextBox(
                text="",
                background=self.colors[11],
                foreground=self.colors[10],
                padding=0,
                fontsize=Sizes.widget_sep_size,
            ),
            widget.TextBox(
                text="  ",
                foreground=self.colors[7],
                background=self.colors[10],
                padding=0,
                mouse_callbacks={
                    "Button1": lambda qtile: qtile.cmd_spawn("pavucontrol")
                },
            ),
            widget.Volume(
                foreground=self.colors[7], background=self.colors[10], padding=5
            ),
            widget.TextBox(
                text="",
                background=self.colors[10],
                foreground=self.colors[9],
                padding=0,
                fontsize=Sizes.widget_sep_size,
            ),
            widget.CurrentLayoutIcon(
                custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                foreground=self.colors[0],
                background=self.colors[9],
                padding=0,
                scale=0.7,
            ),
            widget.CurrentLayout(
                foreground=self.colors[7], background=self.colors[9], padding=5
            ),
            widget.TextBox(
                text="",
                foreground=self.colors[8],
                background=self.colors[9],
                padding=0,
                fontsize=Sizes.widget_sep_size,
            ),
            widget.Clock(
                foreground=self.colors[7],
                background=self.colors[8],
                mouse_callbacks={
                    "Button1": lambda qtile: qtile.cmd_spawn("/usr/bin/kitty")
                },
                format="%B %d  [ %H:%M ]",
            ),
            widget.Sep(
                linewidth=0,
                padding=10,
                foreground=self.colors[0],
                background=self.colors[8],
            ),
        ]
        return widgets_list

    def init_widgets_list_fancy(self):
        # return self.init_widgets_list_simple()
        from qtile_extras import widget as widget_extra
        from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

        def powerline(path: str | list[tuple] = "arrow_right", size=10):
            return {
                "decorations": [
                    PowerLineDecoration(
                        path=path,
                        size=size,
                    ),
                ]
            }

        def rectangle(side=""):
            return {
                "decorations": [
                    RectDecoration(
                        filled=True,
                        radius={"left": [8, 0, 0, 8], "right": [0, 8, 8, 0]}.get(
                            side, 8
                        ),
                        use_widget_background=True,
                    ),
                ]
            }

        spacer_len = 1

        def make_spacer(length=spacer_len):
            return widget.Spacer(length=length)

        def color(bg: str | None, fg: str | None) -> dict:
            return {"background": bg, "foreground": fg}

        def font():
            return {
                "font": "Symbols Nerd Font Mono Regular",
                "fontsize": Sizes.widget_font_size,
            }

        def sep(fg, offset=0, padding=10):
            return widget.textbox.TextBox(
                **color(None, fg),
                **font(),
                offset=offset,
                padding=padding,
                text="󰇙",
            )

        return [
            make_spacer(),
            widget_extra.TextBox(
                padding=Sizes.widget_logo_padding,
                text="",
                mouse_callbacks={"Button1": lazy.restart()},
                **color(bg=palette.blue, fg=palette.base),
                **rectangle(),
                **font(),
            ),
            sep(fg=palette.surface2, padding=Sizes.widget_padding),
            GroupBox(
                **font(),
                colors=[
                    palette.teal,
                    palette.pink,
                    palette.yellow,
                    palette.red,
                    palette.blue,
                    palette.green,
                ],
                highlight_color=palette.base,
                highlight_method="line",
                inactive=palette.surface2,
                invert=True,
                padding=6,
                rainbow=True,
            ),
            sep(palette.surface2, offset=20, padding=0),
            make_spacer(10),
            widget_extra.TextBox(
                **color(palette.pink, palette.base),
                **font(),
                **rectangle("left"),
                offset=10,
                padding=20,
                text="",
                x=-2,
            ),
            widget_extra.Volume(
                **color(palette.pink, palette.base),
                **powerline("arrow_left", size=10),
                # check_mute_command="pamixer --get-mute",
                # check_mute_string="true",
                # get_volume_command="pamixer --get-volume-human",
                # mute_command="pamixer --toggle-mute",
                # update_interval=0.1,
                # volume_down_command="pamixer --decrease 5",
                # volume_up_command="pamixer --increase 5",
            ),
            # widget.Spacer(
            #     linewidth=0,
            #     padding=0,
            #     **color(palette.red, palette.base),
            # ),
            widget_extra.TextBox(
                **color(palette.red, palette.base),
                **font(),
                offset=-1,
                text="",
                x=-2,
                padding=10,
            ),
            widget_extra.CheckUpdates(
                distro="Arch",
                **color(palette.red, palette.base),
                **rectangle("right"),
                # colour_have_updates=palette.red,
                # colour_no_updates=palette.red,
                # custom_command="checkupdates",
                # display_format="{updates} updates  ",
                display_format="{updates} ",
                initial_text="0 ",
                no_update_string="No updates  ",
                padding=5,
                update_interval=5,
                offset=-5,
                x=-5,
            ),
            widget.Spacer(),
            # * window name
            widget_extra.WindowName(
                **color(None, palette.text),
                format="{name}",
                # max_chars=60,
                # width=CALCULATED,
            ),
            widget.Spacer(),
            # * cpu
            widget_extra.TextBox(
                **color(palette.green, palette.base),
                **font(),
                **rectangle("left"),
                offset=-13,
                padding=15,
                text="󰍛",
            ),
            widget_extra.CPU(
                **color(palette.green, palette.base),
                **powerline("arrow_right"),
                format="{load_percent:.0f}%",
            ),
            # * RAM
            widget_extra.TextBox(
                **color(palette.yellow, palette.base),
                **font(),
                offset=-1,
                padding=5,
                text="󰘚",
            ),
            widget_extra.Memory(
                **color(palette.yellow, palette.base),
                **powerline("arrow_right"),
                format="{MemUsed: ,.0f}{mm} ",
                padding=-3,
            ),
            # * DISK
            widget_extra.TextBox(
                **color(palette.teal, palette.base),
                **font(),
                offset=-1,
                text="",
                x=-2,
            ),
            widget_extra.DF(
                **color(palette.teal, palette.base),
                **rectangle("right"),
                format="{f} GB  ",
                padding=0,
                partition="/",
                visible_on_warn=False,
                warn_color=palette.teal,
            ),
            sep(palette.surface2, offset=20, padding=10),
            make_spacer(),
            # * Time
            widget_extra.TextBox(
                **color(palette.pink, palette.base),
                **font(),
                **rectangle("left"),
                offset=-14,
                padding=15,
                text="",
            ),
            widget_extra.Clock(
                **color(palette.pink, palette.base),
                **rectangle("right"),
                format="%A - %I:%M %p ",
                long_format="%B %-d, %Y ",
                padding=7,
            ),
            make_spacer(),
            # widget.QuickExit(background="666666"),
            # make_spacer(),
        ]

    def init_widgets_list(self):
        return self.init_widgets_list_fancy()

    def init_widgets_screen(self):
        """
        Function that returns the widgets in a list.
        It can be modified so it is useful if you  have a multimonitor system
        """
        widgets_screen = self.init_widgets_list()
        return widgets_screen

    def init_widgets_screen2(self):
        """
        Function that returns the widgets in a list.
        It can be modified so it is useful if you  have a multimonitor system
        """
        widgets_screen2 = self.init_widgets_screen()
        widgets_screen2 = [
            i for i in widgets_screen2 if not isinstance(i, widget.Systray)
        ]
        return widgets_screen2

    def init_screen(self):
        """
        Init the widgets in the screen
        """
        return [
            Screen(
                top=bar.Bar(
                    widgets=self.init_widgets_screen(), opacity=1.0, size=Sizes.bar_size
                )
            ),
            Screen(
                top=bar.Bar(
                    widgets=self.init_widgets_screen2(),
                    opacity=1.0,
                    size=Sizes.bar_size,
                )
            ),
        ]
