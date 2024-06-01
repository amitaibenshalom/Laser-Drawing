"""
Filename: Button.py
Purpose: Button class for creating buttons on the screen
Author: A.B.S
"""

import pygame

class Button(object):
    """
    Button class for creating buttons on the screen
    """
    def __init__(self, pos, size, color, coloron, img, imgon, function):
        """
        Constructor for the Button class
        :param pos: position of the button
        :param size: size of the button
        :param color: color of the button (relevant if img is None)
        :param coloron: color of the button when clicked (relevant if imgon is None)
        :param img: image of the button
        :param imgon: image of the button when clicked
        :param function: function to be called when the button is clicked
        """
        self.pos = pos
        self.size = size
        self.color = color
        self.coloron = coloron
        self.img = img  # image when not clicking
        self.imgon = imgon  # image when clicking
        self.tempimg = img  # also saves img but not changing (tempimg = temporary image)
        self.function = function
        self.done = True

    def check(self):
        """
        Check if the button is clicked, and call the function if it is)
        """
        global buttons_enabled, screen

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        on_button = rect.collidepoint(mouse)
        
        if click[0] == 0:
            self.img = self.tempimg

            if self.img is not None:
                screen.blit(self.img, self.img.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, self.color, rect)
            self.done = True
        
        elif on_button and self.done:

            if self.imgon is not None:
                screen.blit(self.imgon, self.imgon.get_rect(center=rect.center))
            
            else:
                pygame.draw.rect(screen, self.coloron, rect)
            
            self.done = False
            self.img = self.imgon
            
            if self.function is not None:
                self.function()
            
            buttons_enabled = False

        else:

            if self.img is not None:
                screen.blit(self.img, self.img.get_rect(center=rect.center))

            else:
                pygame.draw.rect(screen, self.color, rect)

    def draw_static(self):
        """
        Draw the button (with the default image) on the screen (used when buttons are locked)
        """
        global screen

        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        if self.img is not None:
            screen.blit(self.img, self.img.get_rect(center=rect.center))

        else:
            pygame.draw.rect(screen, self.color, rect)


def check_buttons(buttons):
    """
    Check all the buttons on the screen (if they are clicked)
    if buttons are not enabled, draw the buttons statically (without changing the image on touch)
    :param buttons: list of buttons to check
    """
    global buttons_enabled

    if buttons_enabled:
        for button in buttons:
            button.check()

    else:
        for button in buttons:
            button.draw_static()