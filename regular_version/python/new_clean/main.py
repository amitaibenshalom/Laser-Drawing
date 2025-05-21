"""
Filename: main.py
Purpose: Main file for the exhibit - run me
"""

import pygame
from pygame.locals import *
from consts import *
from asset_loader import *
from ui import Ui
from logs import *


def main():

    logger = get_logger()
    logger.info("Starting Laser Drawing Exhibit")
    
    pygame.init()
    pygame.display.set_caption("Laser Drawing")
    clock = pygame.time.Clock()
    
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        view_port = (screen_width, screen_height)

    else:
        screen = pygame.display.set_mode(VIEWPORT)
        view_port = VIEWPORT
    
    ui = Ui(screen, view_port, logger)

    mouse_down = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

            if event.type == KEYDOWN:
                if event.key == K_e:
                    ui.show_estimated_time = not ui.show_estimated_time

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True      
                    ui.handle_point(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click released
                    mouse_down = False
                    ui.end_stroke()
    
        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            ui.handle_point(mouse_pos)

        ui.render_screen()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()