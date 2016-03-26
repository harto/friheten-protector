import cv2
from datetime import datetime
from os import path
from sauron.capture import read_frames
from sauron.upload import upload_file
import tempfile
import time

INTERVAL_SECS = 60 * 10

def initialise_camera():
    cam = cv2.VideoCapture(0)
    time.sleep(3)
    read_frame(cam)
    return cam

def read_frame(cam):
    return read_frames(cam).next()

def record_frame(cam, dir):
    frame = read_frame(cam)
    frame.overlay_timestamp()
    timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    record_image(frame.raw, path.join(dir, 'raw-%s.jpg' % timestamp))
    record_image(frame.processed, path.join(dir, 'processed-%s.jpg' % timestamp))

def record_image(img, file_path):
    cv2.imwrite(file_path, img)
    print 'wrote %s' % file_path
    try:
        upload_file(file_path)
    except Exception as e:
        print 'upload error: %s'

if __name__ == '__main__':
    dir = tempfile.mkdtemp()
    print "recording to %s" % dir
    while True:
        cam = initialise_camera()
        record_frame(cam, dir)
        cam.release()
        time.sleep(INTERVAL_SECS)
