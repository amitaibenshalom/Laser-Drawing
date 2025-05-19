"""
Filename: consts.py
Purpose: Constants for the car plotter exhibit
"""
import os

# serial communication values
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

# screen dimensions
VIEWPORT = (800, 600)  # default viewport size
FULLSCREEN = False  # if True, the game will run in fullscreen mode (ignoring the viewport size)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLOR_OUTSIDE_BORDER = (226, 233, 241)
CUTTING_AREA_COLOR = WHITE

# assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")  # directory where the assets are stored

# dict of picture names, their sizes and position to load on screen
PICTURES_TO_LOAD = {
    "background.png": (("full", "full"), (0, 0)),
    "grid.png": (("70%", "70%"),("25%", "25%")),
}

# logging values
LOG_FOLDER = os.path.join(os.path.dirname(__file__), "logs")  # get the path of the logs folder
MAX_SIZE_PER_LOG_FILE = 1 * 1024 * 1024  # 1MB
BACKUP_COUNT = 10  # max number of log files, if all 10 are full, the first one will be deleted, rotating the rest 
