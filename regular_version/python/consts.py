import pygame
import os
from pygame.locals import *


# serial communication values
port = '/dev/ttyUSB0'
baudrate = 115200

# colors
gray = (100, 100, 100)
lightgray = (180, 180, 180)
verylightgray = (220, 220, 220)
red = (255, 0, 0)
pink = (255, 0, 255)
light_red = (255, 100, 100)
green = (0, 255, 0)
purple = (255, 0, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
brown = (139, 69, 19)
orange = (255, 165, 0)
button_color = (199, 33, 47)
button_pressed_color = (242, 188, 27)
colorOutSideBorder = (226, 233, 241)
cuttingAreaColor = white
bgColor = white

# screen_width = 1000
# screen_height = 600
const_width_screen = 1366  # DO NOT CHANGE - for calculations of proportional sizes
const_height_screen = 768  # DO NOT CHANGE - for calculations of proportional sizes
saved_image_width, saved_image_height = 720, 480

pygame.init()
infoObject = pygame.display.Info()
print(infoObject)
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screenColor = gray

# logging values
log_name = "log.txt"
log_dir = "logs"
currentDir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(currentDir, log_dir)):
    os.makedirs(os.path.join(currentDir, log_dir))
LOG_FILE_PATH = os.path.join(currentDir, log_dir, log_name)

# borderLineHeight = int(142 / const_height_screen * screen_height)
borderLineHeight = int(142 / const_height_screen * screen_height)
# borderLine2Height = int((const_height_screen - 142) / const_height_screen * screen_height)
borderLine2Height = screen_height-int(60/const_height_screen*screen_height)
borderLineX = int(130 / const_width_screen * screen_width)
# borderLine2X = int((const_width_screen - 330) / const_width_screen * screen_width)
borderLine2X = int((const_width_screen - 385) / const_width_screen * screen_width)
centerInsideBorders = (int((borderLineX + borderLine2X) / 2), int((borderLineHeight + borderLine2Height) / 2))
center = (int(screen_width / 2), int(screen_height / 2))

# cuttingAreaColor = white
cuttingAreaWidth = int((const_height_screen - 142) / const_height_screen * screen_height) - int(142 / const_height_screen * screen_height)
cuttingAreaHeight = cuttingAreaWidth
cuttingAreaPos = (centerInsideBorders[0] - cuttingAreaWidth / 2, centerInsideBorders[1] - cuttingAreaHeight / 2)
cuttingAreaSize = (cuttingAreaWidth, cuttingAreaHeight)

# red border values
redBorderWidth = int(10 / const_width_screen * screen_width)
redBorderPos = (borderLineX, borderLineHeight)
redBorderSize = (borderLine2X - borderLineX, borderLine2Height - borderLineHeight)
redBorderColor = red

drawingAreaPos = (borderLineX + redBorderWidth, borderLineHeight + redBorderWidth)
drawingAreaSize = (borderLine2X - borderLineX - 2* redBorderWidth, borderLine2Height - borderLineHeight - 2*redBorderWidth)
drawingAreaColor = white

# mm_per_pixel_x = 295/1366
# mm_per_pixel_y = 165/768
pixel_per_cm_screen = 90 / 1.9

# bezier curve values
curveColor = red
# selectedCurveColor = green
curveWidth = int(6 / const_width_screen * screen_width)
min_distance_between_points = 10
max_length = 3000

# contour values
contourColor = black
contourWidth = int(8 / const_width_screen * screen_width)

# button values
buttonInactiveColour = yellow
buttonHoverColour = red
buttonPressedColour = green
buttonOfflineColour = gray

button_height0 = 1.3
button_contour_height0 = 1.7
button_height = int(button_height0 / 16.5 * screen_height)
# sizes of buttons and images
buttonAddSize = (int(7.2 / 29.5 * screen_width), button_height)
buttonDeleteSize = (int(4.5 / 29.5 * screen_width), button_height)
buttonInfoSize = (int(button_contour_height0 / 16.5 * screen_height), int(button_contour_height0 / 16.5 * screen_height))
buttonPreviewSize = (int(7.2 / 29.5 * screen_width), button_height)
buttonPrintSize = (int(4.5 / 29.5 * screen_width), button_height)
buttonHeartSize = buttonInfoSize
buttonDropSize = buttonInfoSize
buttonSquareSize = buttonInfoSize
buttonLettersSize = (int(1 / 16.5 * screen_height), int(1 / 16.5 * screen_height))
buttonLettersLeftSize = buttonLettersSize
buttonLettersRightSize = buttonLettersSize

