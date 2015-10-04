import numpy
import cv2
from sauron import config
from sauron.detection import MotionDetector

if __name__ == '__main__':
    config.init()
    camera = cv2.VideoCapture(0)
    MotionDetector(camera).detect()
    #cv2.destroyAllWindows()
    camera.release()
