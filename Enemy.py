import pygame as pg
import random as rand
import time
import shot

ENEMY_TYPE = 'ENEMY'

class Enemy(pg.sprite.Sprite):
    """Class representing our player."""
    def __init__(self,location):
        pg.sprite.Sprite.__init__(self)
        self.health = 10
        self.speed = 3
        self.damage = 5
        self.shots = False
        self.image = pg.image.load("base_face.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=location)
        self.last_moved = 0.0
        self.move_change_rate = 1
        self.force_new_move = False
        self.movement = (0,0)
        self.type = ENEMY_TYPE
        self.last_fire = 0
        self.shot_frequency = 1.5
        self.shot_speed = 6
        self.shots = dict()

    def draw(self,surface):
        """Blit the player to the target surface."""
        surface.blit(self.image, self.rect)
        for moving in self.shots.values():
            moving.draw()

    def update(self,obstacles,player,now):
        self.movement = self.get_move_direction(now)
        can_move = self.check_collisions(self.movement, 1, obstacles)
        if can_move:
            self.rect.move_ip(self.movement[0],self.movement[1])

        if self.should_shoot(now):
            self.last_fire = now
            self.shoot(player,now)

        to_remove = []

        for shooting in self.shots.values():
            shooting.update(to_remove,obstacles,now)

        for dead in to_remove:
            self.shots.pop(dead)

    def should_shoot(self,now):
        return now-self.last_fire>self.shot_frequency

    def shoot(self,player,now):
        prect = player.rect
        x_dir = (1 if prect.left > self.rect.left else -1 if prect.left < self.rect.left else 0)
        y_dir = (1 if prect.top > self.rect.top else -1 if prect.top < self.rect.top else 0)
        shooting = shot.Shot(self.rect.topleft,x_dir,y_dir,self.shot_speed,self.damage,ENEMY_TYPE,now)
        self.shots[shooting.key] = shooting

    # return a tuple where x/y are the randomly assigned values of up/down/l/r times speed
    def get_move_direction(self, now):
        move_time = time.time()
        if self.force_new_move or now-self.last_moved>self.move_change_rate:
            self.last_moved =move_time
            self.force_new_move = False
            return (rand.randint(-1,1)*self.speed,rand.randint(-1,1)*self.speed)
        return self.movement

    def check_collisions(self,dir,index,obstacles):
        unaltered = True
        self.rect.move_ip(dir[0],dir[1])
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        collidable = pg.sprite.collide_mask
        delta_x = 0
        delta_y = 0
        if(len(collisions)>0):
            unaltered = False
            self.force_new_move = True
            count = 0
            while count < self.speed and pg.sprite.spritecollideany(self, collisions, collidable):
                delta_x = (1 if dir[0] < 0 else -1 if dir[0] > 0 else 0)
                delta_y += (1 if dir[1] < 0 else -1 if dir[1] > 0 else 0)
                self.rect[0] += delta_x
                self.rect[1] += delta_y
                count += 1
            self.movement = (delta_x,delta_y)

        self.rect.move_ip(-dir[0],-dir[1])
        return unaltered

    def take_damage(self,projectile):
        self.health -= projectile.damage
        if self.health <=0:
            self.kill()