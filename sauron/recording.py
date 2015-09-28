import cv2
from os import path
from sauron import config
import time

class Recording(object):

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.frame_count = 0
        self.last_write_time = time.time()

    def write(self, frame, rects):
        now = time.time()
        if now - self.last_write_time < 1.0 / config.get('OUTPUT_FPS'): return
        image = self.overlay(frame.raw.copy(), rects)
        self.write_image(image, '%02d' % self.frame_count)
        self.frame_count += 1
        self.last_write_time = now

    def write_image(self, image, filename):
        output_path = path.join(self.output_dir, '%s.jpg' % filename)
        cv2.imwrite(output_path, image)
        print 'wrote %s' % output_path

    def overlay(self, image, rects):
        for (x, y, w, h) in rects:
            cv2.rectangle(image,
                          (x, y),
                          (x + w, y + h),
                          color=(0, 0, 255),
                          thickness=2)
        return image

    def finish(self):
        print 'finalising recording'
