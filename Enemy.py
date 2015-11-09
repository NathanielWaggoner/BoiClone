import pygame as pg
import random as rand
import time
class Enemy(pg.sprite.Sprite):

    """Class representing our player."""
    def __init__(self,location):
        pg.sprite.Sprite.__init__(self)
        self.health = 10
        self.speed = 10
        self.damage = 5
        self.shots = False
        self.image = pg.image.load("base_face.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=location)
        self.last_moved = 0.0
        self.move_change_rate = 1
        self.force_new_move = False
        self.movement = (0,0)

    def draw(self,surface):
        """Blit the player to the target surface."""
        surface.blit(self.image, self.rect)

    def update(self,obstacles,player):
        self.movement = self.get_move_direction()
        can_move = self.check_collisions(self.movement, 1, obstacles)
        if can_move:
            self.rect.move_ip(self.movement[0],self.movement[1])
    # return a tuple where x/y are the randomly assigned values of up/down/l/r times speed
    def get_move_direction(self):
        move_time = time.time()
        if self.force_new_move or move_time- self.last_moved>self.move_change_rate:
            self.last_moved =move_time
            self.force_new_move = False
            return (rand.randint(-1,1)*self.speed,rand.randint(-1,1)*self.speed)
        return self.movement

    def check_collisions(self,dir,index,obstacles):
        unaltered = True
        old_loc = self.rect
        self.rect.move_ip(dir[0],dir[1])
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        collidable = pg.sprite.collide_mask
        delta_x = 0
        delta_y = 0
        if(len(collisions)>0):
            unaltered = False
            self.force_new_move = True

            while pg.sprite.spritecollideany(self, collisions, collidable):
                delta_x = (1 if dir[0] < 0 else -1 if dir[0] > 0 else 0)
                delta_y += (1 if dir[1] < 0 else -1 if dir[1] > 0 else 0)
                self.rect[0] += delta_x
                self.rect[1] += delta_y
            self.movement = (delta_x,delta_y)

        self.rect.move_ip(-dir[0],-dir[1])
        return unaltered