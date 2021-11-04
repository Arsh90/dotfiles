import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import (
	Key,
	Screen,
	Group,
	Drag,
	Click,
	ScratchPad,
	DropDown,
	Match,
)
from libqtile.command import lazy
from libqtile import layout, bar, hook, extension #,widget
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration


group_decor = {
    "decorations": [
        RectDecoration(colour="#242831", radius=10, filled=True, padding_y=6)
    ],
    "padding_x": 5,
}

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "firefox" # My browser of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm+" -e zsh"),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("dmenu_run -p 'Run: '"),
             desc='Run Launcher'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='Qutebrowser'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         Key([mod], "r",
             lazy.to_screen(2),
             desc='Keyboard focus to monitor 3'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
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

workspaces = [
	{"name": "", "key": "1"},
	{"name": "","key": "2",},
	{
		"name": "",
		"key": "3",
	},
	{"name": "", "key": "4"},
	{"name": "", "key": "5"},
	{
		"name": "",
		"key": "6",
	},
	{"name": "", "key": "7"},
	{"name": "", "key": "8"},
	{"name": "", "key": "9"},
]

groups = [
	ScratchPad(
		"scratchpad",
		[
			# define a drop down terminal.
			# it is placed in the upper third of screen by default.
			DropDown(
				"term",
				"alacritty --class dropdown -e tmux_startup.sh",
				height=0.6,
				on_focus_lost_hide=False,
				opacity=1,
				warp_pointer=False,
			),
		],
	),
]

for workspace in workspaces:
	matches = workspace["matches"] if "matches" in workspace else None
	groups.append(Group(workspace["name"]))
	keys.append(
		Key(
			[mod],
			workspace["key"],
			lazy.group[workspace["name"]].toscreen(),
			desc="Focus this desktop",
		)
	)
	keys.append(
		Key(
			[mod, "shift"],
			workspace["key"],
			lazy.window.togroup(workspace["name"]),
			desc="Move focused window to another group",
		)
	)


# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {
	"border_width": 3,
	"margin": 9,
	"border_focus": "3b4252",
	"border_normal": "3b4252",
	"font": "FiraCode Nerd Font",
	"grow_amount": 2,
}

layouts = [
    layout.Floating(**layout_theme, fullscreen_border_width=3, max_border_width=3),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
#    layout.Zoomy(**layout_theme)
]

colors = [
	["#2e3440", "#2e3440"],  # 0 background
	["#d8dee9", "#d8dee9"],  # 1 foreground
	["#3b4252", "#3b4252"],  # 2 background lighter
	["#bf616a", "#bf616a"],  # 3 red
	["#a3be8c", "#a3be8c"],  # 4 green
	["#ebcb8b", "#ebcb8b"],  # 5 yellow
	["#81a1c1", "#81a1c1"],  # 6 blue
	["#b48ead", "#b48ead"],  # 7 magenta
	["#88c0d0", "#88c0d0"],  # 8 cyan
	["#e5e9f0", "#e5e9f0"],  # 9 white
	["#4c566a", "#4c566a"],  # 10 grey
	["#d08770", "#d08770"],  # 11 orange
	["#8fbcbb", "#8fbcbb"],  # 12 super cyan
	["#5e81ac", "#5e81ac"],  # 13 super blue
	["#242831", "#242831"],  # 14 super dark background
]

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_main():
    widgets_list = [
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0],
                       ),
              widget.GroupBox(
					**group_decor,
                    font="Font Awesome 5 Brands",
                    borderwidth = 0,
                    active = colors[9],
                    inactive = colors[10],
                    disable_drag = True,
                    rounded = True,
                    block_highlight_text_color = colors[6],
                    foreground = colors[1],
                    background = colors[0],
            ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0],
                       ),
            widget.CurrentLayout(
                **group_decor,
                background = colors[0],
                foreground = colors[8],
                padding = 10
            ),
            widget.Spacer(background = colors[0]),
            widget.WindowName(
                background=colors[0],
                foreground=colors[12],
                width=bar.CALCULATED,
                empty_group_string="",
                max_chars=130,
                fmt = ' {}'
            ),
            widget.Spacer(background = colors[0]),
            widget.PulseVolume(
                **group_decor,
                padding = 10,
                foreground=colors[8],
                background=colors[0],
                limit_max_volume="True",
                mouse_callbacks={"Button3": lambda: qtile.cmd_spawn("pavucontrol")},
                fmt = ' {}'
            ),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Systray(
                **group_decor,
                padding = 10,
                icon_size = 20,
                #foreground=colors[14],
                background=colors[0],
            ),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Wlan(
                **group_decor,
                padding = 10,
                disconnected_message = 'Disconnected',
                background = colors[0],
                foreground = colors[8],
                interface = 'wlp0s20f0u6',
                format = ' {essid}',
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("networkmanager_dmenu")},
            ),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Clock(
                **group_decor,
                padding = 10,
                format=" %a, %b %d",
                background=colors[0],
                foreground=colors[5],
			),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Clock(
                **group_decor,
                padding = 10,
                format="  %I:%M %p",
                background=colors[0],
                foreground=colors[4],
			),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.TextBox(
                    **group_decor,
					text="⏻",
                    background = colors[0],
					foreground=colors[13],
					font="Font Awesome 5 Free Solid",
					fontsize=15,
					padding=10,
					#mouse_callbacks={"Button1": lambda: open_powermenu},
				),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
]
    return widgets_list

def init_widgets_secondary():
    widgets_list = [
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0],
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0],
                       ),
            widget.CurrentLayout(
                **group_decor,
                background = colors[0],
                foreground = colors[8],
                padding = 10
            ),
            widget.Spacer(background = colors[0]),
            widget.WindowName(
                background=colors[0],
                foreground=colors[12],
                width=bar.CALCULATED,
                empty_group_string="",
                max_chars=130,
                fmt = ' {}'
            ),
            widget.Spacer(background = colors[0]),
            widget.PulseVolume(
                **group_decor,
                padding = 10,
                foreground=colors[8],
                background=colors[0],
                limit_max_volume="True",
                mouse_callbacks={"Button3": lambda: qtile.cmd_spawn("pavucontrol")},
                fmt = ' {}'
            ),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Systray(
                **group_decor,
                padding = 10,
                icon_size = 20,
                #foreground=colors[14],
                background=colors[0],
            ),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Wlan(
                **group_decor,
                padding = 10,
                disconnected_message = 'Disconnected',
                background = colors[0],
                foreground = colors[8],
                interface = 'wlp0s20f0u6',
                format = ' {essid}',
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("networkmanager_dmenu")},
            ),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Clock(
                **group_decor,
                padding = 10,
                format=" %a, %b %d",
                background=colors[0],
                foreground=colors[5],
			),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.Clock(
                **group_decor,
                padding = 10,
                format="  %I:%M %p",
                background=colors[0],
                foreground=colors[4],
			),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
            widget.TextBox(
                    **group_decor,
					text="⏻",
                    background = colors[0],
					foreground=colors[13],
					font="Font Awesome 5 Free Solid",
					fontsize=15,
					padding=10,
					#mouse_callbacks={"Button1": lambda: open_powermenu},
				),
            widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0],
            ),
]
    return widgets_list

screens = [Screen(top=bar.Bar(widgets=init_widgets_main(), opacity=1.0, size=35)),Screen(top=bar.Bar(widgets=init_widgets_secondary(),opacity=1.0,size=35))]
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
    Match(wm_class='Unity'),          # Unity
    Match(wm_class='unityhub'),       # UnityHub
    Match(wm_class='About Mozilla Firefox'),          # Firefox
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])



wmname = "LG3D"
