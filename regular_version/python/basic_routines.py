"""
Filename: basic_routines.py
Purpose: Basic routines for the program
Author: A.B.S
"""

import math

def distance(point1, point2):
    """
    Compute the distance between two points
    NOTE: This is not the regular distance formula, this calculation is more accurate for laser working estimation
    :param point1: first point
    :param point2: second point
    :return: distance between the two points
    """
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


def rotate_point(point, angle, center_p):
    """
    Rotate a point around a center point - this is used to tilt the square contour
    :param point: point to rotate
    :param angle: angle of rotation
    :param center_p: center point
    :return: rotated point
    """
    x, y = point
    cx, cy = center_p

    # Translate the point and center to the origin
    translated_x = x - cx
    translated_y = y - cy

    # Perform the rotation
    new_x = translated_x * math.cos(angle) - translated_y * math.sin(angle)
    new_y = translated_x * math.sin(angle) + translated_y * math.cos(angle)

    # Translate the point back to its original position
    rotated_x = new_x + cx
    rotated_y = new_y + cy

    return int(rotated_x), int(rotated_y)