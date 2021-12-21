import cv2

cap = cv2.VideoCapture()   # usb camera number 0,1,...
cap.open(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    ret,frame = cap.read()

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    hogParams = {
        "winStride":(8,8),
        "padding":(0,0),
        "scale":1.05,
        "hitThreshold":0,
        "finalThreshold":1
    }
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    human, r = hog.detectMultiScale(gray, **hogParams)
    if (len(human)>0):
        for (x, y, w, h) in human:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 1)
    
    frame = cv2.resize(frame, (720, 480))
    cv2.imshow('Test', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()