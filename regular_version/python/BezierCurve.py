"""
Filename: BezierCurve.py
Purpose: Object of a curve, defined by 4 points (Bezier curve)
Author: A.B.S
"""

import pygame
import math
from basic_routines import distance

class BezierCurve(object):
    """
    Object of a curve, defined by 4 points (Bezier curve)
    """
    def __init__(self, p0, p1, p2, p3, moveable, color, width):
        """
        Constructor for the BezierCurve class
        :param p0: first point of the curve
        :param p1: second point of the curve
        :param p2: third point of the curve
        :param p3: fourth point of the curve
        :param moveable: boolean to check if the curve is moveable
        :param color: color of the curve
        :param width: width of the curve
        """
        self.vertices = [p0, p1, p2, p3]
        self.moveable = moveable
        self.color = color
        self.width = width

    def compute_bezier_points(self, numPoints=None):
        """
        Compute the points of the Bezier curve
        :param numPoints: number of points to compute
        :return: list of points of the Bezier curve
        """

        if numPoints is None:
            numPoints = 30  # arbitrary choice

        if numPoints < 2 or len(self.vertices) != 4:
            return None  # invalid inputs

        result = []

        b0x = self.vertices[0][0]
        b0y = self.vertices[0][1]
        b1x = self.vertices[1][0]
        b1y = self.vertices[1][1]
        b2x = self.vertices[2][0]
        b2y = self.vertices[2][1]
        b3x = self.vertices[3][0]
        b3y = self.vertices[3][1]

        # Compute polynomial coefficients from Bezier points
        ax = (-b0x + 3 * b1x + -3 * b2x + b3x)
        ay = (-b0y + 3 * b1y + -3 * b2y + b3y)

        bx = (3 * b0x + -6 * b1x + 3 * b2x)
        by = (3 * b0y + -6 * b1y + 3 * b2y)

        cx = (-3 * b0x + 3 * b1x)
        cy = (-3 * b0y + 3 * b1y)

        dx = (b0x)
        dy = (b0y)

        # Set up the number of steps and step size
        numSteps = numPoints - 1  # arbitrary choice
        h = 1.0 / numSteps  # compute our step size

        # Compute forward differences from Bezier points and "h"
        pointX = dx
        pointY = dy

        firstFDX = (ax * (h * h * h) + bx * (h * h) + cx * h)
        firstFDY = (ay * (h * h * h) + by * (h * h) + cy * h)

        secondFDX = (6 * ax * (h * h * h) + 2 * bx * (h * h))
        secondFDY = (6 * ay * (h * h * h) + 2 * by * (h * h))

        thirdFDX = (6 * ax * (h * h * h))
        thirdFDY = (6 * ay * (h * h * h))

        # Compute points at each step
        result.append((int(pointX), int(pointY)))

        for i in range(numSteps):
            pointX += firstFDX
            pointY += firstFDY

            firstFDX += secondFDX
            firstFDY += secondFDY

            secondFDX += thirdFDX
            secondFDY += thirdFDY

            result.append((int(pointX), int(pointY)))

        return result

    def draw(self, surface):
        """
        Draw the curve on the screen
        :param surface: surface to draw the curve on
        """

        b_points = self.compute_bezier_points()
        pygame.draw.lines(surface, self.color, False, b_points, self.width)

    def get_length(self):
        """
        Compute the length of the curve
        :return: length of the curve
        """
        b_points = self.compute_bezier_points()
        length = 0
        for i in range(len(b_points) - 1):
            length += distance(b_points[i], b_points[i + 1])
        return length


def length_of_curve(curve):
    """
    Compute the true length of a curve
    :param curve: curve to compute the length of
    :return: length of the curve
    """
    length = 0
    for i in range(len(curve) - 1):
        length += math.dist(curve[i], curve[i + 1])
    return length


def length_of_curve_zigzag(curve):
    """
    Compute the length of a curve (zigzag)
    the zigzag is not a straight line, so the distance is NOT the sqrt of the sum of squares
    :param curve: curve to compute the length of
    :return: length of the curve (in zigzag)
    """
    length = 0

    for i in range(len(curve) - 1):
        length += distance(curve[i], curve[i + 1])
        
    return length