import pygame
from sys import exit
from random import randint, choice

#player sprite
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    #player anim
    self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
    player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
    self.player_walk = [player_walk_1, player_walk_2]
    self.player_anim_index = 0

    self.image = self.player_walk[self.player_anim_index]
    self.rect = self.image.get_rect(midbottom = (80, 300))
    self.gravity = 0

  #player input for jumping
  def player_input(self):
    key_input = pygame.key.get_pressed()
    if self.rect.bottom >= 300:
      if key_input[pygame.K_SPACE] or key_input[pygame.K_UP]:
        self.gravity = -20

  #player gravity after jumping
  def apply_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    if self.rect.bottom >= 300:
      self.rect.bottom = 300

  #animation application
  def animation_state(self):
    if self.rect.bottom < 300:
      self.image = self.player_jump
    else:
      self.player_anim_index += 0.1
      if self.player_anim_index >= len(self.player_walk):
        self.player_anim_index = 0
      self.image = self.player_walk[int(self.player_anim_index)]

  #player methods
  def update(self):
    self.player_input()
    self.apply_gravity()
    self.animation_state()

class Enemy(pygame.sprite.Sprite):
  def __init__(self, type):
    super().__init__()

    if type == 'fly':
      fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
      fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
      self.anim_frames = [fly_1, fly_2]
      y_pos = 210
    else:
      snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
      snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
      self.anim_frames = [snail_1, snail_2]
      y_pos = 300

    self.anim_index = 0
    self.image = self.anim_frames[self.anim_index]
    self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

  def animation_state(self):
    self.anim_index += 0.1
    if self.anim_index >= len(self.anim_frames):
      self.anim_index = 0
    self.image = self.anim_frames[int(self.anim_index)]

  def update(self):
    self.animation_state()
    self.rect.x -= 6
    self.destroy()

  def destroy(self):
    if self.rect.x <= -100:
      self.kill()

def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_message = game_font.render(f'Score: {score}', False, (64, 64, 64))
  score_message_rect = score_message.get_rect(center = (400, 75))
  SCREEN.blit(score_message, score_message_rect)
  return current_time

#initiate game
pygame.init()

#initial attributes
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 400
game_clock = pygame.time.Clock()
game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_name = pygame.display.set_caption('Runner Game by Clear Code')
score = 0

#display screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

#intro screen
game_title = game_font.render('Runner Game', False, (64, 64, 64))
game_title_rect = game_title.get_rect(center = (400, 75))
game_subtitle = game_font.render('by Clear Code', False, (64, 64, 64))
game_subtitle = pygame.transform.rotozoom(game_subtitle, 0, 0.7)
game_subtitle_rect = game_subtitle.get_rect(center = (400, 100))

game_message = game_font.render('Press "Space" to start', False, (64, 64, 64))
game_message_rect = game_message.get_rect(center = (400, 250))

#render background (sky & ground)
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#render player character
player = pygame.sprite.GroupSingle()
player.add(Player())

#render enemy characters
enemy = pygame.sprite.Group()
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

#game state
game_active = False
start_time = 0

while True:


  for event in pygame.event.get():
    #how to quit the game
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    
    if game_active:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        game_active = False
      if event.type == enemy_timer:
        enemy.add(Enemy(choice(['fly', 'snail', 'snail', 'snail'])))
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        exit()
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        start_time = int(pygame.time.get_ticks() / 1000)

  #render background
  SCREEN.blit(sky_surf, (0, 0))
  SCREEN.blit(ground_surf, (0, 300))
  
  if game_active:
    #game starts

    player.draw(SCREEN)
    player.update()

    enemy.draw(SCREEN)
    enemy.update()

    score = display_score()
  
  else:
    #game intro/game over
    SCREEN.blit(game_title, game_title_rect)
    SCREEN.blit(game_subtitle, game_subtitle_rect)
    score_result = game_font.render(f'Score: {score}', False, (64, 64, 64))
    score_result_rect = score_result.get_rect(center = (400, 250))


    if score == 0:
      #game message/instruction
      SCREEN.blit(game_message, game_message_rect)
    else:
      #game score
      SCREEN.blit(score_result, score_result_rect)
  
  pygame.display.update()
  game_clock.tick(60)