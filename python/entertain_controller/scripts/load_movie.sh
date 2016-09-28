#!/bin/bash

rm -f movie_fifo
mkfifo movie_fifo
/usr/bin/omxplayer $1 < movie_fifo
#/usr/bin/omxplayer -o hdmi --display=5 $1 < movie_fifo
