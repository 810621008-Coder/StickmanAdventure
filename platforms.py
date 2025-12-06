import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, move_x=0, move_y=0, move_dist=0):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 移動平台設定
        self.move_x = move_x
        self.move_y = move_y
        self.move_dist = move_dist
        self.start_x = x
        self.start_y = y
        self.traveled = 0
        self.direction = 1
        self.current_dx = 0
        self.current_dy = 0

    def update(self):
        # 重置當前幀的移動量
        self.current_dx = 0
        self.current_dy = 0

        # 如果有設定移動速度
        if self.move_x != 0 or self.move_y != 0:
            dx = self.move_x * self.direction
            dy = self.move_y * self.direction
            
            self.rect.x += dx
            self.rect.y += dy
            
            self.current_dx = dx
            self.current_dy = dy
            
            self.traveled += abs(dx) + abs(dy)
            
            if self.traveled >= self.move_dist:
                self.direction *= -1
                self.traveled = 0
