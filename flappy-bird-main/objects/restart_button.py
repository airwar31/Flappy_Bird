import pygame.sprite

import assets
import configs
from layer import Layer


class RestartButton(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = pygame.image.load('assets/sprites/restart_button.png').convert_alpha()
        if self.image.get_width() == 0:
            self.image = pygame.Surface((100, 50))
            self.image.fill((242, 80, 34)) 
            font = pygame.font.SysFont('Arial', 20)
            text = font.render("Restart", True, (255, 255, 255))
            text_rect = text.get_rect(center=(50, 25))
            self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2 + 100))
        super().__init__(*groups)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)