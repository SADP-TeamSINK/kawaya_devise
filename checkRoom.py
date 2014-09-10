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
    def __init__(self, id, url, sensor, pre_exist):
        # 端末の固有IDを登録
        self.id = id
        self.url = url  
        self.sensor = sensor #センサー情報（人がいればtrue）
        self.proxyDict = Setting.proxyDict
        self.pre_exist = pre_exist #前の状態のavailable

    #監視処理の開始
    def start(self):
        print "Start to check this room!"
        print "Now, there is ", self.pre_exist

        try:

            if self.sensor:
                    # もし規定距離内に反応があった場合
                self.exist()
            else:
                    # 規定距離内に反応がなかった場合
                self.not_exist()
        except:
            print "Exception caught!!", sys.exc_info()[0]

        return self.pre_exist#現在のセンサー情報を返す
                
    # センサーが人を感知した場合
    def exist(self):
        print "someone exists"
        if not self.pre_exist:
            self.pre_exist = True
            json_data = {"room_id": self.id, "status": 1}
            headers={'content-type': 'application/json'}
            api_url=self.url
            encoded_json=json.dumps(json_data,indent=1)
            print "send to:", api_url
            print encoded_json
            print headers
            r = requests.post(api_url, data=encoded_json, headers=headers, proxies=self.proxyDict)
            print r

    # センサーが人を感知しなかった場合
    def not_exist(self):
        print "noone exists"
        if self.pre_exist:
            self.pre_exist = False
            json_data = {"room_id": self.id, "status": 0}
            headers={'content-type': 'application/json'}
            encoded_json=json.dumps(json_data)
            api_url=self.url
            print "send to:", api_url
            print encoded_json
            r = requests.post(api_url, data=encoded_json, headers=headers, proxies=self.proxyDict)
            print r
