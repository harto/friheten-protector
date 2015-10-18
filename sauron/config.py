from derpconf.config import Config
from os import path

Config.define('FRAME_WIDTH', 320, 'Width of video frames', 'General')

Config.define('BLUR_KERNEL', (21, 21), 'Size of blur filter for input normalisation (must be odd numbers)', 'Input')

Config.define('MIN_CHANGE_THRESHOLD', 50, 'Pixel value change threshold for detection events', 'Detection')
Config.define('MIN_CHANGE_AREA', 400, 'Minimum number of changed pixels for detection events', 'Detection')

Config.define('OUTPUT_FPS', 5, 'Frames per second of output video', 'Output')
Config.define('MAX_RECORDING_SECONDS', 20, 'Maximum number of seconds to record', 'Output')

_config = None

def get(key):
    return _config.get(key)

def init(path=None):
    global _config
    if path is None:
        _config = Config()
    else:
        _config = Config.load(path)
