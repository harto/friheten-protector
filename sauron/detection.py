import cv2
from sauron.recording import Recording
from sauron.upload import upload_video

class MotionDetector(object):

    WAITING = 'waiting'
    CAPTURING = 'capturing'

    def __init__(self, frames):
        self.frames = frames

    def detect(self):
        self.background = self.frames.next()
        self.state = WAITING
        for frame in self.frames:
            self.process_frame(frame)

    def process_frame(self, frame):
        diffs = self.background.diffs(frame)
        if len(diffs):
            if self.state == WAITING:
                self.start_recording()
            if self.should_record(frame):
                self.recording.write(frame, diffs)
        else:
            if self.state == CAPTURING:
                self.finish_recording()

    def start_recording(self, frame):
        self.state = CAPTURING
        self.recording = Recording.initialise(self.background, frame)

    def finish_recording(self):
        video_path = self.recording.finalise()
        try:
            upload_video(video_path)
        except:
            # Don't crash on upload failure
            pass
        self.state = 'waiting'
