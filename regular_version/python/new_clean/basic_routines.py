"""
Filename: basic_routines.py
Purpose: Basic routines for the program
"""

def distance(point1, point2):
    """
    Compute the distance between two points
    NOTE: This is not the regular distance formula, this calculation is more accurate for laser working estimation
    :param point1: first point
    :param point2: second point
    :return: distance between the two points
    """
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))