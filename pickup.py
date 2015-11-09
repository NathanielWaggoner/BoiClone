import pygame as pg

PICKUP = "PICKUP"
HEALTH_PICKUP = "HEALTH"
FunkyPickup = "FUNKY"

class Pickup(pg.sprite.Sprite):

    def __init__(self,location, image, mType):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image).convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=location)
        self.type = PICKUP
        self.pickup_type= mType

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class HealthPickup(Pickup):

    def __init__(self,location):
        Pickup.__init__(self,location,"health_up.png",HEALTH_PICKUP)
        self.health_bonus = 10

    def bePickedUp(self,consumer):
        consumer.health+= self.health_bonus
        self.kill()

class FunkyPickup(Pickup):

    def __init__(self,location):
        Pickup.__init__(self,location,"funky_pickup.png",FunkyPickup)
        self.shot_freq_mult = .7

    def bePickedUp(self,consumer):
        consumer.fire_rate = consumer.fire_rate*self.shot_freq_mult
        self.kill()
