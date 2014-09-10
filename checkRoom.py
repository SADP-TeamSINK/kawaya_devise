#!/usr/bin/python
    # coding: UTF-8
import sys
import numpy as np
import time
from util import reading
from setting import Setting
import requests
import json


class Checker:
    def __init__(self, id, url, time, sensor):
        # 端末の固有IDを登録
        self.id = id
        self.existence = False
        self.time = time
        self.url = url + "/" + str(self.id) + "/"
        self.sensor = sensor #センサー情報（人がいればtrue）

    #監視処理の開始
    def start(self):
        print "Start to check this room!"
        while True:
            print "Now, there is ", self.existence

            # 距離の取得間隔
            time.sleep(self.time)
            # 距離の取得
            #d = reading(0)

            try:
                print d

                if self.sensor:
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
            # api_url = self.url + "1"
            # print "api-url: ", api_url
            # r = requests.patch(api_url)
            json_data = {"room_id": self.id, "status": 1}
            headers={'content-type': 'application/json'}
            api_url=self.url
            print "send to: ", api_url
            r = requests.post(api_url, data=json.dumps(json_data,indent=2), headers=headers)
            print r

    # センサーが人を完治しなかった場合
    def not_exist(self):
        print "noone exists"
        if self.existence:
            self.existence = False
            # api_url = self.url + "0"
            # print "api-url: ", api_url
            # r = requests.patch(api_url)
            json_data = {"room_id": self.id, "status": 0}
            headers={'content-type': 'application/json'}
            api_url=self.url
            print "send to: ", api_url
            r = requests.post(api_rl, data=json.dumps(json_data,indent=2), headers=headers)
            print r


# if __name__ == '__main__':
#     ID = Setting.ID;
#     url = Setting.url;
#     time = Setting.time
#     ch = Checker(ID, url, time, sensor);
#     ch.start();
