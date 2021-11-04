#!/usr/bin/env bash
# Wallpaper
nitrogen --restore &
# Dunst
dunst &

# Network manager for non ethernet connections
nm-applet &

# Not using picom atm
# picom &
picom --config ~/.config/qtile/picom.conf &