infoHebSize = (int(18.5 / 29.5 * screen_width), int(12.2 / 16.5 * screen_height))
# infoEngSize = infoHebSize
# infoArabSize = infoHebSize
textAboveSize = (int(14 / 29.5 * screen_width), int(3 / 16.5 * screen_height))
textFrameSize = buttonHeartSize

button_contour_x = int(0.5 / 29.5 * screen_width)
button_operation_x = int(29 / 29.5 * screen_width)
button_operation_x0 = 5
# positions of the buttons
buttonAddPosition = (button_operation_x - buttonAddSize[0], int(button_operation_x0 / 16.5 * screen_height))
buttonPreviewPosition = (button_operation_x - buttonPreviewSize[0], int((button_operation_x0 + button_height0 + 1) / 16.5 * screen_height))
buttonDeletePosition = (button_operation_x - 1.3*buttonDeleteSize[0], int((button_operation_x0 + 2 * (button_height0 + 1)) / 16.5 * screen_height))
buttonInfoPosition = (button_contour_x, borderLineHeight+int(0.5/16.5 * screen_height))
buttonPrintPosition = (button_operation_x - 1.3*buttonPrintSize[0], int((button_operation_x0 + 3 * (button_height0 + 1)) / 16.5 * screen_height))
buttonHeartPosition = (button_contour_x, int((6 + button_contour_height0 + 0.5) / 16.5 * screen_height))
buttonDropPosition = (button_contour_x, int((6 + 2 * (button_contour_height0 + 0.5)) / 16.5 * screen_height))
buttonSquarePosition = (button_contour_x, int((6 + 3 * (button_contour_height0 + 0.5)) / 16.5 * screen_height))
buttonLettersPosition = (buttonAddPosition[0] + 0.5*(buttonAddSize[0]-buttonLettersSize[0]), int((button_operation_x0 - 0.3) / 16.5 * screen_height)-buttonLettersSize[1])
buttonLettersLeftPosition = (buttonLettersPosition[0] - 1.5*buttonLettersSize[0], buttonLettersPosition[1])
buttonLettersRightPosition = (buttonLettersPosition[0] + 1.5*buttonLettersSize[0], buttonLettersPosition[1])
textAbovePosition = (centerInsideBorders[0]-textAboveSize[0]/2, borderLineHeight-textAboveSize[1])
textFramePosition = (buttonHeartPosition[0], buttonHeartPosition[1]-textFrameSize[0])

