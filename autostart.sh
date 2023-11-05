#!/bin/sh
picom --config  $HOME/.config/picom/picom.conf&
sh -c "(sleep 10 && exec /opt/nutstore/bin/nutstore-pydaemon.py)"&
# "/home/sawyer/programs/nextcloud" --background&
ibus-daemon -drx&
~/programs/clash/cfw &

nitrogen --restore&
