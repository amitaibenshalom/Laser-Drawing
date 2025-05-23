"""
Filename: laser.py
Purpose: Handle all the laser functions
"""

import serial
import serial.tools.list_ports
from consts import *
import time


class Laser():

    def __init__(self, laser_cutting_pos, laser_cutting_size, logger):
        self.laser_cutting_pos = laser_cutting_pos
        self.laser_cutting_size = laser_cutting_size
        self.logger = logger

        self.drawing = False
        self.sent_init_params = False
        self.points = []
        self.frame_points = []
        self.index = 0
        self.mode = "drawing_points"  # drawing_points OR frame_points - which to send right now
        self.batch_size = POINTS_BATCH_SIZE
        # self.screen_scale = (LASER_BOARD_SIZE[0] / laser_cutting_area[2], LASER_BOARD_SIZE[1] / laser_cutting_area[3])

        self.last_time_sent_data = time.time()
        self.waiting_for_ack = False
        self.drawing_start_time = time.time()

        self.arduino = self.open_serial_connection()
        self.last_time_tried_to_connect = time.time()

    
    def find_arduino_port(self):
        """
        Locate the Arduino's serial port (e.g., ttyUSB0 or ttyACM0 on Linux).
        """
        ports = serial.tools.list_ports.comports()

        for port in ports:
            # Check if the device description matches an Arduino
            # print(f"port: {port}")
            if "Arduino" in port.description or "ttyUSB" in port.device or "ttyACM" in port.device:
                print(f"Found Arduino on port {port.device}")
                self.logger.info(f"Found Arduino on port: {port.device}")

                # if hasattr(self.find_arduino_port, "already_sent_error"):
                #     self.find_arduino_port.already_sent_error = False

                return port.device
        
        # for not spamming the logs
        # if not hasattr(self.find_arduino_port, "already_sent_error"):
        #     self.find_arduino_port.already_sent_error = False

        # if not self.find_arduino_port.already_sent_error:
        #     self.logger.error("Error: Arduino not found")
        #     print("Arduino not found")
        #     self.find_arduino_port.already_sent_error = True

        return None  # continue without Arduino


    def open_serial_connection(self, timeout=1):
        """
        Open a serial connection to the specified port.
        """
        port = self.find_arduino_port()

        if not port:
            print(f"Error: Arduino not found")
            self.logger.error(f"Error: Arduino not found")
            return None

        try:
            ser = serial.Serial(port, BAUDRATE, timeout=timeout)
            
            print(f"Connected to {port}")
            self.logger.info(f"Connected to {port}")
            time.sleep(0.01)
            return ser
        
        except serial.SerialException as e:
            print(f"Error: Could not open serial port {port} - {e}")
            self.logger.error(f"Error: Could not open serial port {port} - {e}")
            return None
        
    def exist(self):
        return self.arduino != None
    
    def is_drawing(self):
        return self.drawing
    
    def send_values(self, *values, delay=False, delay_time=0.01):
        for value in values:
            encoded_value = f"{value}\n".encode()
            self.arduino.write(encoded_value)

        if delay:
            time.sleep(delay_time) # small delay

    def send_initial_parameters(self):
        if not self.arduino:
            return
        
        self.logger.info("Sending initial parameters for Arduino")

        try:
            self.send_values("PARAMS")
            self.send_values(*self.laser_cutting_pos,
                             self.laser_cutting_pos[0] + self.laser_cutting_size[0], 
                             self.laser_cutting_pos[1] + self.laser_cutting_size[1],
                             delay=True)
            self.send_values(LASER_POWER, LASER_POWER, LASER_OFF_RATE, LASER_ON_RATE, FRAME_RATE, MAX_DC_MOTOR_TIME * 1000, delay=True)
            self.logger.info("Waiting for 'OK'...")

            start = time.time()
            while time.time() - start < INIT_PARAMS_TIMEOUT:
                if self.arduino.in_waiting:
                    response = self.arduino.readline().strip()

                    if response == b"OK":
                        self.logger.info("Got OK - Arduino acknowledged parameters")
                        self.send_initial_parameters = True
                        return True
                    
                    else:
                        self.logger.info(f"Unexpected response: {response}")
                        self.arduino = None
                        return False
                    
            print("Error: No 'OK' from Arduino")
            self.logger.error("Error: No 'OK' from Arduino")
            self.arduino = None
            return False

        except serial.SerialException as e:
            print(f"[ERROR] Failed during transmission: {e}")
            self.logger.error(f"ERROR: Failed during transmission: {e}")
            self.arduino = None
            return False

    def init_drawing(self, points, frame_points):
        self.points = points
        self.frame_points = frame_points
        self.drawing = True
        self.drawing_start_time = time.time()
        self.waiting_for_ack = False
        self.mode = "drawing_points"
        self.logger.info("Started drawing...")

        try:
            self.send_values("START")
            return True
        
        except:
            print(f"[ERROR] Failed during transmission")
            self.logger.error(f"Error: Failed during transmission")
            return False

    def send_batch_points(self):        
        # Waiting for Arduino ACK (ack of finishing drawing the batch)
        if self.waiting_for_ack:
            if self.arduino.in_waiting:
                line = self.arduino.readline().decode().strip()
                if line == "OK":
                    self.waiting_for_ack = False
                    self.last_time_sent_data = None
                else:
                    return "ACK"

            elif time.time() - self.last_time_sent_data > ARDUINO_DRAWING_BATCH_TIMEOUT:
                self.send_values("RESET")
                return "RESET" 
            
            else:
                return "ACK"

        # Not waiting: send the next batch
        points = self.points if self.mode == "drawing_points" else self.frame_points
        if self.index >= len(points):
            self.send_values("D_DONE" if self.mode == "drawing_points" else "F_DONE")  # drawing done or frame done
            self.waiting_for_ack = False
            return "DONE"

        batch = points[self.index:self.index + self.batch_size]
        for point in batch:
            if point is None:
                self.send_values("None")
            else:
                x, y = point
                # laser_x, laser_y = (x - self.laser_cutting_area[0])* self.screen_scale[0], (y - self.laser_cutting_area[1])* self.screen_scale[1]
                self.send_values(f"{x},{y}")

        self.send_values("B_DONE")  # batch done
        self.index += self.batch_size
        self.waiting_for_ack = True
        self.last_time_sent_data = time.time()
        return "ACK"


    def end_drawing(self):
        self.drawing = False
        self.points.clear()
        self.frame_points.clear()
        self.index = 0
        self.mode = "drawing_points"
        self.last_time_sent_data = time.time()
        self.waiting_for_ack = False

    def check_on_laser(self):
        if not self.drawing:
            return "NOT DRAWING"
        
        try:
            status = self.send_batch_points()

            if status == "RESET":
                print("Timeout waiting for Arduino. Stopping transmission.")
                self.logger.error("Error: Timeout waiting for Arduino. Stopping transmission.")
                self.end_drawing()
                return "DONE"
            
            if status == "DONE":
                if self.mode == "drawing_points":
                    # done only user points, now send frame points
                    self.mode = "frame_points"
                    self.index = 0
                    return "DRAWING"
                
                # if got to here, than finished drawing the frame points - fully done!
                total_time = f"{(time.time() - self.drawing_start_time):.1f}"
                print(f"Finished drawing in {total_time} seconds")
                self.logger.error(f"Finished drawing in {total_time} seconds")
                self.end_drawing()
                return "DONE"
            
            return "DRAWING"
        
        except:
            return "ERROR"
        

            
        


        
            


                
