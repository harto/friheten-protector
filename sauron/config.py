from derpconf.config import Config
from os import path

Config.define('INPUT_FRAME_WIDTH', 500, 'Downscaled width of input frames', 'Input')
Config.define('BLUR_KERNEL_SIZE', 20, 'Size of blur filter for input normalisation', 'Input')
Config.define('MIN_CHANGE_THRESHOLD', 50, 'Pixel value change threshold for detection events', 'Detection')
Config.define('MIN_CHANGE_AREA', 500, 'Minimum number of changed pixels for detection events', 'Detection')
Config.define('OUTPUT_FRAME_WIDTH', 500, 'Width of output frames', 'Output')
Config.define('OUTPUT_FPS', 24, 'Frames per second of output video', 'Output')
Config.define('OUTPUT_FORMAT', 'MPEG', 'Four character code of output video format', 'Output')

def load_config(path):
    conf = Config.load(path)

# root_dir = path.join(path.dirname(__file__), '..')
# config_path = path.join(root_dir, 'sauron.conf')