# get the image from the directory "pictures"
pic_buttonDelete = pygame.image.load("pictures/buttonDelete.jpg")
pic_buttonPressedDelete = pygame.image.load("pictures/buttonPressedDelete.jpg")
pic_buttonInfo = pygame.image.load("pictures/buttonInfo.jpg")
pic_buttonPressedInfo = pygame.image.load("pictures/buttonPressedInfo.jpg")
pic_buttonAdd = pygame.image.load("pictures/buttonAdd.jpg")
pic_buttonPressedAdd = pygame.image.load("pictures/buttonPressedAdd.jpg")
pic_buttonPreview = pygame.image.load("pictures/buttonPreview.jpg")
pic_buttonPressedPreview = pygame.image.load("pictures/buttonPressedPreview.jpg")
pic_buttonPrint = pygame.image.load("pictures/buttonPrint.jpg")
pic_buttonPressedPrint = pygame.image.load("pictures/buttonPressedPrint.jpg")
pic_buttonOffPrint = pygame.image.load("pictures/buttonOffPrint.jpg")
pic_bg0 = pygame.image.load("pictures/vertical_bg_0.jpg")
pic_bg1 = pygame.image.load("pictures/bgWithButtons.jpg")
pic_infoHeb = pygame.image.load("pictures/infoHeb2.jpg")
# pic_infoEng = pygame.image.load("pictures/infoEng.jpg")
# pic_infoArab = pygame.image.load("pictures/infoArab.jpg")
pic_buttonHeart = pygame.image.load("pictures/buttonHeart.jpg")
pic_buttonPressedHeart = pygame.image.load("pictures/buttonPressedHeart.jpg")
pic_buttonDrop = pygame.image.load("pictures/buttonDrop.jpg")
pic_buttonPressedDrop = pygame.image.load("pictures/buttonPressedDrop.jpg")
pic_buttonSquare = pygame.image.load("pictures/buttonSquare.jpg")
pic_buttonPressedSquare = pygame.image.load("pictures/buttonPressedSquare.jpg")
# pic_buttonLetters = pygame.image.load("pictures/buttonLetters.jpg")
# pic_buttonPressedLetters = pygame.image.load("pictures/buttonPressedLetters.jpg")
pic_buttonLettersLeft = pygame.image.load("pictures/left_arrow.png")
pic_buttonPressedLettersLeft = pygame.image.load("pictures/left_arrow.png")
pic_buttonLettersRight = pygame.image.load("pictures/right_arrow.png")
pic_buttonPressedLettersRight = pygame.image.load("pictures/right_arrow.png")
pic_doubleArrow = pygame.image.load("pictures/double_arrow.png")
pic_textAbove = pygame.image.load("pictures/textAbove2.jpg")
pic_textFrame = pygame.image.load("pictures/frame.jpg")

# load the images of the letters and transform them to the right size
pic_letters = []
for i in range(0, 27):
    pic_letters.append(pygame.image.load("pictures/letters/" + str(i) + ".png"))
    pic_letters[2*i] = pygame.transform.scale(pic_letters[2*i], buttonLettersSize)
    pic_letters.append(pygame.image.load("pictures/letters/" + str(i) + "_pressed.png"))
    pic_letters[2*i+1] = pygame.transform.scale(pic_letters[2*i+1], buttonLettersSize)

# resize the images
pic_buttonDelete = pygame.transform.scale(pic_buttonDelete, buttonDeleteSize)
pic_buttonPressedDelete = pygame.transform.scale(pic_buttonPressedDelete, buttonDeleteSize)
pic_buttonInfo = pygame.transform.scale(pic_buttonInfo, buttonInfoSize)
pic_buttonPressedInfo = pygame.transform.scale(pic_buttonPressedInfo, buttonInfoSize)
pic_buttonAdd = pygame.transform.scale(pic_buttonAdd, buttonAddSize)
pic_buttonPressedAdd = pygame.transform.scale(pic_buttonPressedAdd, buttonAddSize)
pic_buttonPreview = pygame.transform.scale(pic_buttonPreview, buttonPreviewSize)
pic_buttonPressedPreview = pygame.transform.scale(pic_buttonPressedPreview, buttonPreviewSize)
pic_buttonPrint = pygame.transform.scale(pic_buttonPrint, buttonPrintSize)
pic_buttonPressedPrint = pygame.transform.scale(pic_buttonPressedPrint, buttonPrintSize)
pic_buttonOffPrint = pygame.transform.scale(pic_buttonOffPrint, buttonPrintSize)
pic_bg0 = pygame.transform.scale(pic_bg0, (screen_width, screen_height))
pic_bg1 = pygame.transform.scale(pic_bg1, (screen_width, screen_height))
pic_infoHeb = pygame.transform.scale(pic_infoHeb, infoHebSize)
# pic_infoEng = pygame.transform.scale(pic_infoEng, infoEngSize)
# pic_infoArab = pygame.transform.scale(pic_infoArab, infoArabSize)
pic_buttonHeart = pygame.transform.scale(pic_buttonHeart, buttonHeartSize)
pic_buttonPressedHeart = pygame.transform.scale(pic_buttonPressedHeart, buttonHeartSize)
pic_buttonDrop = pygame.transform.scale(pic_buttonDrop, buttonDropSize)
pic_buttonPressedDrop = pygame.transform.scale(pic_buttonPressedDrop, buttonDropSize)
pic_buttonSquare = pygame.transform.scale(pic_buttonSquare, buttonSquareSize)
pic_buttonPressedSquare = pygame.transform.scale(pic_buttonPressedSquare, buttonSquareSize)
pic_buttonLetters = pygame.transform.scale(pic_letters[0], buttonLettersSize)
pic_buttonPressedLetters = pygame.transform.scale(pic_letters[1], buttonLettersSize)
pic_buttonLettersLeft = pygame.transform.scale(pic_buttonLettersLeft, buttonLettersLeftSize)
pic_buttonPressedLettersLeft = pygame.transform.scale(pic_buttonPressedLettersLeft, buttonLettersLeftSize)
pic_buttonLettersRight = pygame.transform.scale(pic_buttonLettersRight, buttonLettersRightSize)
pic_buttonPressedLettersRight = pygame.transform.scale(pic_buttonPressedLettersRight, buttonLettersRightSize)
pic_textAbove = pygame.transform.scale(pic_textAbove, textAboveSize)
pic_textFrame = pygame.transform.scale(pic_textFrame, textFrameSize)

