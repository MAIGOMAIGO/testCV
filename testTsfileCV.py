import cv2
import threading

class CameraClass(threading.Thread):
    enable = True
    num = 0
    img = None
    enimg = None
    frame = None
    def __init__(self,_num):
        threading.Thread.__init__(self)
        #Camera set fourcc:MPEG2TS width:800 height:480 fps:30
        self.num = _num
        self.cap = cv2.VideoCapture()
        self.cap.open(self.num)
        self.fourcc = cv2.VideoWriter_fourcc(*'MP2T')
        self.cap.set(cv2.CAP_PROP_FOURCC, self.fourcc)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def run(self):
        z=0
        while self.enable:
            #fp = 'video/cam' + str(self.num) + 'test' + str(z) + '.ts'
            self.out = cv2.VideoWriter('test.ts',self.fourcc, 30.0, (800,480))
            #30fps * 3s
            for i in range(30 * 3):
                ret,self.frame = self.cap.read()
                if ret == False:
                    print('カメラ',self.num,'から映像を取得できませんでした。')
                    break
                self.out.write(self.frame)
                #jpeg encode
                self.img = cv2.resize(self.frame, (720, 480))
                encode_parms = [int(cv2.IMWRITE_JPEG_QUALITY),95]
                ret, self.enimg = cv2.imencode('.jpg',self.img,encode_parms)
            self.out.release()
            z+=1
        self.cap.release()
def main():
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