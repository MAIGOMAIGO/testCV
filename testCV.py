import cv2

def Camera(num):
    cap = cv2.VideoCapture()
    cap.open(num)
    # Format:MJPG WIDTH:800 HEIGHT:480 FPS:30
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    return cap

#Camera number 0,1,2...
cam = Camera(0)

while True:
    ret,img = cam.read()

    cv2.imshow('Camera1', img)
    
    #Esc break key
    k = cv2.waitKey(1)
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()

