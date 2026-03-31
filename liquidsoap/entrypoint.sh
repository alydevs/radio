#!/bin/sh
/usr/bin/python3 /etc/liquidsoap/gen_playlists.py
/usr/bin/liquidsoap /etc/liquidsoap/script.liq
