from derpconf.config import Config
from os import path

Config.define('FRAME_WIDTH',
              '320',
              'Width of video frames',
              'General')

Config.define('BLUR_KERNEL_WIDTH',
              '21',
              'Width of blur filter for input normalisation (must be odd)',
              'Input')

Config.define('BLUR_KERNEL_HEIGHT',
              '21',
              'Height of blur filter for input normalisation (must be odd)',
              'Input')

Config.define('MIN_CHANGE_THRESHOLD',
              '50',
              'Pixel value change threshold for detection events',
              'Detection')

Config.define('MIN_CHANGE_AREA',
              '400',
              'Minimum number of changed pixels for detection events',
              'Detection')

Config.define('OUTPUT_FPS',
              '5',
              'Frames per second of output video',
              'Output')

Config.define('MAX_RECORDING_SECONDS',
              '20',
              'Maximum number of seconds to record',
              'Output')

Config.allow_environment_variables()

config = Config()

def get(key):
    return config.get(key)
