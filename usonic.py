#!/usr/bin/python
    # coding: UTF-8
import numpy as np
import cv2
# remember to change the GPIO values below to match your sensors
# GPIO output = the pin that's connected to "Trig" on the sensor
# GPIO input = the pin that's connected to "Echo" on the sensor

updatelock = False # トラックバー処理中のロックフラグ
windowname = 'frame' # Windowの名前
trackbarname = 'Position' # トラックバーの名前

    # MP4ファイルを読む
    # MP4は適当な長さのサンプルをインターネットから拾ってくる
    # 参考:http://www.engr.colostate.edu/me/facil/dynamics/avis.htm
    # http://www.gomplayer.jp/player/support/sample.htmlから取ってきました
cap = cv2.VideoCapture('mp4_h264_aac.mp4')

# トラックバーを動かしたときに呼び出されるコールバック関数の定義
def onTrackbarSlide(pos):
    updatelock = True
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos)
    updatelock = False

def reading(sensor):
    import time
    import RPi.GPIO as GPIO
    
    # Disable any warning message such as GPIO pins in use
    GPIO.setwarnings(False)
    
    # use the values of the GPIO pins, and not the actual pin number
    # so if you connect to GPIO 25 which is on pin number 22, the 
    # reference in this code is 25, which is the number of the GPIO 
    # port and not the number of the physical pin
    GPIO.setmode(GPIO.BCM)
    
    if sensor == 0:
        
        # point the software to the GPIO pins the sensor is using
        # change these values to the pins you are using
        # GPIO output = the pin that's connected to "Trig" on the sensor
        # GPIO input = the pin that's connected to "Echo" on the sensor
        GPIO.setup(17,GPIO.OUT)
        GPIO.setup(27,GPIO.IN)
        GPIO.output(17, GPIO.LOW)
        
        # found that the sensor can crash if there isn't a delay here
        # no idea why. If you have odd crashing issues, increase delay
        time.sleep(0.3)
        
        # sensor manual says a pulse ength of 10Us will trigger the 
        # sensor to transmit 8 cycles of ultrasonic burst at 40kHz and 
        # wait for the reflected ultrasonic burst to be received
        
        # to get a pulse length of 10Us we need to start the pulse, then
        # wait for 10 microseconds, then stop the pulse. This will 
        # result in the pulse length being 10Us.
        
        # start the pulse on the GPIO pin 
        # change this value to the pin you are using
        # GPIO output = the pin that's connected to "Trig" on the sensor
        GPIO.output(17, True)
        
        # wait 10 micro seconds (this is 0.00001 seconds) so the pulse
        # length is 10Us as the sensor expects
        time.sleep(0.00001)
        
        # stop the pulse after the time above has passed
        # change this value to the pin you are using
        # GPIO output = the pin that's connected to "Trig" on the sensor
        GPIO.output(17, False)

        # listen to the input pin. 0 means nothing is happening. Once a
        # signal is received the value will be 1 so the while loop
        # stops and has the last recorded time the signal was 0
        # change this value to the pin you are using
        # GPIO input = the pin that's connected to "Echo" on the sensor
        while GPIO.input(27) == 0:
          signaloff = time.time()
        
        # listen to the input pin. Once a signal is received, record the
        # time the signal came through
        # change this value to the pin you are using
        # GPIO input = the pin that's connected to "Echo" on the sensor
        while GPIO.input(27) == 1:
          signalon = time.time()
        
        # work out the difference in the two recorded times above to 
        # calculate the distance of an object in front of the sensor
        timepassed = signalon - signaloff
        
        # we now have our distance but it's not in a useful unit of
        # measurement. So now we convert this distance into centimetres
        distance = timepassed * 17000
        
        # return the distance of an object in front of the sensor in cm
        return distance
        
        # we're no longer using the GPIO, so tell software we're done
        GPIO.cleanup()

    else:
        print "Incorrect usonic() function varible."

        
if(reading(0)<100):
    print "true"

# 名前付きWindowを定義する
    cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)

# MP4ファイルのフレーム数を取得する
    frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

# フレーム数が1以上ならトラックバーにセットする
    if (frames > 0):
        cv2.createTrackbar(trackbarname, windowname, 0, frames, onTrackbarSlide)

# MP4ファイルを開いている間は繰り返し（最後のフレームまで読んだら終わる）
    while(cap.isOpened()):

    # トラックバー更新中は描画しない
        if (updatelock):
            continue

    # １フレーム読む
        ret, frame = cap.read()

        # 読めなかったら抜ける
        if ret == False:
            break

        # 画面に表示
        cv2.imshow(windowname,frame)

        # 現在のフレーム番号を取得
        curpos = int(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))

    # トラックバーにセットする（コールバック関数が呼ばれる）
        cv2.setTrackbarPos(trackbarname, windowname, curpos)

    # qを押したら抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # AVIファイルを解放
    cap.release()

    # Windowを閉じる
    cv2.destroyAllWindows()

else:
    print "false"
