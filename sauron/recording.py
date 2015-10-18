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
    def prepare(cls):
        output_dir = tempfile.mkdtemp()
        print 'writing frames to %s' % output_dir
        recording = cls(output_dir)
        return recording

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.first_write_time = None
        self.last_write_time = None

    def write_frame(self, frame):
        self.write_image(frame.raw, frame.datetime.strftime('%Y%m%d%H%M%S%f'))
        if not self.first_write_time:
            self.first_write_time = frame.time
        self.last_write_time = frame.time

    def should_write(self, frame):
        return not (self.exceeds_max_fps(frame) or self.exceeds_max_duration(frame))

    def exceeds_max_fps(self, frame):
        return self.last_write_time and \
            frame.time - self.last_write_time < 1.0 / config.get('OUTPUT_FPS')

    def exceeds_max_duration(self, frame):
        return self.first_write_time and \
            frame.time - self.first_write_time > config.get('MAX_RECORDING_SECONDS')

    def write_image(self, image, seq):
        output_path = path.join(self.output_dir, seq + '.jpg')
        #print 'writing %s' % output_path
        cv2.imwrite(output_path, image)

    def finalise(self, name):
        print 'finalising recording'
        input_paths = sorted(glob(path.join(self.output_dir, '*')))
        output_path = path.join(tempfile.gettempdir(), name + '.gif')
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
