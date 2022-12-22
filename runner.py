import pygame
from sys import exit
from random import randint, choice
# from pygame.locals import (
#   K_UP,
#   K_SPACE,
#   K_ESCAPE,
#   KEYDOWN,
# )

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
    player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
    self.player_walk = [player_walk_1, player_walk_2]
    self.player_anim_index = 0

    self.image = self.player_walk[self.player_anim_index]
    self.rect = self.image.get_rect(midbottom = (80, 300))
    self.gravity = 0

  def player_input(self):
    key_input = pygame.key.get_pressed()
    if self.rect.bottom >= 300:
      if key_input[pygame.K_SPACE] or key_input[pygame.K_UP]:
        self.gravity = -20
    

  def apply_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    if self.rect.bottom >= 300:
      self.rect.bottom = 300

  def animation_state(self):
    if self.rect.bottom < 300:
      self.image = self.player_jump
    else:
      self.player_anim_index += 0.1
      if self.player_anim_index >= len(self.player_walk):
        self.player_anim_index = 0
      self.image = self.player_walk[int(self.player_anim_index)]

  def update(self):
    self.player_input()
    self.apply_gravity()
    self.animation_state()


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGTH = 400
game_clock = pygame.time.Clock()
game_font = pygame.font.Font('font/Pixeltype.ttf', 50)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

player = pygame.sprite.GroupSingle()
player.add(Player())

game_active = False

while True:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      pygame.quit()
      exit()

  SCREEN.blit(sky_surf, (0, 0))
  SCREEN.blit(ground_surf, (0, 300))

  player.draw(SCREEN)
  player.update()

  pygame.display.update()
  game_clock.tick(60)