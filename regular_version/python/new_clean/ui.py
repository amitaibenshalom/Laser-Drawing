"""
Filename:
Purpose:
"""

import pygame
from consts import *
from asset_loader import *
from button import Button
import math


class Ui:

    def __init__(self, screen, view_port):

        self.screen = screen        
        self.view_port = view_port
        
        self.border_line_left = convert_to_pixels("16%", self.view_port[0])
        self.border_line_right = convert_to_pixels("84%", self.view_port[0])
        self.border_line_top = convert_to_pixels("18.5%", self.view_port[1])
        self.border_line_bottom = convert_to_pixels("92%", self.view_port[1])

        # dict of picture names, their sizes and position to load on screen
        PICTURES_TO_LOAD = {
            "textAbove2.jpg": (("43%", "15%"), ("center", "2%")),
            "frame.jpg": (("7%", None), ("4%", "15%")),
        }

        BUTTONS_CONFIGURATION = {
            "draw": (("6%", None), ("89%", "22%"), ("pencil.png", "pencilPressed.png"), self.drawing_mode_on, True),
            "erase": (("6%", None), ("89%", "37%"), ("eraser.png", "eraserPressed.png"), self.erasing_mode_on, True),
            "clear": (("6%", None), ("89%", "52%"), ("garbage.png", "garbagePressed.png"), self.clear_all, False),
            "print": (("6%", None), ("89%", "77%"), ("printer.png", "printerPressed.png"), None, False),
            "heart": (("7%", None), ("4%", "30%"), ("heart.jpg", "heartPressed.jpg"), self.frame_heart, True),
            "drop": (("7%", None), ("4%", "50%"), ("drop.jpg", "dropPressed.jpg"), self.frame_drop, True),
            "square": (("7%", None), ("4%", "70%"), ("square.jpg", "squarePressed.jpg"), self.frame_square, True)
        }

        self.points = []
        self.mode = DRAWING_MODE
        self.frame = HEART_FRAME
        self.idle = False
        self.asset_loader = AssetLoader(ASSETS_DIR, PICTURES_TO_LOAD, self.view_port)
        self.buttons = self.init_buttons(BUTTONS_CONFIGURATION)

        
    def init_buttons(self, buttons_configuration):
        """
        For each button in the configuration, create a button object and add it to the buttons list
        :param buttons_configuration: dict of button names, their sizes and position to load on screen
        :return: list of button objects
        """
        buttons = {}
        for name, (size, pos, images, function, keep_pressed_image) in buttons_configuration.items():
            size = (convert_to_pixels(size[0], self.view_port[0]), convert_to_pixels(size[1], self.view_port[1]))
            pos = (convert_to_pixels(pos[0], self.view_port[0]), convert_to_pixels(pos[1], self.view_port[1]))
            button = Button(self.screen, pos, size, images, function, keep_pressed_image)
            buttons[name] = button
        return buttons

    
    def render_screen(self):

        # Draw everything
        self.screen.fill(BACKGROUND_COLOR)
        # draw the border rectangles
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER, (0, 0, self.border_line_left, self.view_port[1]))
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER, (self.border_line_right, 0, self.view_port[0] - self.border_line_right, self.view_port[1]))
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER, (0, 0, self.view_port[0], self.border_line_top))
        pygame.draw.rect(self.screen, COLOR_OUTSIDE_BORDER, (0, self.border_line_bottom, self.view_port[0], self.view_port[1] - self.border_line_bottom))

        self.asset_loader.render(self.screen)
        self.render_buttons()
        self.draw_lines()
        self.show_available_length()
        

    def render_buttons(self):
        for name, button in self.buttons.items():
            button.update()

        if self.mode == DRAWING_MODE:
            self.buttons["draw"].current_image = self.buttons["draw"].image_clicked
            self.buttons["erase"].current_image = self.buttons["erase"].image

        else:
            self.buttons["draw"].current_image = self.buttons["draw"].image
            self.buttons["erase"].current_image = self.buttons["erase"].image_clicked

        if self.frame == HEART_FRAME:
            self.buttons["heart"].current_image = self.buttons["heart"].image_clicked
            self.buttons["drop"].current_image = self.buttons["drop"].image
            self.buttons["square"].current_image = self.buttons["square"].image
        
        elif self.frame == DROP_FRAME:
            self.buttons["heart"].current_image = self.buttons["heart"].image
            self.buttons["drop"].current_image = self.buttons["drop"].image_clicked
            self.buttons["square"].current_image = self.buttons["square"].image

        else:
            self.buttons["heart"].current_image = self.buttons["heart"].image
            self.buttons["drop"].current_image = self.buttons["drop"].image
            self.buttons["square"].current_image = self.buttons["square"].image_clicked

        for name, button in self.buttons.items():
            button.render()

    def drawing_mode_on(self):
        self.mode = DRAWING_MODE

    def erasing_mode_on(self):
        self.mode = ERASING_MODE

    def delete_last_stroke(self):
        if not self.points:
            return
        
        idx = len(self.points) - 1
        while idx >= 0 and self.points[idx] is not None:
            idx -= 1

        self.points = self.points[:idx]  # Remove the last stroke

    def point_to_segment_distance(self, p, p1, p2):
        
        if p1 == p2:  # Handle the case where p1 == p2 (degenerate segment)
            return self.distance(p, p1)
    
        line_vec = (p2[0] - p1[0], p2[1] - p1[1])  # Vector from p1 to p2
        point_vec = (p[0] - p1[0], p[1] - p1[1])  # Vector from p1 to p

        line_len = self.distance(p1, p2)
        if line_len == 0:  # Prevent division by zero
            return self.distance(p, p1)

        projection = max(0, min(1, (point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]) / (line_len ** 2)))  # Project the point onto the line (scalar projection)
        closest_point = (p1[0] + projection * line_vec[0], p1[1] + projection * line_vec[1])  # Closest point on the line segment

        return self.distance(p, closest_point)

    def delete_closest_stroke(self, mouse_pos, threshold=MIN_DISTANCE_BETWEEN_POINTS):
        closest_stroke = None
        min_distance = float('inf')
        closest_stroke_start_idx = -1
        closest_stroke_end_idx = -1

        current_stroke = []
        for idx, point in enumerate(self.points):
            if point is None:
                if current_stroke:
                    for i in range(len(current_stroke) - 1):
                        p1 = current_stroke[i]
                        p2 = current_stroke[i + 1]
                        dist = self.point_to_segment_distance(mouse_pos, p1, p2)
                        if dist < min_distance:
                            min_distance = dist
                            closest_stroke = current_stroke
                            closest_stroke_start_idx = self.points.index(current_stroke[0])
                            closest_stroke_end_idx = self.points.index(current_stroke[-1]) + 1
                current_stroke = []
            else:
                current_stroke.append(point)

        if closest_stroke and min_distance <= threshold:
            del self.points[closest_stroke_start_idx:closest_stroke_end_idx]

    def clear_all(self):
        self.points.clear()

    def frame_heart(self):
        # TODO: frame
        self.frame = HEART_FRAME

    def frame_drop(self):
        self.frame = DROP_FRAME

    def frame_square(self):
        self.frame = SQUARE_FRAME

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    
    def in_border(self, pos):
        return self.border_line_left < pos[0] < self.border_line_right and self.border_line_top < pos[1] < self.border_line_bottom

    def add_point(self, pos):
        if (not self.points or self.points[-1] is None or self.distance(self.points[-1], pos) >= MIN_DISTANCE_BETWEEN_POINTS):
            if self.in_border(pos) and self.total_drawing_length() <  MAX_LENGTH:
                self.points.append(pos)
            
            elif self.points and self.points[-1] is not None:
                self.points.append(None)
    
    def end_stroke(self):
        if self.mode == DRAWING_MODE:
            self.points.append(None)

    def total_drawing_length(self):
        total_length = 0
        current_stroke = []

        for point in self.points:
            if point is None:
                if len(current_stroke) > 1:
                    for i in range(len(current_stroke) - 1):
                        total_length += self.distance(current_stroke[i], current_stroke[i + 1])
                current_stroke = []
            else:
                current_stroke.append(point)

        if len(current_stroke) > 1:
            for i in range(len(current_stroke) - 1):
                total_length += self.distance(current_stroke[i], current_stroke[i + 1])


        return total_length

    def handle_point(self, mouse_pos):
        if self.mode == DRAWING_MODE:
            self.add_point(mouse_pos)
        else:
            self.delete_closest_stroke(mouse_pos)

    def draw_lines(self):
        last_point = None
        for point in self.points:
            
            if point is None:
                last_point = None
                continue
            
            if last_point is not None:
                pygame.draw.line(self.screen, DRAWING_COLOR, last_point, point, DRAWING_WIDTH)
            
            last_point = point

    def show_available_length(self, width="15%", height="4%"):

        available_length_precentage = max(0, min(100, int((1 - (self.total_drawing_length() / MAX_LENGTH)) * 100)))

        width = convert_to_pixels(width, self.view_port[0])
        height = convert_to_pixels(height, self.view_port[1])
        font = pygame.font.SysFont(None, 50)
        text_color = BLACK
        rect_color = THE_RED_THAT_IS_ON_THE_BUTTONS
        bg_color = BLACK
        text = font.render(f"{available_length_precentage}%", True, text_color)
        self.screen.blit(text, (self.border_line_right - text.get_width() // 2, (self.border_line_top - text.get_height() - height) // 2))
        pygame.draw.rect(self.screen, bg_color, (self.border_line_right - width // 2, (self.border_line_top - height + text.get_height()) // 2, width, height))
        pygame.draw.rect(self.screen, rect_color, (self.border_line_right - width // 2, (self.border_line_top - height + text.get_height()) // 2, width * (available_length_precentage / 100), height))

        