x_length = 16
x_height = 15 # height from the top of the heart downwards
contour_heart = [[(screen_width / 2 - int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 - int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width / 2 + int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 + int(x_length / const_width_screen * screen_width), int((250 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((250 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width / 2, int(600 / const_height_screen * screen_height)),
                  (int(1145 / const_width_screen * screen_width), int(345 / const_height_screen * screen_height)), (
                  screen_width / 2 + (int(120 / const_width_screen * screen_width)),
                  int(80 / const_height_screen * screen_height)),
                  (screen_width / 2, int(250 / const_height_screen * screen_height))],
                 [(screen_width / 2, int(250 / const_height_screen * screen_height)), (
                 screen_width / 2 - int(120 / const_width_screen * screen_width),
                 int(80 / const_height_screen * screen_height)),
                  (int(225 / const_width_screen * screen_width), int(345 / const_height_screen * screen_height)),
                  (screen_width / 2, int(600 / const_height_screen * screen_height))]]
square_side = [int(193 / const_width_screen * screen_width),int(193 / const_width_screen * screen_width)]
x_height = int(60/const_width_screen * screen_width)
x_length = int(24/const_width_screen * screen_width)
contour_square = [[[screen_width / 2 - square_side[0] + x_height - x_length, screen_height/2-square_side[1] + x_height],
                   [screen_width / 2 - square_side[0] + x_height + x_length, screen_height/2-square_side[1] + x_height],
                   [screen_width / 2 - square_side[0] + x_height - x_length, screen_height/2-square_side[1] + x_height],
                   [screen_width / 2 - square_side[0] + x_height + x_length, screen_height/2-square_side[1] + x_height]],
                [[screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height - x_length],
                   [screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height + x_length],
                   [screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height - x_length],
                   [screen_width / 2 - square_side[0] + x_height, screen_height/2-square_side[1] + x_height + x_length]],
                [[screen_width / 2, screen_height / 2 + square_side[1]],
                   [screen_width / 2 + square_side[0],
                    screen_height / 2 + square_side[1]],
                   [screen_width / 2 + square_side[0],
                    screen_height / 2 + square_side[1]],
                   [screen_width / 2 + square_side[0],
                    screen_height / 2]], [
                      [screen_width / 2 + square_side[0],
                       screen_height / 2],
                      [screen_width / 2 + square_side[0],
                       screen_height / 2 - square_side[1]],
                      [screen_width / 2 + square_side[0],
                       screen_height / 2 - square_side[1]],
                      [screen_width / 2, screen_height / 2 - square_side[1]]],
                  [[screen_width / 2, screen_height / 2 - square_side[1]],
                   [screen_width / 2 - square_side[0],
                    screen_height / 2 - square_side[1]],
                   [screen_width / 2 - square_side[0],
                    screen_height / 2 - square_side[1]],
                   [screen_width / 2 - square_side[0],
                    screen_height/2]], [
                      [screen_width / 2 - square_side[0],
                       screen_height / 2],
                      [screen_width / 2 - square_side[0],
                       screen_height / 2 + square_side[1]],
                      [screen_width / 2 - square_side[0],
                       screen_height / 2 + square_side[1]],
                      [screen_width / 2, screen_height / 2 + square_side[1]]]]
x_height = 35
x_length = 16
contour_drop = [[(screen_width / 2 - int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 - int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 + int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width / 2 + int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height)),
                  (screen_width / 2 + int(x_length / const_width_screen * screen_width), int((145 + x_height) / const_height_screen * screen_height)),
                  (screen_width/2 - int(x_length / const_width_screen * screen_width),int((145 + x_height + 2*x_length) / const_height_screen * screen_height))],
                [(screen_width/2, int(610 / const_height_screen * screen_height)),
                 (screen_width/2 + int(62 / const_width_screen * screen_width), int(610 / const_height_screen * screen_height)),
                 (screen_width/2 + int(184 / const_width_screen * screen_width), int(550 / const_height_screen * screen_height)),
                 (screen_width/2 + int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height))],
                [(screen_width/2 + int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height)),
                 (screen_width/2 + int(184 / const_width_screen * screen_width), int(263 / const_height_screen * screen_height)),
                 (screen_width/2 + int(43 / const_width_screen * screen_width), int(170 / const_height_screen * screen_height)),
                 (screen_width/2, int(145 / const_height_screen * screen_height))],
                [(screen_width/2, int(145 / const_height_screen * screen_height)),
                 (screen_width/2 - int(43 / const_width_screen * screen_width), int(170 / const_height_screen * screen_height)),
                 (screen_width/2 - int(184 / const_width_screen * screen_width), int(263 / const_height_screen * screen_height)),
                 (screen_width/2 - int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height))],
                [(screen_width/2 - int(184 / const_width_screen * screen_width), int(407 / const_height_screen * screen_height)),
                 (screen_width/2 - int(184 / const_width_screen * screen_width), int(550 / const_height_screen * screen_height)),
                 (screen_width/2 - int(62 / const_width_screen * screen_width), int(610 / const_height_screen * screen_height)),
                 (screen_width/2, int(610 / const_height_screen * screen_height))]]

