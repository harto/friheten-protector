import cv2
import time

def init_cam():
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    cam.read()
    return cam

def benchmark(f):
    fps = 0
    last_report_time = time.time()
    while True:
        f()
        fps += 1
        now = time.time()
        if now - last_report_time >= 1.0:
            print 'fps=%d' % fps
            fps = 0
            last_report_time = now

def benchmark_capture():
    print 'benchmarking raw capture'
    cam = init_cam()
    def raw_capture():
        cam.read()
    benchmark(raw_capture)

def benchmark_resize():
    print 'benchmarking capture, resize'
    from sauron.capture import downscale
    cam = init_cam()
    def capture_and_resize():
        _, img = cam.read()
        downscale(img, 320)
    benchmark(capture_and_resize)

def benchmark_preprocess():
    print 'benchmarking capture, preprocess'
    from sauron.capture import process
    cam = init_cam()
    def capture_and_preprocess():
        _, img = cam.read()
        process(img)
    benchmark(capture_and_preprocess)

if __name__ == '__main__':
    import sauron.config
    sauron.config.init()
    benchmark_preprocess()
