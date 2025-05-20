"""
Filename: regular_drawing.py
Purpose: This file is the main file of the program. It is responsible for the GUI and the main logic of the program.
Author: A.B.S
"""

import math
import logging
import serial
import struct
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

from consts import *
from Button import *
from BezierCurve import *
from basic_routines import *


# logging setup
logging.basicConfig(filename=LOG_FILE_PATH, filemode='a', level=logging.INFO)
handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=37500, backupCount=100)
logger = logging.getLogger("Rotating Log")
formatter = logging.Formatter('%(asctime)s.%(msecs)03d;%(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.propagate = False
logger.addHandler(handler)
logger.info('--------------- PROGRAM START ---------------')


# arduino setup
arduino = None

try:
    arduino = serial.Serial(port, baudrate)
    found_arduino = True
    print("Found Arduino")
    logger.info('Found Arduino')

except Exception as e:
    print(f"Serial port error: {e}")
    print('ARDUINO NOT CONNECTED')
    logger.error('Arduino not connected')

# fonts for text
font_style2 = pygame.font.SysFont("calibri", 45)
font_style2.bold = True
font_style = pygame.font.SysFont("calibri", 30)
font_style.bold = True


def insert_drawing_to_surface(surf):
    global curves
    global contour
    for i in range(len(curves)):
        new_curve = BezierCurve(
            [int((curves[i].vertices[0][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((curves[i].vertices[0][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            [int((curves[i].vertices[1][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((curves[i].vertices[1][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            [int((curves[i].vertices[2][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((curves[i].vertices[2][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            [int((curves[i].vertices[3][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((curves[i].vertices[3][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            False, curveColor, curveWidth)
        new_curve.draw(surf)
    for i in range(len(contour)):
        new_curve = BezierCurve(
            [int((contour[i].vertices[0][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((contour[i].vertices[0][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            [int((contour[i].vertices[1][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((contour[i].vertices[1][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            [int((contour[i].vertices[2][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((contour[i].vertices[2][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            [int((contour[i].vertices[3][0] - borderLineX) / (borderLine2X - borderLineX) * saved_image_width),
             int((contour[i].vertices[3][1] - borderLineHeight) / (
                     borderLine2Height - borderLineHeight) * saved_image_height)],
            False, contourColor, contourWidth)
        new_curve.draw(surface=surf)


def save_drawing_img():
    # saving_surface = pygame.Surface((saved_image_width, saved_image_height))
    # saving_surface.fill(bgColor)
    # insert_drawing_to_surface(saving_surface)
    currentDirectory = os.getcwd()
    drawings_dir = os.path.join(currentDirectory, r'drawings')
    if not os.path.exists(drawings_dir):
        os.makedirs(drawings_dir)
    # save the image with the current date and time in the folder drawings_dir png format
    # saving surface is only the drawing in the cutting area (cuttingAreaPos and cuttingAreaSize)
    rect = pygame.Rect(cuttingAreaPos[0], cuttingAreaPos[1], cuttingAreaSize[0], cuttingAreaSize[1])
    saving_surface = screen.subsurface(rect)
    pygame.image.save(saving_surface, os.path.join(drawings_dir, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'))



def check_dc_motor():
    global dc_motor_on
    global last_time_dc_motor
    global ButtonPrint
    global send_to_arduino
    if dc_motor_on:
        if time.time() - last_time_dc_motor > MAX_DC_MOTOR_TIME:
            dc_motor_on = False
            send_to_arduino = False
            ButtonPrint.tempimg = pic_buttonPrint
            ButtonPrint.img = pic_buttonPrint
            ButtonPrint.imgon = pic_buttonPressedPrint


def check_arduino(log_flag=True):
    global curves_to_send
    global waiting
    global last_time
    global drawing_curve
    global curve_index
    global send_to_arduino
    global estimated_time
    global show_estimated_time
    global logger
    global idle_clock_draw
    global idle_clock
    global idle_mode
    global dc_motor_on
    global last_time_dc_motor

    if waiting[1]:
        if arduino.in_waiting > 0:
            received_data = arduino.readline().decode('utf-8').rstrip()
            waiting[1] = False
            print("arduino finished drawing curve " + str(curve_index))
            # if log_flag:
            #     logger.info("arduino finished drawing curve " + str(curve_index))
            curve_index += 1
            if curve_index >= len(curves_to_send):
                dc_motor_on = True
                last_time_dc_motor = time.time()
                # send a key that will tell the arduino to stop reading
                print("sent all curves")
                if log_flag:
                    # logger.info("sent all curves")
                    logger.info("arduino finished drawing all curves successfully")
                send_one_number(end_key)
                print("sent end key for arduino")
                # if log_flag:
                #     logger.info("sent end key for arduino")
                estimated_time = 0
                show_estimated_time = False
                idle_clock = time.time()
                idle_clock_draw = time.time()
                if idle_mode:
                    clear_all(log_flag=False)
                    heart(log_flag=False)
                    add_curve0(log_flag=False)
                return True
            else:
                drawing_curve = False
        elif time.time() - last_time[1] > MAX_DRAWING_TIME_FOR_ARDUINO:
            print("ERROR: arduino didn't send drawing done key")
            logger.error("ERROR: arduino didn't send drawing done key")
            return False
        return True

    if waiting[0]:
        if arduino.in_waiting > 0:
            received_data = arduino.readline().decode('utf-8').rstrip()
            waiting[0] = False
            waiting[1] = True
            last_time[1] = time.time()
            print("arduino finished reading curve " + str(curve_index))
            # if log_flag:
            #     logger.info("arduino finished reading curve " + str(curve_index))
        elif time.time() - last_time[0] > MAX_TIME_WAITING_FOR_ARDUINO:
            print("ERROR: arduino didn't send reading done key")
            logger.error("ERROR: arduino didn't send reading done key")
            return False
        return True

    if not drawing_curve:
        curve = curves_to_send[curve_index]
        send_one_number(len(curve))
        for point in curve:
            send_one_number(point[1])
            send_one_number(point[0])
        # if log_flag:
        #     logger.info("sent curve " + str(curve_index))
        drawing_curve = True
        waiting[0] = True  # waiting for arduino to send key that will tell us it finished reading the curve
        waiting[1] = False  # NOT waiting for arduino to send key that will tell us it finished drawing the curve
        last_time[0] = time.time()
    return True


# send the points as ratio between place and screen size
def send_to_laser(log_flag=True):
    global curves
    global curves_to_send
    global drawing_curve
    global curve_index
    global send_to_arduino
    global ButtonPrint
    global found_arduino
    global contour
    global estimated_time
    global show_estimated_time
    global last_send_time
    global logger
    global idle_mode

    if send_to_arduino:
        return False
    if log_flag:
        logger.info("clicked on print button")

    if not found_arduino:
        print("ERROR: No Laser Connected")
        logger.error("ERROR: No Laser Connected")
        return False
    if len(curves) == 0:
        print("No curves to send")
        # if log_flag:
        #     logger.warning("Clicked on print button with no curves to send")
        return True
    if log_flag:
        logger.info(len(curves))
    save_drawing_img()
    estimated = 0  # estimated time to finish drawing in seconds
    last_send_time = time.time()
    curves_to_send = curves.copy()
    # calculate the estimated time to finish drawing
    last_point = [centerInsideBorders[0] - cuttingAreaWidth / 2, centerInsideBorders[1] - cuttingAreaHeight / 2]
    for curve in curves_to_send:
        estimated += length_of_curve_zigzag(curve) * pulse_per_pixel[0] * LASER_ON_RATE / 1000
        estimated += distance(curve[0], last_point) * pulse_per_pixel[0] * LASER_OFF_RATE / 1000
        last_point = curve.vertices[-1]
    print(f"estimated time to finish drawing (WITHOUT contour): {estimated:.2f} seconds")
    # add all the curves in the contour to curves_to_send
    times = 1  # number of times to draw the contour (usually 1)
    for i in range(times):
        for curve in contour:
            curves_to_send.append(curve.compute_bezier_points())
            estimated += curve.get_length() * pulse_per_pixel[0] * CONTOUR_RATE / 1000
            estimated += distance(curve.vertices[0], last_point) * pulse_per_pixel[0] * LASER_OFF_RATE / 1000
            last_point = curve.vertices[-1]
    print(f"estimated time to finish drawing (with contour): {estimated:.2f} seconds")
    if log_flag:
        logger.info(f"estimated time to finish drawing (with contour): {estimated:.2f} seconds")
    estimated_time = estimated
    show_estimated_time = True
    msgEstimatedTime(estimated_time)
    if not send_one_number(starting_key):  # first, send a key that will tell the arduino to start reading
        return False
    print("sent starting key to laser")
    # if log_flag:
    #     logger.info("sent starting key to laser")
    # then, send the number of curves
    if not send_one_number(-len(curves_to_send)):
        return False
    if not send_one_number(-times * len(contour)):
        return False
    print("sent number of curves and contour")
    # if log_flag:
    #     logger.info("sent number of curves and contour")
    drawing_curve = False
    curve_index = 0
    send_to_arduino = True
    # change the picture of the send to laser button
    ButtonPrint.img = pic_buttonOffPrint
    ButtonPrint.imgon = pic_buttonOffPrint
    ButtonPrint.tempimg = pic_buttonOffPrint
    return True


def send_one_number(value):
    try:
        byte_value = bytearray(struct.pack("f", value))  # Convert float to bytes
        arduino.write(byte_value)
        arduino.flush()
    except Exception:
        print(str(value) + "not sent")
        logger.error(str(value) + "NOT SENT")
        return False
    print("sent " + str(value))
    return True

def in_border(point):
    return borderLineX < point[0] < borderLine2X and borderLineHeight < point[1] < borderLine2Height

def take_control():
    global arduino
    print("taking control over Arduino...")
    logger.info("taking control over Arduino...")
    pytxt = "PY\n"
    try:
        arduino.write(pytxt.encode())
    except:
        print("Error: python failed taking control over arduino - use another serial monitor")
        logger.error("Error: python failed taking control over arduino - use another serial monitor")
        return False
    print("success!")
    logger.info("success!")
    return True


def heart(log_flag=True):
    global contour
    global ButtonSquare
    global ButtonHeart
    global ButtonDrop
    global logger
    ButtonSquare.tempimg = pic_buttonSquare
    ButtonSquare.img = pic_buttonSquare
    ButtonHeart.tempimg = pic_buttonPressedHeart
    ButtonDrop.tempimg = pic_buttonDrop
    ButtonDrop.img = pic_buttonDrop
    contour = []
    for i in range(len(contour_heart)):
        add_contour(contour_heart[i][0], contour_heart[i][1], contour_heart[i][2], contour_heart[i][3])
    if log_flag:
        logger.info("clicked on heart contour")


def sqaure(log_flag=True):
    global contour
    global ButtonSquare
    global ButtonHeart
    global ButtonDrop
    global logger
    ButtonSquare.tempimg = pic_buttonPressedSquare
    ButtonHeart.tempimg = pic_buttonHeart
    ButtonHeart.img = pic_buttonHeart
    ButtonDrop.tempimg = pic_buttonDrop
    ButtonDrop.img = pic_buttonDrop
    contour = []
    for i in range(len(contour_square)):
        add_contour(contour_square[i][0], contour_square[i][1], contour_square[i][2], contour_square[i][3])
    if log_flag:
        logger.info("clicked on square contour")


def drop(log_flag=True):
    global contour
    global ButtonSquare
    global ButtonHeart
    global ButtonDrop
    global logger
    ButtonSquare.tempimg = pic_buttonSquare
    ButtonSquare.img = pic_buttonSquare
    ButtonHeart.tempimg = pic_buttonHeart
    ButtonHeart.img = pic_buttonHeart
    ButtonDrop.tempimg = pic_buttonPressedDrop
    contour = []
    for i in range(len(contour_drop)):
        add_contour(contour_drop[i][0], contour_drop[i][1], contour_drop[i][2], contour_drop[i][3])
    if log_flag:
        logger.info("clicked on drop contour")


def preview(log_flag=True):
    global show_control_lines
    global logger
    global preview_time_start
    show_control_lines = False
    preview_time_start = time.time()
    if log_flag:
        logger.info("clicked on preview")


def add_curve0(log_flag=True):
    pass

#        if log_flag:
#            logger.warning("clicked on add curve button when max curves reached")


def msgNumCurves(num):
    if num > 0:
        value = font_style2.render(f"ורתונ םיווק {round(num)}%", True, black)
    else:
        value = font_style2.render("תומוקע ורתונ אל", True, red)
    text_rect = value.get_rect(center=((borderLine2X + screen_width) / 2, borderLineHeight / 2))
    screen.blit(value, text_rect)


def msgEstimatedTime(time):
    value = font_style.render(f" תוינש {time:.1f} :ךרעומ ןמז ", True, black)
    text_rect = value.get_rect(
        center=((borderLine2X + screen_width) / 2, buttonPrintPosition[1] + 1.5 * buttonPrintSize[1]))
    screen.blit(value, text_rect)


# def msg():
#     global screen
#     value = font_style2.render("!תודוקנה תועצמאב וקה תרוצ תא ונש", True, white)
#     text_rect = value.get_rect(center=(screen_width / 2, 50))
#     screen.blit(value, text_rect)



# clear the LAST curve
def clear(log_flag=True):
    global curves
    global delta_outside
    global logger
    if len(curves) == 0:
        #        if log_flag:
        #            logger.warning("clicked on delete button with no curves on screen")
        return

    curves.pop()


def clear_all(log_flag=True):
    global curves
    global selected_curve
    global selected
    global delta
    global delta_outside
    curves.clear()

def add_curve(log_flag=True):
    pass

def add_contour(p0, p1, p2, p3):
    global contour
    new_contour = BezierCurve(p0, p1, p2, p3, False, contourColor, contourWidth)
    contour.append(new_contour)

def insert_letter():
    pass


def letter_left_arrow():
    pass


def letter_right_arrow():
    pass


def check_idle():
    global idle_mode
    global idle_clock
    global idle_clock_draw
    global sample_index
    global auto_run
    global send_to_arduino
    global logger
    global enable_idle_drawing
    global letter_index
    global ButtonLetters

    if not idle_mode and time.time() - idle_clock > IDLE_TIME and not auto_run and not send_to_arduino:
        idle_mode = True
        logger.info("idle mode triggered")
        heart(log_flag=False)
        clear_all(log_flag=False)
        add_curve0(log_flag=False)
        letter_index = 0
        ButtonLetters.tempimg = pic_letters[0]
        ButtonLetters.img = pic_letters[0]
        ButtonLetters.imgon = pic_letters[1]
        #            idle_clock = time.time()
        idle_clock_draw = time.time()

    if idle_mode and time.time() - idle_clock_draw > IDLE_TIME_DRAW and not auto_run and not send_to_arduino and enable_idle_drawing:
        logger.info("drawing sample number " + str(sample_index))
        clear_all(log_flag=False)
        # insert_sample(sample_index)
        # sample_index += 1
        # if sample_index >= len(samples):
        #     sample_index = 0
        send_to_laser(log_flag=False)
        idle_clock_draw = time.time()
        idle_clock = time.time()


def draw_all(screen):
    global curves
    for curve in curves:
        if len(curve) > 1:
            pygame.draw.lines(screen, curveColor, False, curve, curveWidth)
    if len(current_curve) > 1:
        for p in current_curve:
            pygame.draw.lines(screen, curveColor, False, current_curve, curveWidth)
    for curve in contour:
        curve.draw(screen)


def show_popup():
    global show_picture
    global logger
    global info_time_start
    show_picture = True
    logger.info("clicked on info page")
    info_time_start = time.time()


curves = []  # list of all curves
current_curve = []  # list of points of the current curve
last_point = None  # The last point added to the current curve
contour = []  # list of all contour curves
selected = None  # The currently selected point
show_picture = False
show_estimated_time = False
estimated_time = 0
last_send_time = 0
auto_run = False
run_index = 0
sample_index = 0
letter_index = 0
info_time_start = time.time()
preview_time_start = time.time()
idle_clock = time.time()
idle_clock_draw = time.time()
last_time_dc_motor = time.time()
dc_motor_on = False
red_border_on = False

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# define all the buttons and make an array of them
ButtonAdd = Button(buttonAddPosition, buttonAddSize, buttonInactiveColour, buttonPressedColour, pic_buttonAdd,
                   pic_buttonPressedAdd, add_curve0)
ButtonDelete = Button(buttonDeletePosition, buttonDeleteSize, buttonInactiveColour, buttonPressedColour,
                      pic_buttonDelete, pic_buttonPressedDelete, clear)
ButtonInfo = Button(buttonInfoPosition, buttonInfoSize, buttonInactiveColour, buttonPressedColour, pic_buttonInfo,
                    pic_buttonPressedInfo, show_popup)
ButtonPreview = Button(buttonPreviewPosition, buttonPreviewSize, buttonInactiveColour, buttonPressedColour,
                       pic_buttonPreview, pic_buttonPressedPreview, preview)
ButtonPrint = Button(buttonPrintPosition, buttonPrintSize, buttonInactiveColour, buttonPressedColour, pic_buttonPrint,
                     pic_buttonPressedPrint, send_to_laser)
ButtonHeart = Button(buttonHeartPosition, buttonHeartSize, buttonInactiveColour, buttonPressedColour, pic_buttonHeart,
                     pic_buttonPressedHeart, heart)
ButtonDrop = Button(buttonDropPosition, buttonDropSize, buttonInactiveColour, buttonPressedColour, pic_buttonDrop,
                    pic_buttonPressedDrop, drop)
ButtonSquare = Button(buttonSquarePosition, buttonSquareSize, buttonInactiveColour, buttonPressedColour,
                      pic_buttonSquare, pic_buttonPressedSquare, sqaure)
# ButtonLetters = Button(buttonLettersPosition, buttonLettersSize, buttonInactiveColour, buttonPressedColour,
#                        pic_letters[0], pic_letters[1], insert_letter)
# ButtonLettersLeftArrow = Button(buttonLettersLeftPosition, buttonLettersLeftSize, buttonInactiveColour,
#                                 buttonPressedColour,
#                                 pic_buttonLettersLeft, pic_buttonPressedLettersLeft, letter_left_arrow)
# ButtonLettersRightArrow = Button(buttonLettersRightPosition, buttonLettersRightSize, buttonInactiveColour,
#                                  buttonPressedColour,
#                                  pic_buttonLettersRight, pic_buttonPressedLettersRight, letter_right_arrow)
# buttons = [ButtonAdd, ButtonDelete, ButtonInfo, ButtonPreview, ButtonPrint, ButtonHeart, ButtonDrop, ButtonSquare,
#            ButtonLetters, ButtonLettersLeftArrow, ButtonLettersRightArrow]
buttons = [ButtonAdd, ButtonDelete, ButtonInfo, ButtonPreview, ButtonPrint, ButtonHeart, ButtonDrop, ButtonSquare]

# rotate the square contour 45 degrees
angle = math.radians(45)
for i in range(len(contour_square)):
    for j in range(len(contour_square[i])):
        contour_square[i][j] = rotate_point(contour_square[i][j], angle, centerInsideBorders)


def main():
    global curves
    global selected_curve
    global selected
    global show_control_lines
    global show_picture
    global show_estimated_time
    global last_send_time
    global send_to_arduino
    global found_arduino
    global buttons_enabled
    global arduino
    global auto_run
    global run_index
    global sample_index
    global logger
    global preview_time_start
    global info_time_start
    global idle_clock
    global idle_clock_draw
    global idle_mode
    global red_border_on

    clock = pygame.time.Clock()
    heart(log_flag=False)

    sent_border = False
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                logger.info("PROGRAM ENDED BY USER")
                running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_p:  # if p is pressed then start running the laser automatically
                    auto_run = True
                    run_index = 0
                else:
                    if auto_run:
                        print("auto run stopped after: " + str(run_index) + " runs")
                        logger.info("auto run stopped after: " + str(run_index) + " runs")
                    auto_run = False
                    if event.key == pygame.K_r:
                        clear()
                    elif event.key == pygame.K_c:
                        clear_all()
                    elif event.key == pygame.K_a:
                        # add_curve0()
                        pass
                    elif event.key == pygame.K_s:
                        pass
                        # insert_sample(sample_index)
                        # sample_index += 1
                        # if sample_index >= len(samples):
                        #     sample_index = 0
                    elif event.key == pygame.K_l:
                        insert_letter()
                    elif event.key == pygame.K_LEFT:
                        letter_left_arrow()
                    elif event.key == pygame.K_RIGHT:
                        letter_right_arrow()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        logger.info("PROGRAM ENDED BY USER")
                    else:
                        running = False
                        logger.info("PROGRAM ENDED BY USER")
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                idle_clock = time.time()
                idle_clock_draw = time.time()
                idle_mode = False
                if auto_run:
                    print("auto run stopped after: " + str(run_index) + " runs")
                    logger.info("auto run stopped after: " + str(run_index) + " runs")
                    auto_run = False
                if in_border(pygame.mouse.get_pos()):
                    buttons_enabled = False
                    selected = pygame.mouse.get_pos()

                # for curve in curves:
                #     for p in curve.vertices:
                #         if math.dist(p, event.pos) < toleranceTouch:
                #             if selected is None:
                #                 selected_curve = curve
                #                 selected_curve.color = selectedCurveColor
                #                 selected = p
                #                 buttons_enabled = False
                #             elif math.dist(p, event.pos) < math.dist(selected, event.pos):
                #                 selected_curve.color = curveColor
                #                 selected_curve = curve
                #                 selected_curve.color = selectedCurveColor
                #                 selected = p
                #                 buttons_enabled = False
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                idle_clock = time.time()
                idle_clock_draw = time.time()
                idle_mode = False
                if auto_run:
                    print("auto run stopped after: " + str(run_index) + " runs")
                    logger.info("auto run stopped after: " + str(run_index) + " runs")
                    auto_run = False
                selected = None
                buttons_enabled = True
                # if selected_curve is not None:
                #     selected_curve.color = curveColor
                #     selected_curve = None
                if show_picture:
                    show_picture = False
                    logger.info(
                        "closed info page after " + str(int((time.time() - info_time_start) * 10) / 10.0) + " seconds")
                # if not show_control_lines:
                #     show_control_lines = True
                #     logger.info("closed preview mode after " + str(
                #         int((time.time() - preview_time_start) * 10) / 10.0) + " seconds")
                if len(current_curve) > 1:
                    curves.append(current_curve.copy())
                    print(len(curves[-1]))
                    current_curve.clear()

        total_length = 0
        for curve in curves:
            total_length += length_of_curve(curve)
        total_length += length_of_curve(current_curve)

        point = pygame.mouse.get_pos()
        if selected is not None and total_length < max_length and len(current_curve) == 0 and in_border(point):
            current_curve.append(point)
        elif total_length < max_length and selected is not None and math.dist(current_curve[-1], point) >= min_distance_between_points \
                and in_border(point):
            current_curve.append(point)

        # Draw everything
        screen.fill(bgColor)
        # draw the border rectangles
        pygame.draw.rect(screen, colorOutSideBorder, (0, 0, borderLineX, screen_height))
        pygame.draw.rect(screen, colorOutSideBorder, (borderLine2X, 0, screen_width - borderLine2X, screen_height))
        pygame.draw.rect(screen, colorOutSideBorder, (0, 0, screen_width, borderLineHeight))
        pygame.draw.rect(screen, colorOutSideBorder,
                         (0, borderLine2Height, screen_width, screen_height - borderLine2Height))
        if SHOW_RED_BORDER:
            # for each curve, check if there are any points outside the border
            for curve in curves + [current_curve]:
                for p in curve:
                    if p[0] < borderLineX + redBorderWidth or \
                            p[0] > borderLine2X - redBorderWidth or \
                            p[1] < borderLineHeight + redBorderWidth or \
                            p[1] > borderLine2Height - redBorderWidth:
                        pygame.draw.rect(screen, redBorderColor, (redBorderPos, redBorderSize), 0)
                        pygame.draw.rect(screen, drawingAreaColor, (drawingAreaPos, drawingAreaSize), 0)
                        break

        # draw the text above
        screen.blit(pic_textAbove, textAbovePosition)
        # draw the "frame:" text
        screen.blit(pic_textFrame, textFramePosition)
        # draw a rectangle in the middle of the screen to show the laser cutting area
        pygame.draw.rect(screen, cuttingAreaColor,
                         (cuttingAreaPos[0], cuttingAreaPos[1], cuttingAreaSize[0], cuttingAreaSize[1]))
        draw_all(screen)
        msgNumCurves((max_length - total_length)/max_length * 100)
        if show_picture:
            popup_x = centerInsideBorders[0] - infoHebSize[0] / 2
            popup_y = centerInsideBorders[1] - infoHebSize[1] / 2
            screen.blit(pic_infoHeb, (popup_x, popup_y))
        if show_estimated_time:
            msgEstimatedTime(max(estimated_time - time.time() + last_send_time, 0))

        check_buttons(buttons)
        check_idle()
        check_dc_motor()

        pygame.display.update()
        # Flip screen
        pygame.display.flip()

        # check if sending to arduino
        if found_arduino:
            if send_to_arduino:
                if not check_arduino():
                    print("--- SOMETHING WENT WRONG WITH THE ARDUINO !!! ---")
                    logger.error("--- SOMETHING WENT WRONG WITH THE ARDUINO !!! ---")
                    send_to_arduino = False
                    show_estimated_time = False
                    if auto_run:
                        print("auto run stopped after: " + str(run_index) + " runs")
                        logger.info("auto run stopped after: " + str(run_index) + " runs")
                    auto_run = False
            else:
                try:
                    if arduino.in_waiting > 0:
                        received_data = arduino.readline().decode().rstrip()
                        print("Received from Arduino:", received_data)
                        if not sent_border:
                            take_control()
                            time.sleep(0.5)
                            sent_border = True
                            # send the cutting area size
                            print(send_one_number(centerInsideBorders[0] - cuttingAreaWidth / 2))
                            print(send_one_number(centerInsideBorders[1] - cuttingAreaHeight / 2))
                            print(send_one_number(centerInsideBorders[0] + cuttingAreaWidth / 2))
                            print(send_one_number(centerInsideBorders[1] + cuttingAreaHeight / 2))
                            print(send_one_number(LASER_POWER))
                            print(send_one_number(CONTOUR_POWER))
                            print(send_one_number(LASER_OFF_RATE))
                            print(send_one_number(LASER_ON_RATE))
                            print(send_one_number(CONTOUR_RATE))
                            print(send_one_number(MAX_DC_MOTOR_TIME * 1000))
                            logger.info("sent laser variables to arduino")
                            time.sleep(time_delay_arduino)

                    else:
                        pass
                finally:
                    pass
                if auto_run:
                    if run_index < MAX_RUNS:
                        time.sleep(MAX_DC_MOTOR_TIME + 2)
                        send_to_laser()
                        run_index += 1
                    else:
                        auto_run = False

        clock.tick(100)
        # print clock.get_fps()
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
