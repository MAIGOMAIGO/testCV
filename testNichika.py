import cv2
import threading

def camera():
    cap = cv2.VideoCapture()   # usb camera number 0,1,...
    cap.open(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    threshold = 200
    
    while True:
        ret,frame = cap.read()
        re,thresh = cv2.threshold(frame,threshold,255,cv2.THRESH_BINARY)

        img = cv2.resize(thresh, (720, 480))
        cv2.imshow('Test', img)

        k = cv2.waitKey(1)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

tCam = threading.Thread(target=camera)
tCam.start()
tCam.join()