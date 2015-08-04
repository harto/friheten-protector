from derpconf.config import Config
from os import path

Config.define('FRAME_WIDTH', 500, 'Width of video frames', 'General')

Config.define('BLUR_KERNEL', (21, 21), 'Size of blur filter for input normalisation (must be odd numbers)', 'Input')

Config.define('MIN_CHANGE_THRESHOLD', 50, 'Pixel value change threshold for detection events', 'Detection')
Config.define('MIN_CHANGE_AREA', 400, 'Minimum number of changed pixels for detection events', 'Detection')

Config.define('OUTPUT_DIR', path.join(path.dirname(__file__), '..', 'tmp'), 'Directory to store captures in', 'Output')
Config.define('OUTPUT_FPS', 24, 'Frames per second of output video', 'Output')
Config.define('OUTPUT_FORMAT', 'MJPG', 'Four character code of output video format', 'Output')

_config = None

def get(key):
    return _config.get(key)

def init(path=None):
    global _config
    if path is None:
        _config = Config()
    else:
        _config = Config.load(path)
