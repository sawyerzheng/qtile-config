#!/bin/sh
picom --config  $HOME/.config/picom/picom.conf&

if test -f /opt/nutstore/bin/nutstore-pydaemon.py ; then
    sh -c "(sleep 10 && exec /opt/nutstore/bin/nutstore-pydaemon.py)"&
else
    echo "Waring:: nutstore not installed"
fi

# "/home/sawyer/programs/nextcloud" --background&
ibus-daemon -drx&
~/programs/clash/cfw &

nitrogen --restore&
