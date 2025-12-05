import pygame
import random
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

class FallingEnemy(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 100, 100)) # 淺紅色
        self.rect = self.image.get_rect()
        # 隨機在螢幕寬度內生成
        self.rect.x = random.randrange(0, SCREEN_WIDTH - 30)
        self.rect.y = -40 # 從螢幕上方掉下來
        self.platforms = platforms
        self.speed = 2
        self.direction = 0 # 0: 尚未決定方向, 1: 向右, -1: 向左

    def update(self):
        # 慢慢往下飄降
        self.rect.y += 2
        
        # 平台碰撞偵測
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            lowest = hits[0]
            # 如果在平台上方，就停在平台上
            if self.rect.bottom < lowest.rect.bottom + 10:
                self.rect.bottom = lowest.rect.top
                # 落地後決定方向 (只決定一次)
                if self.direction == 0:
                    self.direction = random.choice([-1, 1])
        
        # 如果已經決定方向，就持續移動
        if self.direction != 0:
            self.rect.x += self.speed * self.direction

        # 掉出螢幕或走出左右邊界就刪除
        if self.rect.top > SCREEN_HEIGHT or self.rect.right < -50 or self.rect.left > SCREEN_WIDTH + 50:
            self.kill()
