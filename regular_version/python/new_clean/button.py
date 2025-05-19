"""
Filename: Button.py
Purpose: Button class for creating buttons on the screen
"""

import pygame

class Button(object):
    """
    Button class for creating buttons on the screen
    """
    def __init__(self, screen, pos, size, image, image_clicked, function, execute_on_release=True):
        """
        Constructor for the Button class
        :param screen: screen to draw the button on
        :param pos: position of the button (x, y)
        :param size: size of the button (width, height)
        :param image: image of the button (when not clicked)
        :param image_clicked: image of the button (when clicked)
        :param function: function to call when the button is clicked
        """
        self.screen = screen
        self.pos = pos
        self.size = size
        self.image = image
        self.image_clicked = image_clicked
        self.function = function
        self.execute_on_release = execute_on_release  # if the function should be executed on release

        self.enabled = True  # if the button is enabled
        self.clicked = False  # if the button is clicked
        self.current_image = image  # the image to draw on the button (this will be changed when the button is clicked)

    def update(self):
        """
        Update the button state, draw the button on the screen and call the function if clicked
        """

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        on_button = rect.collidepoint(mouse)
        
        if self.enabled and on_button and click[0] == 1 and not self.clicked:
            self.clicked = True
            self.current_image = self.image_clicked
            
            if not self.execute_on_release:
                self.function()

        elif on_button and click[0] == 0 and self.clicked:
            self.clicked = False
            self.current_image = self.image
            
            if self.execute_on_release:
                self.function()

        elif not on_button and click[0] == 0 and self.clicked:
            self.clicked = False
            self.current_image = self.image

        elif not on_button and click[0] == 1:
            self.enabled = False

        elif click[0] == 0:
            self.clicked = False
            self.current_image = self.image
            self.enabled = True

        self.screen.blit(self.current_image, (self.pos[0], self.pos[1]))
