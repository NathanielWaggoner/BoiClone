import os
import sys
import random
import Player
import pygame as pg
import Room

CAPTION = "Basic Platforming: Pixel Perfect Collision"
SCREEN_SIZE = (1000, 750)



class Control(object):
    """Class for managing event loop and game states."""
    def __init__(self):
        """Nothing to see here folks. Move along."""
        self.screen = pg.display.get_surface()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.player = Player.Player((350,250))
        self.room = Room.Room()
        self.obstacles = self.room.make_obstacles()



    def event_loop(self):
        """We can always quit, and the player can sometimes jump."""
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True


    def update(self):
        """Update held keys and the player."""
        self.keys = pg.key.get_pressed()
        self.player.update(self.obstacles, self.keys)

    def draw(self):
        """Draw all necessary objects to the display surface."""
        self.room.draw(self.screen)
        self.player.draw(self.screen)

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        """As simple as it gets."""
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)
            self.display_fps()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()
