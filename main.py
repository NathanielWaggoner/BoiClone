import os
import sys
import random
import Player
import pygame as pg

CAPTION = "Basic Platforming: Pixel Perfect Collision"
SCREEN_SIZE = (700, 500)
BACKGROUND_COLOR = (50, 50, 50)



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
        self.obstacles = self.make_obstacles()

    def make_obstacles(self):
        """Adds some arbitrarily placed obstacles to a sprite.Group."""
        # obstacles = [Block((400,400)), Block((300,270)), Block((150,170))]
        # obstacles += [Block((500+50*i,220)) for i in range(3)]
        # for i in range(12):
        #     obstacles.append(Block((50+i*50,450)))
        #     obstacles.append(Block((100+i*50,0)))
        #     obstacles.append(Block((0,50*i)))
        #     obstacles.append(Block((650,50*i)))
        # return pg.sprite.Group(obstacles)

    def event_loop(self):
        """We can always quit, and the player can sometimes jump."""
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update(self):
        """Update held keys and the player."""
        self.keys = pg.key.get_pressed()
        self.player.update(self.obstacles, self.keys)

    def draw(self):
        """Draw all necessary objects to the display surface."""
        self.screen.fill(BACKGROUND_COLOR)
        # self.obstacles.draw(self.screen)
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
