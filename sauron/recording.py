import cv2
from datetime import datetime
from os import makedirs, path, rmdir
from glob import glob
from sauron import config
import shutil
import subprocess
import time

class Recording(object):

    @classmethod
    def setup(cls): # FIXME: needs better name
        output_dir = path.join('/tmp', datetime.now().strftime('recording-%Y%m%d%H%M%S'))
        if not path.exists(output_dir): makedirs(output_dir)
        return cls(output_dir)

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.frame_count = 0
        self.last_write_time = time.time()

    def write(self, frame, rects):
        now = time.time()
        if now - self.last_write_time < 1.0 / config.get('OUTPUT_FPS'): return
        image = self.overlay(frame.raw.copy(), rects)
        self.write_image(image)
        self.frame_count += 1
        self.last_write_time = now

    def write_image(self, image):
        filename = datetime.now().strftime('%Y%m%d%H%M%S%f.jpg')
        output_path = path.join(self.output_dir, filename)
        cv2.imwrite(output_path, image)

    def overlay(self, image, rects):
        for (x, y, w, h) in rects:
            cv2.rectangle(image,
                          (x, y),
                          (x + w, y + h),
                          color=(0, 0, 255),
                          thickness=2)
        return image

    def finalise(self):
        print 'finalising recording'
        input_files = sorted(glob(path.join(self.output_dir, '*')))
        output_filename = "%s.gif" % self.output_dir
        args = ['convert',
                '-delay',
                str(int(100.0 / config.get('OUTPUT_FPS'))),
                '-loop',
                '0']
        args += input_files
        args += [output_filename]
        exit_status = subprocess.call(args)
        if exit_status == 0:
            print 'wrote %s' % output_filename
            shutil.rmtree(self.output_dir)
            return output_filename
        else:
            print 'error writing %s' % output_filename
