import pygame as pg

class Player(pg.sprite.Sprite):

    """Class representing our player."""
    def __init__(self,location):
        self.health = 10
        self.image = pg.image.load("base_face.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=location)

    def draw(self,surface):
        """Blit the player to the target surface."""
        surface.blit(self.image, self.rect)