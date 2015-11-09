import pygame as pg
import Enemy
import pickup
## ROOMS ARE:::
##   always the same size
##   always big squares
##   can contain stuff in places
##   have enemies
## have some number of doors

WALL_TYPE = "WALL"
class Wall(pg.sprite.Sprite):

    """A class representing solid obstacles."""

    def __init__(self, color, rect):
        """The color is an (r,g,b) tuple; rect is a rect-style argument."""
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.type = WALL_TYPE

    def draw(self,surface):
        surface.blit(self.image, self.rect)


class Door(Wall,pg.sprite.Sprite):
     def __init__(self, color, rect):
         Wall.__init__(self, color,rect)



class Room(pg.sprite.Sprite):
    def make_obstacles(self):
        # this room is 1000/750 with 2*20wide walls on each side, giving us a 960/710
        self.walls = [Wall(pg.Color("chocolate"), (0,0,20,750)),
                 Wall(pg.Color("chocolate"), (980,0,20,750)),
                 Wall(pg.Color("chocolate"), (0,0,1000,20)),
                 Wall(pg.Color("chocolate"), (0,730,1000,20)),
                 Wall(pg.Color("chocolate"), (240,177,480,20)),
                 Wall(pg.Color("chocolate"), (240,533,480,20)),
                 Wall(pg.Color("chocolate"), (240,177,20,250)),
                 Wall(pg.Color("chocolate"), (480,300,20,250)),
                 Wall(pg.Color("chocolate"), (710,177,20,250))


                ]

        self.doors = [Door(pg.Color("red"),(0,310,25,50))]

        self.enemies = [Enemy.Enemy((28,28)),
                   Enemy.Enemy((780,600)),
                   Enemy.Enemy((430,475))
                   ]

        self.pickups = [pickup.HealthPickup((400,400)),
                        pickup.FunkyPickup((375,375))]

        self.obstacles = pg.sprite.Group(self.walls, self.doors,self.enemies,self.pickups)
        self.enemy_concern = pg.sprite.Group(self.walls, self.doors)
        return self.obstacles

    def draw(self, surface):
        self.room_color = (50, 50, 50)
        surface.fill(self.room_color)
        self.obstacles.draw(surface)
        for enemy in self.enemies:
            for shot in enemy.shots.values():
                shot.draw(surface)

    def __init__(self):
        self.obstacles = self.make_obstacles()

    def update(self,player, now):
        self.enemy_concern = pg.sprite.Group(self.enemy_concern,player)
        toremove = []
        for enemy in self.enemies:
            enemy.update(self.enemy_concern,player,now)
            if enemy.health<=0:
                toremove.append(enemy)

        for dead in toremove:
            self.enemies.remove(dead)