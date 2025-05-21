"""
Filename: laser.py
Purpose: Handle all the laser functions
"""

import serial
import serial.tools.list_ports
from consts import BAUDRATE
import time


class Laser():

    def __init__(self, logger=None):
        self.logger = logger

        self.port = self.find_arduino_port()
        self.arduino = self.open_serial_connection()
        self.last_time_tried_to_connect = time.time()

        self.drawing = False
        self.sent_initial_params = False
        

    
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
                if self.logger:
                    self.logger.info(f"Found Arduino! port: {port.device}")

                if hasattr(self.find_arduino_port, "already_sent_error"):
                    self.find_arduino_port.already_sent_error = False

                return port.device
        
        if self.logger:
            # for not spamming the logs
            if not hasattr(self.find_arduino_port, "already_sent_error"):
                self.find_arduino_port.already_sent_error = False

            if not self.find_arduino_port.already_sent_error:
                self.logger.error("Error: Arduino not found")
                print("Arduino not found")
                self.find_arduino_port.already_sent_error = True

        return None  # continue without Arduino


    def open_serial_connection(self, timeout=1):
        """
        Open a serial connection to the specified port.
        """
        if not self.port:
            return None

        try:
            ser = serial.Serial(self.port, BAUDRATE, timeout=timeout)
            
            print(f"Connected to {self.port}")
            if self.logger:
                self.logger.info(f"Connected to {self.port}")

            return ser
        
        except serial.SerialException as e:
            print(f"Error: Could not open serial port {self.port} - {e}")
            if self.logger:
                self.logger.error(f"Error: Could not open serial port {self.port} - {e}")

            return None
