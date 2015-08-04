import numpy
import cv2
from sauron.config import init as init_config
from sauron.config import get as get_config
from sauron.detector import detect_motion

if __name__ == '__main__':
    init_config()
    camera = cv2.VideoCapture(0)
    detect_motion(camera)
    cv2.destroyAllWindows()
    camera.release()
