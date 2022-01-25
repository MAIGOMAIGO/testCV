import cv2
import threading
import subprocess as sp
import copy

class CameraClass(threading.Thread):
    def __init__(self,_num):
        sp.call("mkdir -p /tmp/Stream".split())
        sp.call("mkdir -p /tmp/StreamImg".split())
        threading.Thread.__init__(self)
        #Camera set width:800 height:480 fps:30
        self.num = _num
        self.cap = cv2.VideoCapture()
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.cap.set(cv2.CAP_PROP_FOURCC, self.fourcc)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.enable = True

    def run(self):
        self.z=0
        self.cap.open(self.num)
        while self.enable:
            #30fps * 3s
            for i in range(30 * 3):
                ret,self.frame = self.cap.read()
                if ret == False:
                    print('カメラ',self.num,'から映像を取得できませんでした。')
                    break
                threading.Thread(target=self.makeImg,args=(self.frame,self.z,i)).start()
            else:
                threading.Thread(target=self.makeTs).start()
                self.z+=1
                continue
            # cam not found
            break
        self.cap.release()
        
    def makeImg(self,frame,z,i):
        #jpeg encode
        self.img = cv2.resize(frame, (720, 480))
        encode_parms = [int(cv2.IMWRITE_JPEG_QUALITY),95]
        ret, self.enimg = cv2.imencode('.jpg',self.img,encode_parms)
        with open('/tmp/StreamImg/cam'+str(self.num)+'stream'+str(z)+'img'+ str(i) +'.jpg','ab') as wf:
            wf.write(self.enimg)
            
    def makeTs(self):
        d = copy.deepcopy(self.z)
        cmd = "ffmpeg -y -r 30 -i /tmp/StreamImg/cam"+str(self.num)+"stream"+str(d)+"img%d.jpg "\
                  "-c:v libx264 -filter_complex scale=720x600,fps=30 "\
                  "/tmp/Stream/cam"+str(self.num)+"stream"+str(d)+".ts"
        sp.call(cmd.split())
        for s in range(90):
            cmd = "rm /tmp/StreamImg/cam"+str(self.num)+"stream"+str(d)+"img"+str(s)+".jpg"
            sp.call(cmd.split())

# import Camera
# 
# cam0 = Camera.CameraClass(0)
# cam0.start()
# while (not cam0.cap.isOpened()):
#     print("None.")
# cam0.enable = False
# cam0.join()
