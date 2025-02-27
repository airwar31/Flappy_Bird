import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.restart_button import RestartButton
from objects.score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird Game v1.0.2")
        
        icon = pygame.image.load('assets/icons/red_bird.png')
        pygame.display.set_icon(icon)
        
        self.clock = pygame.time.Clock()
        self.column_create_event = pygame.USEREVENT

        self.running = True
        self.gameover = False
        self.gamestarted = False

        assets.load_sprites()
        assets.load_audios()

        self.sprites = pygame.sprite.LayeredUpdates()

        self.bird, self.game_start_message, self.score = self.create_sprites()
    
    def create_sprites(self):
        Background(0, self.sprites)
        Background(1, self.sprites)
        Floor(0, self.sprites)
        Floor(1, self.sprites)
        
        return Bird(self.sprites), GameStartMessage(self.sprites), Score(self.sprites)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == self.column_create_event:
                Column(self.sprites)
                
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and self.gameover:
                self.handle_mouse_event(event)
            
            if not self.gameover:
                self.bird.handle_event(event)
    
    def handle_keydown_event(self, event):
        if event.key == pygame.K_SPACE and not self.gamestarted and not self.gameover:
            self.start_game()
        elif event.key == pygame.K_ESCAPE and self.gameover:
            self.restart_game()
    
    def handle_mouse_event(self, event):
        for sprite in self.sprites:
            if isinstance(sprite, RestartButton) and sprite.is_clicked(event.pos):
                self.restart_game()
    
    def start_game(self):
        self.gamestarted = True
        self.game_start_message.kill()
        pygame.time.set_timer(self.column_create_event, 1500)
    
    def restart_game(self):
        self.gameover = False
        self.gamestarted = False

        best_score = self.score.best_score
        self.sprites.empty()

        self.bird, self.game_start_message, self.score = self.create_sprites()
        self.score.best_score = best_score
    
    def check_collisions(self):
        if self.bird.check_collision(self.sprites) and not self.gameover:
            self.gameover = True
            self.gamestarted = False
            GameOverMessage(self.sprites)
            RestartButton(self.sprites)
            pygame.time.set_timer(self.column_create_event, 0)
            assets.play_audio("hit")
    
    def check_score(self):
        for sprite in self.sprites:
            if type(sprite) is Column and sprite.is_passed():
                self.score.value += 1
                assets.play_audio("point")
    
    def update(self):
        if self.gamestarted and not self.gameover:
            self.sprites.update()
            
        self.check_collisions()
        self.check_score()
    
    def render(self):
        self.screen.fill(0)
        self.sprites.draw(self.screen)
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(configs.FPS)
        
        pygame.quit()