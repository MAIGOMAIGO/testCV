import cv2
import threading
import subprocess as sp
import copy

class CameraClass(threading.Thread):
    enable = True
    num = 0
    img = None
    enimg = None
    frame = None
    def __init__(self,_num):
        threading.Thread.__init__(self)
        #Camera set width:800 height:480 fps:30
        self.num = _num
        self.cap = cv2.VideoCapture(self.num)
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.cap.set(cv2.CAP_PROP_FOURCC, self.fourcc)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def run(self):
        self.z=0
        while self.enable:
            #30fps * 3s
            for i in range(30 * 3):
                ret,self.frame = self.cap.read()
                if ret == False:
                    print('カメラ',self.num,'から映像を取得できませんでした。')
                    break
                #jpeg encode
                self.img = cv2.resize(self.frame, (720, 480))
                encode_parms = [int(cv2.IMWRITE_JPEG_QUALITY),95]
                ret, self.enimg = cv2.imencode('.jpg',self.img,encode_parms)
                with open('/tmp/StreamImg/cam'+str(self.num)+'stream'+str(self.z)+'img'+ str(i) +'.jpg','ab') as wf:
                    wf.write(self.enimg)
            ts = threading.Thread(target=self.makeTs)
            ts.start()
            self.z+=1
        ts.join()
        self.cap.release()
    def makeTs(self):
        d = copy.deepcopy(self.z)
        cmd = "ffmpeg -y -r 30 -i /tmp/StreamImg/cam"+str(self.num)+"stream"+str(d)+"img%d.jpg "\
                  "-vcodec mpeg2video -filter_complex scale=720x600,fps=30 "\
                  "/tmp/Stream/cam"+str(self.num)+"stream"+str(d)+".ts"
        sp.call(cmd.split())
        for s in range(90):
            cmd = "rm /tmp/StreamImg/cam"+str(self.num)+"stream"+str(d)+"img"+str(s)+".jpg"
            sp.call(cmd.split())

def main():
    sp.call("mkdir -p /tmp/Stream".split())
    sp.call("mkdir -p /tmp/StreamImg".split())
    cam0 = CameraClass(0)
    cam0.start()
    #wait camera Open
    while (cam0.frame is None):
        print("None.")

    while True:
        cv2.imshow("Camera0", cam0.frame)

        #Esc break key
        k = cv2.waitKey(1)
        if k == 27:
            cam0.enable = False
            break
    cam0.join()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()