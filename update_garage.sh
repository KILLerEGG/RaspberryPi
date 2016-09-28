#!/bin/bash

show(){
	local x=$1
	local y=$2
	local txt="$3"
	# Set cursor position on screen
	tput cup $x $y
	echo "$txt"
}
while [ : ]
do
	clear
	# Get the system time
	now="$(date +"%r")"
	now_hour="$(date +"%H")"
	now_min="$(date +"%M")"
	now_day="$(date +"%u")"
	# Show main - menu, server name and time
	show 10 10 "Garage update script for $HOSTNAME - $now"
	show 11 10 "Will update every Monday at midnight"
	if [[ "$now_hour" = "00" && "$now_min" = "00" ]]
	then
		if [ "$now_day" = "1" ]
		then
			show 13 10 "Updating database now!"
			php update_garage.php
		fi
	fi

	show 12 10 "PLEASE DO NOT STOP SCRIPT, OR DATABASE WILL NOT UPDATE WEEKLY!"

	sleep 60
done
