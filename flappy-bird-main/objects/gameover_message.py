import pygame.sprite
import pygame.font

import assets
import configs
from layer import Layer


class GameOverMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI

        score_instance = None
        for group in groups:
            for sprite in group:
                if sprite.__class__.__name__ == "Score":
                    score_instance = sprite
                    break
            if score_instance:
                break
        
        best_score = score_instance.best_score if score_instance else 0

        gameover_img = assets.get_sprite("gameover")

        font = pygame.font.SysFont('Arial', 30)
        best_score_text = font.render(f"BEST SCORE: {best_score}", True, (255, 255, 255))
        best_score_rect = best_score_text.get_rect()

        self.image = pygame.surface.Surface((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT), pygame.SRCALPHA)

        gameover_rect = gameover_img.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        self.image.blit(gameover_img, gameover_rect)

        best_score_rect.topleft = (20, configs.SCREEN_HEIGHT / 2 - 100)
        self.image.blit(best_score_text, best_score_rect)

        self.rect = self.image.get_rect(topleft=(0, 0))
        super().__init__(*groups)
