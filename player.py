import pygame as pg
import time
import random as r

class _Physics(object):
    """
    A simplified physics class. Using a 'real' gravity function here, though
    it is questionable whether or not it is worth the effort. Compare to the
    effect of gravity in fall_rect and decide for yourself.
    """
    def __init__(self):
        """You can experiment with different gravity here."""
        self.x_vel = self.y_vel = self.y_vel_i = 0
        self.grav = 20
        self.time = None

    def physics_update(self):
        """If the player is falling, calculate current y velocity."""
        # if self.canMove:
        #     time_now = pg.time.get_ticks()
        #     if not self.time:
        #         self.time = time_now
        #     self.y_vel = self.grav*((time_now-self.time)/1000.0)+self.y_vel_i
        # else:
        #     self.time = None
        #     self.y_vel = self.y_vel_i = 0
        self.y_vel

class PlayerShot(object):
    def __init__(self,location, x_vel, y_vel, shot_speed, damage):
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.speed = shot_speed
        self.damage = damage
        self.image = pg.image.load("projectile.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=location)
        self.key = time.time()
        self.age = .5

    def update(self,to_remove,objstacles):
        self.rect.move_ip(self.x_vel*self.speed,self.y_vel*self.speed)

        update = time.time();

        # check if this projectile has gone stale
        if update-self.key>self.age:
            to_remove.append(self.key)

        if self.check_collisions(self.y_vel,self.x_vel,1,objstacles):
            to_remove.append(self.key)

    def check_collisions(self, offset_y,offset_x, index, obstacles):
        unaltered = True
        self.rect.move_ip(offset_x,offset_y)
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        collidable = pg.sprite.collide_mask
        if not pg.sprite.spritecollideany(self, collisions, collidable):
            return False
        return True




class Player(_Physics, pg.sprite.Sprite):


    """Class representing our player."""
    def __init__(self,location):
        """
        The location is an (x,y) coordinate pair, and speed is the player's
        speed in pixels per frame. Speed should be an integer.
        """
        _Physics.__init__(self)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("base_face.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.canMove = False
        self.jump_power = 10
        self.moving_y = False
        self.moving_x = False
        self.firing_x = 0
        self.firing_y = 0
        self.projectiles = dict()
        self.last_fire = time.time()

        self.trinkets = []
        self.items = []
        self.consumables = []

        self.health = 3
        self.fire_rate = .5
        self.shot_speed = 20;
        self.damage = 5
        self.speed = 10


        self.rect = self.image.get_rect(topleft=location)

    def get_position(self, obstacles):
        """Calculate the player's position this frame, including collisions."""
        self.canMove = self.check_collisions((0,self.y_vel), 1, obstacles)
        if self.x_vel:
            self.move_x()
        if self.y_vel:
            self.move_y()

    def move_x(self):
        self.rect.move_ip(self.x_vel,0)

    def move_y(self):
        self.rect.move_ip(0,self.y_vel)

    def check_falling(self, obstacles):
        """If player is not contacting the ground, enter fall state."""
        # self.rect.move_ip((0,1))
        # collisions = pg.sprite.spritecollide(self, obstacles, False)
        # collidable = pg.sprite.collide_mask
        # if not pg.sprite.spritecollideany(self, collisions, collidable):
        #     self.fall = True
        # self.rect.move_ip((0,-1))

    def check_collisions(self, offset, index, obstacles):
        """
        This function checks if a collision would occur after moving offset
        pixels.  If a collision is detected position is decremented by one
        pixel and retested. This continues until we find exactly how far we can
        safely move, or we decide we can't move.
        """
        # unaltered = True
        # self.rect.move_ip(offset)
        # collisions = pg.sprite.spritecollide(self, obstacles, False)
        # collidable = pg.sprite.collide_mask
        # while pg.sprite.spritecollideany(self, collisions, collidable):
        #     self.rect[index] += (1 if offset[index]<0 else -1)
        #     unaltered = False
        # return unaltered

    def check_keys(self, keys):
        """Find the player's self.x_vel based on currently held keys."""
        self.x_vel = 0
        self.moving_x= False
        self.moving_y= False
        if keys[pg.K_a]:
            self.x_vel -= self.speed
            self.moving_x = True
        if keys[pg.K_d]:
            self.x_vel += self.speed
            self.moving_x = True

        if keys[pg.K_s]:
            self.y_vel += 1
            self.moving_y = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.y_vel -= 1
            self.moving_y = True

        if not self.moving_y:
            self.y_vel = 0
        if not self.moving_x:
            self.x_vel = 0;

        self.determine_fire_direction(keys)

    def determine_fire_direction(self, keys):

        isFiringX= False
        isFiringY = False
        if keys[pg.K_LEFT]:
            self.firing_x = -1
            isFiringX = True

        if keys[pg.K_RIGHT]:
            self.firing_x = 1
            isFiringX = True

        if keys[pg.K_DOWN]:
            self.firing_y = 1
            isFiringY = True

        if keys[pg.K_UP]:
            self.firing_y = -1
            isFiringY = True

        if not isFiringY:
            self.firing_y = 0;
        if not isFiringX:
            self.firing_x = 0;

        if isFiringX or isFiringY:

            if (time.time() - self.last_fire) > self.fire_rate:
                shot = PlayerShot(self.rect.topleft,self.firing_x,self.firing_y,self.shot_speed,self.damage)
                self.projectiles[shot.key] = shot
                self.last_fire = time.time()

    def jump(self):
        """Called when the user presses the jump button."""

    def update(self, obstacles, keys):
        """Everything we need to stay updated."""
        self.check_keys(keys)
        self.get_position(obstacles)

        to_remove = []
        for proj in self.projectiles.values():
            proj.update(to_remove,obstacles)

        for key in to_remove:
            self.projectiles.pop(key)

        self.physics_update()

    def draw(self,surface):
        """Blit the player to the target surface."""
        surface.blit(self.image, self.rect)
        for proj in self.projectiles.values():
            surface.blit(proj.image,proj.rect)
