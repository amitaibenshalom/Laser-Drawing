"""
Filename: consts.py
Purpose: Constants for the car plotter exhibit
"""
import os

# serial communication values
BAUDRATE = 115200

# screen dimensions
VIEWPORT = (800, 600)  # default viewport size
FULLSCREEN = True  # if True, the game will run in fullscreen mode (ignoring the viewport size)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BACKGROUND_COLOR = WHITE
CUTTING_AREA_COLOR = WHITE
COLOR_OUTSIDE_BORDER = (226, 233, 241)


# drawing values
DRAWING_COLOR = RED
DRAWING_WIDTH = 10
MIN_DISTANCE_BETWEEN_POINTS = 10
MAX_LENGTH = 3000

# frame values
FRAME_COLOR = BLACK
FRAME_WIDTH = 10

# assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")  # directory where the assets are stored

# logging values
LOG_FOLDER = os.path.join(os.path.dirname(__file__), "logs")  # get the path of the logs folder
MAX_SIZE_PER_LOG_FILE = 1 * 1024 * 1024  # 1MB
BACKUP_COUNT = 10  # max number of log files, if all 10 are full, the first one will be deleted, rotating the rest 

# idle
IDLE_TIME = 100 # seconds


# laser values
# MAX_TIME_WAITING_FOR_ARDUINO = 5  # seconds
# MAX_DRAWING_TIME_FOR_ARDUINO = 150  # seconds
# time_delay_arduino = 0.005  # seconds

# LASER_POWER = 255  # (0 <= x <= 255)
# CONTOUR_POWER = 255  # (0 <= x <= 255)
# LASER_OFF_RATE = 6
# LASER_ON_RATE = 6
# CONTOUR_RATE = 50 # for green/yellow paper
# MAX_DC_MOTOR_TIME = 1.5  # seconds

# mm_per_pulse = [2*80.0/800, 2*80.0/800]  # mm per pulse for each motor
# board_size = [83.0, 83.0]  # size of the board in mm
# screen_scale = [board_size[0]/cuttingAreaWidth, board_size[1]/cuttingAreaHeight]  # scale from the screen to the board on arduino in mm per pixel
# pulse_per_pixel = [screen_scale[0]/mm_per_pulse[0], screen_scale[1]/mm_per_pulse[1]]  # pulse per pixel for each motor

# starting_key = -2
# next_curve_key = -3
# end_key = -4

# found_arduino = False
# send_to_arduino = False
# drawing_curve = False
# curve_index = 0
# waiting = [False,False]  # two flags to indicate if we are waiting for the arduino to send us data: first is reading a curve, second is drawing one
# last_time = [0, 0]  # to limit the time we wait for the arduino to send us data
