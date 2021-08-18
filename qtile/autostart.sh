#!/usr/bin/env bash 
festival --tts $HOME/.config/qtile/welcome_msg &
lxsession &
nitrogen --restore &
/usr/bin/emacs --daemon &
volumeicon &
nm-applet &
