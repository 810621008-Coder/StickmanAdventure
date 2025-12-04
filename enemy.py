import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y # 設定底部對齊
        
        self.start_x = x
        self.distance = distance
        self.walk_count = 0
        self.speed = 2
        self.direction = 1 # 1 為向右，-1 為向左

    def update(self):
        # 左右巡邏邏輯
        self.rect.x += self.speed * self.direction
        self.walk_count += self.speed
        
        # 如果走超過設定距離，就回頭
        if self.walk_count >= self.distance:
            self.direction *= -1
            self.walk_count = 0
        # 如果走回原點(或超過)，也回頭 (這裡簡化處理，直接用計數器控制來回)
