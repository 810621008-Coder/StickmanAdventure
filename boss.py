import pygame
import random
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED * direction

    def update(self):
        self.rect.x += self.speed
        # 子彈超出螢幕太遠就刪除 (這裡簡單判斷，實際上應該根據世界座標)
        # 但因為我們有 shift_world，所以這裡不需要特別處理，
        # 只要在 main.py 裡把子彈也加入 shift_world 即可。
        
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        width = BOSS_WIDTH if type == 'mini' else BOSS_WIDTH * 1.5
        height = BOSS_HEIGHT if type == 'mini' else BOSS_HEIGHT * 1.5
        color = ORANGE if type == 'mini' else DARK_RED
        self.hp = 3 if type == 'mini' else 5
        
        self.image = pygame.Surface((int(width), int(height)))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        
        self.speed = 2
        self.direction = -1 # 初始向左
        self.move_counter = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000 if type == 'mini' else 1500

    def update(self):
        # 移動邏輯
        if self.type == 'mini':
            # 小 Boss: 簡單左右巡邏
            self.rect.x += self.speed * self.direction
            self.move_counter += 1
            if self.move_counter > 100:
                self.direction *= -1
                self.move_counter = 0
        else:
            # 大 Boss: 移動範圍更大，速度稍快
            self.rect.x += self.speed * self.direction * 1.5
            self.move_counter += 1
            if self.move_counter > 150:
                self.direction *= -1
                self.move_counter = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # 發射子彈 (方向跟隨 Boss 面向)
            return Bullet(self.rect.centerx, self.rect.centery, self.direction)
        return None
