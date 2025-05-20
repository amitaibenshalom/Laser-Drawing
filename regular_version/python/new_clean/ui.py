"""
Filename:
Purpose:
"""

import pygame
from consts import *
from asset_loader import *


class Ui:

    def __init__(self, screen, view_port):

        self.screen = screen        
        self.view_port = view_port
        
        border_line_left = convert_to_pixels("9.5%", self.view_port[0])
        border_line_right = convert_to_pixels("72%", self.view_port[0])
        border_line_top = convert_to_pixels("18.5%", self.view_port[1])
        border_line_bottom = convert_to_pixels("92%", self.view_port[1])
        center = (convert_to_pixels("center", self.view_port[0]), convert_to_pixels("center", self.view_port[1]))
        center_inside_borders = ((border_line_left + border_line_right) // 2, (border_line_top + border_line_bottom) // 2)

        # dict of picture names, their sizes and position to load on screen
        PICTURES_TO_LOAD = {
            "background.png": (("full", "full"), (0, 0)),
            "grid.png": (("70%", "70%"),("25%", "25%")),
        }

        BUTTONS_CONFIGURATION = {
            "draw"
        }

        self.points = []
        self.max_length = MAX_LENGTH
        self.frame = "heart"
        self.idle = False
        self.asset_loader = AssetLoader(ASSETS_DIR, PICTURES_TO_LOAD, self.view_port)
        self.buttons = self.init_buttons()

        
    def init_buttons(self):
        return []
    
    def render_screen(self):

        # Draw everything
        self.screen.fill(BACKGROUND_COLOR)
        # draw the border rectangles
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER, (0, 0, borderLineX, screen_height))
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER, (borderLine2X, 0, screen_width - borderLine2X, screen_height))
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER, (0, 0, screen_width, borderLineHeight))
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER,
                         (0, borderLine2Height, screen_width, screen_height - borderLine2Height))


    def delete_last_stroke(self):

        if not self.points:
            return
        
        idx = len(self.points) - 1
        while idx >= 0 and self.points[idx] is not None:
            idx -= 1
        self.points = self.points[:idx]  # Remove the last stroke

    def clear_all(self):
        self.points.clear()

    def frame_heart(self):
        # TODO: frame
        pass

    # def add_point(self):


    