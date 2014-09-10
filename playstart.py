import cv2
from usonic import reading
import threading
import time

updatelock = False
windowname = 'frame'
cap = cv2.VideoCapture('mp4_h264_aac.mp4')

class playvideo:
    def __init__(self):
        self.stop_event = threading.Event() #stopping flag 

        #making and starting thread
        self.thread = threading.Thread(target = self.video)
        self.thread.start()

    def video(self):
            #define window name 
        cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)

            #get the number of frame
        frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            #print "frame:",frames
        
            #until all frames read:
        while(cap.isOpened()):
                #print "2"
            if(self.stop_event.is_set()):#get stoping frag
                print "stop"
                break;
                #read 1 frame
            ret, frame = cap.read()

                #can not read
            if ret == False:
                    #print "3"
                break

                # show in display
            cv2.imshow(windowname,frame)

            # break by q key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release file
        cap.release()

        # close Window
        cv2.destroyAllWindows()

    def stop(self):
        self.stop_event.set()
        self.thread.join()    #wait thread stopping

if __name__ == '__main__':
    #print "aaaaaaaaa"
    while(True):
        if(reading(0)<100):
            print "true"
            p = playvideo()
            #print p.isAlive()
            while(True):
                print "while"
                time.sleep(3)
                if(reading(0)>100):
                    p.stop()
                    break
        else:
            print "false"
    time.sleep(3)
