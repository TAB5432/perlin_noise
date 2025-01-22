import pygame
from random import randint
import sys
import math
from math import sin, cos
import numpy as np
from pygame.locals import *
import noise

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

icon = pygame.image.load("player.png").convert_alpha()
icon = pygame.transform.rotate(icon, 90)

pygame.display.set_icon(icon)
pygame.display.set_caption("Endless Onslaught")

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*3.5), int(self.image.get_height()*3.5)))
        self.original_image = self.image
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)

        self.rotation = 0
        self.rotating_left = False
        self.rotating_right = False

        self.moving_forwards = False
        self.moving_backwards = False
        self.dx = 0
        self.dy = 0

        self.speed = 7
        

    
        

    def update(self):
        
        if self.rotating_left:
            self.rect.x += -10
        elif self.rotating_right:
            self.rect.x += 10
            
        
        self.dx = cos(math.radians(self.rotation)) 
        self.dy = sin(math.radians(self.rotation)) 

        if self.moving_forwards:  
            self.rect.y -= 10


        elif self.moving_backwards:
            self.rect.y += 10
        

        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))
        self.mask = pygame.mask.from_surface(self.image)
        
    def spawn(self):
        player_group.add(self)

    def despawn(self):
        player_group.remove(self)

    def draw(self):
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, rotation):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*3.5), int(self.image.get_height()*3.5)))
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect(center = (x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx * 22
        self.rect.y -= self.dy * 22

        if self.rect.left > self.rect.centerx + SCREEN_WIDTH // 2 or self.rect.right < player.rect.centerx - SCREEN_WIDTH // 2\
        or self.rect.bottom < player.rect.centery - SCREEN_HEIGHT // 2 or self.rect.top > player.rect.centery + SCREEN_HEIGHT // 2:
                self.despawn()
        

    def spawn(self):
        bullet_group.add(self)

    def despawn(self):
        bullet_group.remove(self)

    def draw(self):
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        

class Game():
    def __init__(self):
        self.running = True
        
        

game = Game()

player_group = pygame.sprite.Group()
player = Player()
player.spawn()

bullet_group = pygame.sprite.Group()

width = 1920
height = 1080
scale = 0.01
octaves = 8
persistence = 0.6
lacunarity = randint(2, 3)


true_scroll = [0, 0]

t1 = pygame.image.load("tile1.png").convert()
t1 = pygame.transform.scale(t1, (int(t1.get_width()*0.1), int(t1.get_height()*0.1)))

t2 = pygame.image.load("tile2.png").convert()
t2 = pygame.transform.scale(t2, (int(t2.get_width()*0.1), int(t2.get_height()*0.1)))

t3 = pygame.image.load("tile3.png").convert()
t3 = pygame.transform.scale(t3, (int(t3.get_width()*0.1), int(t3.get_height()*0.1)))

t4 = pygame.image.load("tile4.png").convert()
t4 = pygame.transform.scale(t4, (int(t4.get_width()*0.1), int(t4.get_height()*0.1)))



tile_index = {1:t1,
              2:t2,
              3:t3,
              4:t4
              }
game_map = {}
CHUNK_SIZE = 80
def generate_chunk(x, y):
    chunk_data = []
    for y_pos  in range(CHUNK_SIZE):
        for x_pos  in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            
            value = noise.pnoise2(target_x * scale, target_y * scale, octaves, persistence, lacunarity)
            if value < -0.1:
                tile_type = 1
                    
            elif value < 0:
                tile_type = 2
                
            elif value < 0.4:
                tile_type = 3
                
            else:
                tile_type = 4
                    
            chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.rotating_left = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.rotating_right = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.moving_forwards = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.moving_backwards = True
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.centery, player.dx, player.dy, player.rotation)
                bullet.spawn()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.rotating_left = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.rotating_right = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.moving_forwards = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
               player.moving_backwards = False

while game.running:
     
    true_scroll[0] += (player.rect.centerx - true_scroll[0] - SCREEN_WIDTH // 2) // 3
    true_scroll[1] += (player.rect.centery - true_scroll[1] - SCREEN_HEIGHT //2) // 3
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    
    check_events()
               
    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 96*0.1)))
            target_y = y - 1+ int(round(scroll[1] / (CHUNK_SIZE * 96*0.1)))
            target_chunk = str(target_x) + ";" + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            for tile in game_map[target_chunk]:
                screen.blit(tile_index[tile[1]], (tile[0][0] * 96*0.1 - scroll[0], tile[0][1]* 96*0.1 - scroll[1]))
        
            
                
    player.update()
    player.draw()

    for bullet in bullet_group:
        bullet.update()
        bullet.draw()
    
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
sys.exit()