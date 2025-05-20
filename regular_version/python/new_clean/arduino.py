"""
Filename: arduino.py
Purpose: Arduino functions for the Jumping Ring UI
"""

import serial
import serial.tools.list_ports
from consts import BAUDRATE


def find_arduino_port(logger=None):
    """
    Locate the Arduino's serial port (e.g., ttyUSB0 or ttyACM0 on Linux).
    """
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Check if the device description matches an Arduino
        # print(f"port: {port}")
        if "Arduino" in port.description or "ttyUSB" in port.device or "ttyACM" in port.device:
            print(f"Found Arduino on port {port.device}")
            if logger:
                logger.info(f"Found Arduino! port: {port.device}")

            if hasattr(find_arduino_port, "already_sent_error"):
                find_arduino_port.already_sent_error = False

            return port.device
    
    if logger:
        # for not spamming the logs
        if not hasattr(find_arduino_port, "already_sent_error"):
            find_arduino_port.already_sent_error = False

        if not find_arduino_port.already_sent_error:
            logger.error("Error: Arduino not found")
            print("Arduino not found")
            find_arduino_port.already_sent_error = True

    return None  # continue without Arduino


def open_serial_connection(port=None, baud_rate=BAUDRATE, timeout=1, logger=None):
    """
    Open a serial connection to the specified port.
    """
    if not port:
        return None

    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        
        print(f"Connected to {port}")
        if logger:
            logger.info(f"Connected to {port}")

        return ser
    
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port} - {e}")
        if logger:
            logger.error(f"Error: Could not open serial port {port} - {e}")

        return None




