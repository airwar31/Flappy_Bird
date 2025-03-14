import pygame.sprite

import assets
import configs
from layer import Layer
from objects.column import Column
from objects.floor import Floor


class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PLAYER

        self.images = [
            assets.get_sprite("redbird-upflap"),
            assets.get_sprite("redbird-midflap"),
            assets.get_sprite("redbird-downflap")
        ]

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(-50, configs.SCREEN_HEIGHT // 2))

        self.mask = pygame.mask.from_surface(self.image)

        self.flap = 0
        self.rotation = 0

        super().__init__(*groups)

    def update(self):
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]

        self.flap += configs.GRAVITY
        self.rect.y += self.flap

        if self.flap < 0:
            self.rotation = max(-25, self.rotation - 2)
        else: 

            self.rotation = min(70, self.rotation + 1.5)

        original_center = self.rect.center
        rotated_image = pygame.transform.rotate(self.images[0], self.rotation)
        self.rect = rotated_image.get_rect(center=original_center)
        self.image = rotated_image

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.x < 50:
            self.rect.x += 3

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.rotation = -20

            self.flap = -6.5
            
            assets.play_audio("wing")

    def check_collision(self, sprites):
        for sprite in sprites:
            if ((type(sprite) is Column or type(sprite) is Floor) and sprite.mask.overlap(self.mask, (
                    self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)) or
                    self.rect.bottom < 0):
                return True
        return False
