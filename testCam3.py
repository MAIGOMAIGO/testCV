import cv2
import threading

enimg = None
img = None

def cam():
    global enimg
    global img
    cap = cv2.VideoCapture()   # usb camera number 0,1,...
    cap.open(0)
    #format:MJPG W:800 H:480 FPS:30
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    while True:
        ret,frame = cap.read()
        img = cv2.resize(frame, (720, 480))
        
        encode_parms = [int(cv2.IMWRITE_JPEG_QUALITY),95]
        ret, enimg = cv2.imencode('.jpg',img,encode_parms)
        
        cv2.imshow('Test', frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    tCam = threading.Thread(target = cam)
    tCam.start()
    while (img is None):
        print ("None.")
    while (enimg is None):
        print ("None.")

#     with open("data/output2.jpg",'wb') as wf:
#         wf.write(enimg)

    tCam.join()

main()

