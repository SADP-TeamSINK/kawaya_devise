#!/usr/bin/python
    # coding: UTF-8
import sys
import numpy as np
import time
from util import reading
from setting import Setting
import requests


class Checker:
    def __init__(self, id, dist, url, time):
        # 端末の固有IDを登録
        self.id = id
        self.existence = False
        self.dist = dist
        self.time = time
        self.url = url + "/" + str(self.id) + "/"

    #監視処理の開始
    def start(self):
        print "Start to check this room!"
        while True:
            print "Now, there is ", self.existence

            # 距離の取得間隔
            time.sleep(self.time)
            # 距離の取得
            d = reading(0)

            try:
                print d

                if d < self.dist:
                    # もし規定距離内に反応があった場合
                    self.exist()
                else:
                    # 規定距離内に反応がなかった場合
                    self.not_exist()
            except:
                print "Exception caught!!", sys.exc_info()[0]
                
    # センサーが人を感知した場合
    def exist(self):
        print "someone exists"
        if not self.existence:
            self.existence = True
            api_url = self.url + "1"
            print "api-url: ", api_url
            r = requests.patch(api_url)

    # センサーが人を完治しなかった場合
    def not_exist(self):
        print "noone exists"
        if self.existence:
            self.existence = False
            api_url = self.url + "0"
            print "api-url: ", api_url
            r = requests.patch(api_url)


if __name__ == '__main__':
    ID = Setting.ID;
    DIST = Setting.dist;
    url = Setting.url;
    time = Setting.time
    ch = Checker(ID, DIST, url, time);
    ch.start();
