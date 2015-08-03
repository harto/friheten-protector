from derpconf.config import Config
from os import path

Config.define('INPUT_FRAME_WIDTH', 500, 'Downscaled width of input frames', 'Input')
Config.define('BLUR_KERNEL', (21, 21), 'Size of blur filter for input normalisation (must be odd numbers)', 'Input')

Config.define('MIN_CHANGE_THRESHOLD', 50, 'Pixel value change threshold for detection events', 'Detection')
Config.define('MIN_CHANGE_AREA', 500, 'Minimum number of changed pixels for detection events', 'Detection')

Config.define('OUTPUT_FRAME_SIZE', (500, 375), 'Width of output frames', 'Output')
Config.define('OUTPUT_FPS', 24, 'Frames per second of output video', 'Output')
Config.define('OUTPUT_FORMAT', 'MPEG', 'Four character code of output video format', 'Output')

_config = None

def get(key):
    return _config.get(key)

def init(path=None):
    global _config
    if path is None:
        _config = Config()
    else:
        _config = Config.load(path)
