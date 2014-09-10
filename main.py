#!/usr/bin/python
    # coding: UTF-8

from util import reading 
import os
import time
import subprocess
import shlex
from checkRoom import Checker 
from setting import Setting

video = "mp4_h264_aac.mp4"
cmd = "omxplayer -o hdmi " + video

cmdline = shlex.split(cmd)

ID = Setting.ID;
url = Setting.url;
time = Setting.time
# ch = Checker(ID, url, time, sensor);
# ch.start();
while(True):
    if(reading(0)<70):
        print "true"
        #send room information to server 
        ch = Checker(ID, url, time, True)
        ch.start() 
        sp = subprocess.Popen(cmdline,preexec_fn=os.setsid) #subprocess called
        while(sp.poll() == None):
            time.sleep(3)
            if(reading(0)>70):
                print "break"
                os.killpg(sp.pid, signal.SIGTERM) #subprocess is stoped, send SIGTERM signal
                break
    else:
        print "false"
         #send room information to server 
        ch = Checker(ID, url, time, False)
        ch.start()

    time.sleep(3)


