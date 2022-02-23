from cmath import nan
from threading import Thread
import time

class CameraMan(Thread):
    isAlive = False
    def __init__(self, tempo, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.tempo = tempo

    def run(self):
        self.isAlive = True
        time.sleep(self.tempo)
        print("gravando!")
        self.isAlive = False
        

if __name__ == "__main__":

    camera_man_0 = CameraMan(3)
    camera_man_1 = CameraMan(5)

    camera_man_0.start()
    camera_man_1.start()

    while True:

        if not (camera_man_0.isAlive and camera_man_1.isAlive):

            camera_man_0.start()
            camera_man_1.start()
  