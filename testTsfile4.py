import cv2
import threading
import time

flag = False

def Timer():
    global flag
    print("TimerStart")
    time.sleep(10)
    flag = True

class CameraClass(threading.Thread):
    enable = True
    num = 0
    img = None
    enimg = None
    frame = None
    def __init__(self,_num):
        threading.Thread.__init__(self)
        self.num = _num
        self.cap = cv2.VideoCapture()   # usb camera number 0,1,...
        self.cap.open(self.num)
        fourcc = cv2.VideoWriter_fourcc(*'MP2T')
        self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
#         self.out = cv2.VideoWriter('video/hikaku/test.ts',fourcc, 30.0, (800,480))
        self.out = cv2.VideoWriter()
    def run(self):
        f = 0
        while self.enable:
            ret,self.frame = self.cap.read()
            if ret == False:
                print('カメラ',self.num,'から映像を取得できませんでした。')
                break
            self.out.write(self.frame)
            self.img = cv2.resize(self.frame, (720, 480))
            encode_parms = [int(cv2.IMWRITE_JPEG_QUALITY),95]
            ret, self.enimg = cv2.imencode('.jpg',self.img,encode_parms)
            fname = "video/hikaku/test" + str(f) + ".jpg"
            with open(fname,'wb') as wf:
                wf.write(self.enimg)
            f+=1
        self.out.release()
        self.cap.release()

cam0 = CameraClass(0)
t = threading.Thread(target=Timer)
cam0.start()

while (cam0.frame is None):
    print("None.")

t.start()
while True:
    cv2.imshow("Camera0", cam0.frame)

    #Esc break key
    k = cv2.waitKey(1)
    if k == 27 or flag:
        cam0.enable = False
        break
cam0.join()
cv2.destroyAllWindows()

