import cv2
from datetime import datetime
from os import path, rmdir
from glob import glob
from sauron import config
import shutil
import subprocess
import tempfile

class Recording(object):

    @classmethod
    def prepare(cls, background):
        output_dir = tempfile.mkdtemp()
        recording = cls(output_dir)
        recording.write_frame(background)
        return recording

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.frame_delay = 1.0 / config.get('OUTPUT_FPS')

    def write_frame(self, frame, rects = ()):
        image = self.overlay(frame.raw.copy(), rects)
        self.write_image(image, frame.datetime.strftime('%Y%m%d%H%M%S%f'))
        self.last_write_time = frame.time

    def should_write(self, frame):
        return (not self.last_write_time) or \
            (frame.time - self.last_write_time >= self.frame_delay)

    def write_image(self, image, seq):
        output_path = path.join(self.output_dir, seq + '.jpg')
        print 'writing %s' % output_path
        cv2.imwrite(output_path, image)

    def overlay(self, image, rects):
        for (x, y, w, h) in rects:
            cv2.rectangle(image,
                          (x, y),
                          (x + w, y + h),
                          color=(0, 0, 255),
                          thickness=2)
        return image

    def finalise(self, name):
        print 'finalising recording'
        input_paths = sorted(glob(path.join(self.output_dir, '*')))
        output_path = path.join('/tmp', name + '.gif')
        args = ['convert',
                '-delay', str(int(100.0 / config.get('OUTPUT_FPS'))),
                '-loop', '0']
        args += input_paths
        args += [output_path]
        exit_status = subprocess.call(args)
        if exit_status == 0:
            print 'wrote %s' % output_path
            shutil.rmtree(self.output_dir)
            return output_path
        else:
            print 'error writing %s' % output_path
