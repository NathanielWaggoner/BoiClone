import pygame as pg
import Enemy
## ROOMS ARE:::
##   always the same size
##   always big squares
##   can contain stuff in places
##   have enemies
## have some number of doors

class Wall(pg.sprite.Sprite):

    """A class representing solid obstacles."""

    def __init__(self, color, rect):
        """The color is an (r,g,b) tuple; rect is a rect-style argument."""
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.type = "normal"

    def draw(self,surface):
        surface.blit(self.image, self.rect)


class Door(Wall,pg.sprite.Sprite):
     def __init__(self, color, rect):
         Wall.__init__(self, color,rect)



class Room(pg.sprite.Sprite):
    def make_obstacles(self):

        walls = [Wall(pg.Color("chocolate"), (0,0,20,750)),
                 Wall(pg.Color("chocolate"), (980,0,20,750)),
                 Wall(pg.Color("chocolate"), (0,0,1000,20)),
                 Wall(pg.Color("chocolate"), (0,730,1000,20)),
                ]

        doors = [Door(pg.Color("red"),(0,310,25,50))]

        enemies = [Enemy.Enemy((75,75)),
                   Enemy.Enemy((450,475))
                   ]
        return pg.sprite.Group(walls, doors,enemies)

    def draw(self, surface):
        self.room_color = (50, 50, 50)
        surface.fill(self.room_color)
        self.obstacles.draw(surface)

    def __init__(self):
        self.obstacles = self.make_obstacles()