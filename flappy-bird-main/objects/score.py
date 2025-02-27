import os
import pygame.sprite

import assets
import configs
from layer import Layer


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.value = 0
        self.best_score = self._load_best_score()
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)

        self.__create()

        super().__init__(*groups)

    def _load_best_score(self):

        if os.path.exists(configs.BEST_SCORE_FILE):
            try:
                with open(configs.BEST_SCORE_FILE, 'r') as f:
                    return int(f.read().strip())
            except (ValueError, IOError):

                return 0
        return 0
    
    def _save_best_score(self):
        with open(configs.BEST_SCORE_FILE, 'w') as f:
            f.write(str(self.best_score))

    def __create(self):

        self.str_value = str(self.value)
        self.images = []
        self.width = 0

        for str_value_char in self.str_value:
            img = assets.get_sprite(str_value_char)
            self.images.append(img)
            self.width += img.get_width()

        self.height = self.images[0].get_height()
        

        self.str_best = str(self.best_score)
        

        total_width = self.width
        total_height = self.height
        
        self.image = pygame.surface.Surface((total_width, total_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, 50))

        x_offset = 0
        x = x_offset
        for img in self.images:
            self.image.blit(img, (x, 0))
            x += img.get_width()

    def update(self):

        if self.value > self.best_score:
            self.best_score = self.value
            self._save_best_score()
        self.__create()
