import time
import random as rand
import pygame as pg
import Enemy
import player
import room

class Shot(object):
    def __init__(self,location, x_vel, y_vel, shot_speed, damage, parent,now):
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.speed = shot_speed
        self.damage = damage
        self.image = pg.image.load("projectile.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=location)
        self.key = time.time()
        self.birth = now
        self.age = 2
        self.parent = parent

    def update(self,to_remove,obstacles, now):
        self.rect.move_ip(self.x_vel*self.speed,self.y_vel*self.speed)
        # check if this projectile has gone stale
        diff = now-self.birth
        shouldRemove = False
        if diff>self.age:
           shouldRemove = True

        if not shouldRemove:
            shouldRemove = self.handle_collisions(to_remove,obstacles,now)

        if shouldRemove:
            to_remove.append(self.key)

    def handle_collisions(self, to_remove, obstacles,now):
        if not self.check_collisions(self.y_vel,self.x_vel,1,obstacles,now):
            to_remove.append(self.key)

    def check_collisions(self, offset_y,offset_x, index, obstacles,now):
        unaltered = True
        self.rect.move_ip(offset_x,offset_y)
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        collidable = pg.sprite.collide_mask
        if not pg.sprite.spritecollideany(self, collisions, collidable):
            for coll in collisions:
                if coll.type == self.parent:
                    return unaltered
                elif coll.type == Enemy.ENEMY_TYPE or coll.type == player.PLAYER_TYPE:
                    coll.take_damage(self)
                    unaltered = False
                if coll.type == room.WALL_TYPE:
                    unaltered = self.handle_wall_collision(coll,now)

        return unaltered

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def handle_wall_collision(self, collision,now):
        return False



class BouncyShot(Shot):

    def __init__(self,location, x_vel, y_vel, shot_speed, damage, parent,now):
        Shot.__init__(self,location,x_vel,y_vel,shot_speed,damage,parent,now)

    def handle_wall_collision(self, collision,now):
        ## are we coming from left/right/above or below?
        ## handle each case correctly
        # coming from left:
        if self.x_vel > 0:
            if self.rect.x < collision.rect.x+collision.rect.width:
                self.x_vel = -self.x_vel
        # coming from right
        elif self.x_vel < 0:
             if self.rect.x > collision.rect.x:
                  self.x_vel = -self.x_vel

        if self.y_vel > 0:
            if self.rect.y < collision.rect.y+collision.rect.height:
                self.y_vel = -self.y_vel

        elif self.y_vel < 0:
            if self.rect.y < collision.rect.y:
                self.y_vel = -self.y_vel

        return True

class ExplodingShot(BouncyShot):
    def __init__(self,location, x_vel, y_vel, shot_speed, damage, parent,now):
        BouncyShot.__init__(self,location,x_vel,y_vel,shot_speed,damage,parent,now)

    def handle_wall_collision(self, collision,now):
        BouncyShot.handle_wall_collision(self,collision,now)
        # one = =Shot(self.rect.topleft, 0, self.y_vel, self.speed, self.damage/2, self.parent,now)
        # two = Shot(self.rect.topleft, self.x_vel, 0, self.speed, self.damage/2, self.parent,now)