contours = [contour_heart, contour_square, contour_drop]

# move the conour heart to the center inside the borders
for k in range(len(contours)):
    for i in range(len(contours[k])):
        for j in range(len(contours[k][i])):
            contours[k][i][j] = (
            contours[k][i][j][0] + int(centerInsideBorders[0] - center[0]),
            contours[k][i][j][1] + int(centerInsideBorders[1] - center[1]))

buttons_enabled = True
IS_MOVING_ALL_CURVE = True
IDLE_TIME = 100 # seconds
IDLE_TIME_DRAW = 120 # seconds
enable_idle_drawing = False
idle_mode = False
MAX_RUNS = 60

SHOW_RED_BORDER = True

# laser values
MAX_TIME_WAITING_FOR_ARDUINO = 5  # seconds
MAX_DRAWING_TIME_FOR_ARDUINO = 150  # seconds
time_delay_arduino = 0.005  # seconds

LASER_POWER = 255  # (0 <= x <= 255)
CONTOUR_POWER = 255  # (0 <= x <= 255)
LASER_OFF_RATE = 6
LASER_ON_RATE = 6
CONTOUR_RATE = 50 # for green/yellow paper
MAX_DC_MOTOR_TIME = 1.5  # seconds

mm_per_pulse = [2*80.0/800, 2*80.0/800]  # mm per pulse for each motor
board_size = [83.0, 83.0]  # size of the board in mm
screen_scale = [board_size[0]/cuttingAreaWidth, board_size[1]/cuttingAreaHeight]  # scale from the screen to the board on arduino in mm per pixel
pulse_per_pixel = [screen_scale[0]/mm_per_pulse[0], screen_scale[1]/mm_per_pulse[1]]  # pulse per pixel for each motor

starting_key = -2
next_curve_key = -3
end_key = -4

found_arduino = False
send_to_arduino = False
drawing_curve = False
curve_index = 0
waiting = [False,False]  # two flags to indicate if we are waiting for the arduino to send us data: first is reading a curve, second is drawing one
last_time = [0, 0]  # to limit the time we wait for the arduino to send us data
