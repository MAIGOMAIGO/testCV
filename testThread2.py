import time
import threading

class TestThreadClass:
    def __init__(self):
        self.japan = "こんにちは"
        self.EN = "hello"
        self.c = "a"

    def getJapan(self):
        time.sleep(2)
        print (self.japan)

    def getEN(self):
        time.sleep(1)
        print (self.EN)

    def getC(self):
        time.sleep(0.5)
        print (self.c)

    def setC(self, chello):
        self.c = chello

test = TestThreadClass()
thread1 = threading.Thread(target = test.getJapan)
thread2 = threading.Thread(target = test.getEN)
thread3 = threading.Thread(target = test.getC)

thread1.start()
thread2.start()
thread3.start()

thread3.join()
test.setC("Hello_World")

thread3 = threading.Thread(target = test.getC())
thread3.start()

thread1.join()