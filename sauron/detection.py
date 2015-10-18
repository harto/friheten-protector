import cv2
from datetime import datetime
from sauron.recording import Recording
from sauron.upload import upload_video

class MotionDetector(object):

    WAITING = 'waiting'
    CAPTURING = 'capturing'

    def __init__(self, frames):
        self.frames = frames

    def detect(self):
        self.background = self.frames.next()
        self.state = self.WAITING
        for frame in self.frames:
            self.process_frame(frame)

    def finish(self):
        if self.state == self.CAPTURING:
            self.finish_recording()

    def process_frame(self, frame):
        diffs = self.background.diffs(frame)
        if len(diffs):
            if self.state == self.WAITING:
                print 'motion detected'
                self.start_recording()
            self.record_frame(frame, diffs)
        else:
            if self.state == self.CAPTURING:
                self.finish_recording()

    def start_recording(self):
        self.recording = Recording.prepare()
        self.recording.write_frame(self.background)
        self.state = self.CAPTURING
        print 'recording...'

    def record_frame(self, frame, diffs):
        if not self.recording.should_write(frame): return
        for diff in diffs: frame.overlay_rect(diff)
        frame.overlay_timestamp()
        self.recording.write_frame(frame)

    def finish_recording(self):
        name = datetime.now().strftime('recording-%Y%m%d%H%M%S')
        video_path = self.recording.finalise(name)
        try:
            upload_video(video_path)
        except Exception as e:
            # Don't crash on upload failure
            print 'upload error: %s' % e
        self.state = self.WAITING
