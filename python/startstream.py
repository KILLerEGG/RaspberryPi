import os
import sys
import multiprocessing, time, signal
import shlex, subprocess
from threading import Thread
import datetime

def thread_func(day):
	video_opts_rtmp = "-vcodec copy -an -f flv -metadata streamName=myStream tcp://0.0.0.0:6666"
	video_opts_hls = "-c:v copy -map 0 -f ssegment -segment_time 1 -segment_format mpegts -segment_list /var/www/html/stream/server/stream.m3u8 -segment_list_size 10 -segment_wrap 20 -segment_list_flags +live -segment_list_type m3u8 -segment_list_entry_prefix segments/ '/var/www/html/stream/server/segments/stream%03d.ts'"
	raspiDayArgs = shlex.split("raspivid -n -t 0 -ih -ISO 800 -ex night -w 720 -h 405 -fps 25 -b 20000000 -o - --hflip")
	raspiNightArgs = shlex.split("raspivid -n -t 0 -ex night -w 720 -h 405 -fps 0 -b 500000 -vf -o - --hflip --vflip")
	raspiTest = shlex.split("raspivid -t 0 -ih -ex night -w 704 -h 400 -fps 0 -b 5184000 -vf -o - --hflip --vflip")
	#p1 = subprocess.Popen(raspiTest, stdout=subprocess.PIPE)
	if (day == True):
		p1 = subprocess.Popen(raspiDayArgs, stdout=subprocess.PIPE)
	else:
		p1 = subprocess.Popen(raspiTest, stdout=subprocess.PIPE)

	ffmpegArgs = shlex.split("ffmpeg -y -i - " + video_opts_rtmp + " " + video_opts_hls)
	subprocess.Popen(ffmpegArgs, stdin=p1.stdout)
	return

if __name__ == "__main__":
	systemForce = 0
	day = True

	if (len(sys.argv) == 2):
		if sys.argv[1] == "--night" or sys.argv[1] == "-n":
			day = False
		elif sys.argv[1] == "--force" or sys.argv[1] == "-f":
			systemForce = 1
		else:
                        print "Unknown argument"
                        print "Usage: python startstream.py <optional>(--night/-n --force/-f)"
                        sys.exit()
	elif (len(sys.argv) == 3):
		if (sys.argv[1] == "--night" or sys.argv[1] == "-n") or (sys.argv[2] == "--night" or sys.argv[2] == "-n"):
			day = False
		else:
			print "Unknown argument"
                        print "Usage: python startstream.py <optional>(--night/-n --force/-f)"
                        sys.exit()
		if (sys.argv[2] == "--force" or sys.argv[2] == "-f") or (sys.argv[1] == "--force" or sys.argv[1] == "-f"):
			systemForce = 1
		else:
			print "Unknown argument"
			print "Usage: python startstream.py <optional>(--night/-n --force/-f)"
			sys.exit()
	elif (len(sys.argv) > 3):
		print "Usage: python startstream.py <optional>(--night/-n --force/-f)"
		sys.exit()
	
	#Check if force command was used. If so, then ignore scheduled start/stop
	if systemForce == 0:
		#Start the stream if after 8am and before 9pm
		timecheck = int(datetime.datetime.now().strftime('%H'))
		if (timecheck >= 8) and (timecheck < 21):
			thread_func(day)
			isRunning = True
		else:
			print "[INFO] It is too late to start stream, will resume stream at 8am..."
			isRunning = False
		while (1):
			print "[INFO] Checking time..."
			#Get time and check if it equals 9 then stop stream
			str = datetime.datetime.now().strftime('%H:%M')
			if (str == "21:00") and (isRunning == True):
				print "[INFO] Shutting down stream, time for bed..."
				subprocess.call(["pkill ffmpeg"], shell=True)
				subprocess.call(["pkill raspivid"], shell=True)
				isRunning = False
			elif (str == "08:00") and (isRunning == False):
				#Get time again and check in the morning if == 8 then start stream
				print "[INFO] Good morning! Starting stream up..."
				thread_func(day)
				isRunning = True
			time.sleep(60)
	else:
		thread_func(day)
		while (1):
			time.sleep(10)
