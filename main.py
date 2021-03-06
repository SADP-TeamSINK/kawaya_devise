#!/usr/bin/python
    # coding: UTF-8

from util import reading 
import os
import time
import subprocess
import shlex
from checkRoom import Checker 
from setting import Setting
import signal
import numpy as np

video = "mp4_h264_aac.mp4"
cmd = "omxplayer -o hdmi " + video

cmdline = shlex.split(cmd)

ID = Setting.ID;
url = Setting.url;
Rtime = Setting.time
dist = Setting.dist

pre_exist = False #現在のavailable

while(True):
    if(reading(0)<dist):
        print "true"
        #send room information to server 
        ch = Checker(ID, url, True, pre_exist)
        pre_exist = ch.start() 
        sp = subprocess.Popen(cmdline,preexec_fn=os.setsid) #subprocess called
        while(sp.poll() == None):
            time.sleep(Rtime)
            if(reading(0)>dist):
                print "break"
                os.killpg(sp.pid, signal.SIGTERM) #subprocess is stoped, send SIGTERM signal
                break
    else:
        print "false"
         #send room information to server 
        ch = Checker(ID, url, False, pre_exist)
        pre_exist = ch.start()

    time.sleep(Rtime)


