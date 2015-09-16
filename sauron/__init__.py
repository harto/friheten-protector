import numpy
import cv2
from sauron.config import init as init_config
from sauron.detection import Detector

if __name__ == '__main__':
    init_config()
    camera = cv2.VideoCapture(0)
    Detector(camera).detect()
    cv2.destroyAllWindows()
    camera.release()
