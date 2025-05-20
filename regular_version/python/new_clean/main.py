"""
Filename: main.py
Purpose: Main file for the exhibit
"""

import pygame
from pygame.locals import *
from consts import *
from asset_loader import *
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
    
    # asset_loader = AssetLoader(ASSETS_DIR, PICTURES_TO_LOAD, view_port)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
    
        screen.fill(BLACK)
        # asset_loader.render(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()