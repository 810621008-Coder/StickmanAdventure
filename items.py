import pygame
import math
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_frame = 0
        
    def update(self):
        self.animation_frame += 0.2
        self.image.fill((0, 0, 0, 0)) # 清空
        
        # 旋轉效果：透過改變寬度模擬
        width_scale = abs(math.sin(self.animation_frame))
        current_width = int(22 * width_scale)
        if current_width < 2: current_width = 2
        
        center_x, center_y = 12, 12
        coin_rect = pygame.Rect(center_x - current_width // 2, center_y - 11, current_width, 22)
        
        # 外圈
        pygame.draw.ellipse(self.image, (255, 215, 0), coin_rect) # 金色
        pygame.draw.ellipse(self.image, (200, 150, 0), coin_rect, 2) # 深金邊框
        
        # 內圈裝飾 ($ 符號太複雜，用簡單線條代替)
        if current_width > 8:
            inner_rect = pygame.Rect(center_x - current_width // 4, center_y - 8, current_width // 2, 16)
            pygame.draw.line(self.image, (255, 255, 200), (center_x, center_y - 6), (center_x, center_y + 6), 2)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 90), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 30 # 往上提，對齊地板
        
        self.animation_frame = 0

    def update(self):
        # 簡單的漩渦動畫
        self.animation_frame += 1
        self.image.fill((0, 0, 0, 0)) # 清空
        
        center = (30, 45)
        
        # 繪製多層橢圓模擬漩渦
        colors = [CYAN, PURPLE, WHITE]
        offset = (self.animation_frame // 5) % 3
        
        for i in range(3):
            # 依序切換顏色產生流動感
            color_idx = (i + offset) % 3
            radius_x = 30 - i * 8
            radius_y = 45 - i * 12
            if radius_x > 0 and radius_y > 0:
                rect = pygame.Rect(center[0] - radius_x, center[1] - radius_y, radius_x * 2, radius_y * 2)
                pygame.draw.ellipse(self.image, colors[color_idx], rect, 5)

class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        # 繪製公主的火柴人造型
        # 頭部
        pygame.draw.circle(self.image, PINK, (20, 15), 10, 2) 
        # 皇冠 (黃色三角形)
        pygame.draw.polygon(self.image, YELLOW, [(15, 8), (20, 2), (25, 8)])
        
        # 身體 (穿裙子)
        pygame.draw.line(self.image, PINK, (20, 25), (20, 40), 2)
        # 裙子 (三角形)
        pygame.draw.polygon(self.image, PINK, [(20, 40), (10, 55), (30, 55)], 2)
        
        # 手臂 (自然下垂)
        pygame.draw.line(self.image, PINK, (20, 30), (10, 40), 2)
        pygame.draw.line(self.image, PINK, (20, 30), (30, 40), 2)
        # 手 (圓形)
        pygame.draw.circle(self.image, (255, 220, 180), (10, 40), 3) # 皮膚色手
        pygame.draw.circle(self.image, (255, 220, 180), (30, 40), 3)

        # 臉部 (微笑)
        pygame.draw.circle(self.image, BLACK, (17, 14), 1)
        pygame.draw.circle(self.image, BLACK, (23, 14), 1)
        pygame.draw.arc(self.image, BLACK, (17, 14, 6, 6), 3.4, 6.0, 1)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 20

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((30, 30))
        if type == 'sword':
            self.image.fill((200, 200, 200)) # 銀色
        elif type == 'shield':
            self.image.fill((0, 0, 200)) # 藍色
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 60))
        self.image.fill((0, 150, 0)) # 綠色水管
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
