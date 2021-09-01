# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"                             # My terminal of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([], "Print",
        lazy.spawn("scrot 'screenshot_%Y%m%d_%H%M%S.png' -e 'mkdir -p ~/Pictures/screenshots && mv $f ~/Pictures/screenshots && xclip -selection clipboard -t image/png >-i ~/Pictures/screenshots/`ls -1 -t ~/Pictures/screenshots | head -1`' # All screens"),
    desc='screenshot leta hai'
        ),
        Key(["shift"], "Print",
            lazy.spawn("scrot -s 'screenshot_%Y%m%d_%H%M%S.png' -e 'mkdir -p ~/Pictures/screenshots && mv $f ~/Pictures/screenshots && xclip -selection clipboard -t image/png -i ~/Pictures/screenshots/`ls -1 -t ~/Pictures/screenshots | head -1`' # Area selection"),
            desc='border wala screenshot bro'
            ),
        Key([mod], "p",
            lazy.spawn("/home/demus/.config/scripts/lock")
            ),
         Key([mod], "d",
             lazy.spawn("dmenu_run -p 'Run: '"),
             desc='Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "e",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Treetab controls
          Key([mod, "shift"], "h",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         ]

group_names = [("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ]
groups = [
    Group("", matches=[Match(wm_class=["Evince"])]),
    Group("", matches=[Match(wm_class=["Brave-browser"])]),
    Group("", matches=[Match(wm_class=["discord"])]),
    Group("", matches=[Match(wm_class=["Spotify"])]),
    Group("", matches=[Match(wm_class=["Alacritty"])]),
    Group("", matches=[Match(wm_class=["firefox"])]),
    Group("", matches=[Match(wm_class=["Virtualbox"])]),
    ]


for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {"border_width": 2,
                "border_focus": "#e1acff",
                "border_normal": "#FFE6E6",
                "margin": 8
                }
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Floating(**layout_theme)
]

colors = [["#282a36", "#282a36"], # panel background
          ["#FFB86C", "#FFB86C"], # Underline boi
          ["#bd93f9", "#bd93f9"], # color for the clock and battery
          ["#F3F1F5", "#F3F1F5"], # Group foreground
          ["#FFC947", "#FFC947"], # Color for Updates and Monad layout
          ["#000000", "#000000"], # Foreground for the widgets
          ["#FE5455", "#FE5455"]  # Layout widget color
          ]

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="JetBrains Mono",
    fontsize = 13,
    padding = 0,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
            widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
            widget.GroupBox(font="Noto Nerd Font",
                       fontsize = 13,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 5,
                       borderwidth = 3,
                       active = colors[3],
                       inactive = colors[3],
                       rounded = True,
                       highlight_color = colors[0],
                       highlight_method = "line",
                       this_current_screen_border = colors[1],
                       foreground = colors[2],
                       background = colors[0]
                       ),
            widget.Sep(
                       linewidth = 0,
                       padding = 590,
                       foreground = colors[2],
                       background = colors[0]
                       ),
            widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[2],
                       padding = -1,
                       padding_y = 2,
                       fontsize = 37
                       ),
            widget.Clock(
                       foreground = colors[5],
                       background = colors[2],
                       format =" %A, %B %d - %H:%M "
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[2],
                       foreground = colors[1],
                       padding = -1,
                       fontsize = 37
                       ),
             widget.Battery(
                       battery=1,
                       charge_char='^',
                       discharge_char='V',
                       empty_char='x',
                       full_char='100%',
                       format='   {percent:0.0%} ',
                       background = colors[1],
                       foreground = colors [5],
                            ),
                widget.TextBox(
                       text = '',
                       background = colors[1],
                       foreground = colors[6],
                       padding = -1,
                       fontsize = 37
                       ),
                widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[5],
                       background = colors[6],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[5],
                       background = colors[6],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0,
                       fontsize = 37
                       ),
                widget.Systray(
                       background = colors[0],
                       padding = 2,
                       ),
            widget.Sep (
                      linewidth =0,
                      padding =800,
                      foreground = colors[0],
                      background = colors[0]
                      ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            ]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

