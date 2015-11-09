import pygame as pg
import time
import shot
import pickup

PLAYER_TYPE = 'player'

class Player(pg.sprite.Sprite):

    """Class representing our player."""
    def __init__(self,location):
        """
        The location is an (x,y) coordinate pair, and speed is the player's
        speed in pixels per frame. Speed should be an integer.
        """
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
        self.type = 'player'
        self.trinkets = []
        self.items = []
        self.consumables = []
        self.type = PLAYER_TYPE
        self.health = 3
        self.fire_rate = .5
        self.shot_speed = 10;
        self.damage = 5
        self.speed = 5
        self.rect = self.image.get_rect(topleft=location)

    def get_position(self, obstacles):
        """Calculate the player's position this frame, including collisions."""
        self.can_move = self.check_collisions((self.x_vel,self.y_vel), 1, obstacles)
        if self.can_move:
            if self.x_vel:
                self.move_x()
            if self.y_vel:
                self.move_y()

    def move_x(self):
        self.rect.move_ip(self.x_vel,0)

    def move_y(self):
        self.rect.move_ip(0,self.y_vel)

    def check_collisions(self, offset, index, obstacles):
        """
        This function checks if a collision would occur after moving offset
        pixels.  If a collision is detected position is decremented PLAYER_TYPEby one
        pixel and retested. This continues until we find exactly how far we can
        safely move, or we decide we can't move.
        """
        unaltered = True
        self.rect.move_ip(offset)
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        collidable = pg.sprite.collide_mask
        if len(collisions) >0:
            for coll in collisions:
                if coll.type == pickup.PICKUP:
                    coll.bePickedUp(self)
            unaltered = False
        self.rect.move_ip((-offset[0],-offset[1]))
        return unaltered

    def check_keys(self, keys,now):
        """Find the player's self.x_vel based on currently held keys."""
        self.x_vel = 0
        self.y_vel = 0
        self.moving_x= False
        self.moving_y= False
        if keys[pg.K_a]:
            self.x_vel -= self.speed
            self.moving_x = True
        if keys[pg.K_d]:
            self.x_vel += self.speed
            self.moving_x = True

        if keys[pg.K_s]:
            self.y_vel += self.speed
            self.moving_y = True
        if keys[pg.K_w]:
            self.y_vel -= self.speed
            self.moving_y = True

        if not self.moving_y:
            self.y_vel = 0
        if not self.moving_x:
            self.x_vel = 0;

        self.determine_fire_direction(keys, now)

    def determine_fire_direction(self, keys, now):

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
                mShot = shot.BouncyShot(self.rect.topleft,self.firing_x,self.firing_y,self.shot_speed,self.damage,PLAYER_TYPE,now)
                self.projectiles[mShot.key] = mShot
                self.last_fire = time.time()

    def jump(self):
        """Called when the user presses the jump button."""

    def update(self, obstacles, keys, now):
        """Everything we need to stay updated."""
        self.check_keys(keys,now)
        self.get_position(obstacles)

        to_remove = []
        for proj in self.projectiles.values():
            proj.update(to_remove,obstacles,now)

        for key in to_remove:
            self.projectiles.pop(key)

    def draw(self,surface):
        """Blit the player to the target surface."""
        surface.blit(self.image, self.rect)
        for proj in self.projectiles.values():
            proj.draw(surface)

    def take_damage(self,projectile):
        self.health -= projectile.damage
        if self.health <=0:
            self.kill()