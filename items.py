import pygame
import math
import random
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

class QuestionBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_y = y
        self.active = True
        self.bump_timer = 0
        
        # 隨機決定獎勵
        # life_up: 加命 (+1)
        # life_down: 扣命 (-1)
        # score_100: 特殊金幣 (+100分)
        self.reward = random.choice(['life_up', 'life_down', 'score_100'])

        # 初始化字型 (用於繪製問號)
        self.font_name = pygame.font.match_font('arial', bold=True)
        # 如果找不到 arial，會使用預設字型
        self.font = pygame.font.Font(self.font_name, 30) if self.font_name else pygame.font.SysFont(None, 30)
        
        self.draw_block()

    def draw_block(self):
        if self.active:
            self.image.fill((255, 215, 0)) # 金黃色背景
            pygame.draw.rect(self.image, (200, 150, 0), (0, 0, 40, 40), 4) # 邊框
            
            # 繪製黑底綠邊中空問號 (置中，調暗一點，點與鉤分開)
            text = "?"
            # 使用稍微沒那麼刺眼的綠色
            outline_green = (0, 200, 0) 
            black = (0, 0, 0)
            
            # 設定基準位置 
            base_cx, base_cy = 20, 16  # 文字中心 (往上移，原本19，讓鉤子更高)
            dot_cy = 31                # 點的中心 (往下移，原本29，讓點更低)
            dot_r = 3                  # 點的半徑

            # 1. 繪製文字 (包含外框與本體)
            # 為了讓鉤子和原本的點分開，我們先畫出文字，然後把原本文字的點「蓋掉」，再自己畫一個點
            
            offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]
            for dx, dy in offsets:
                outline_surface = self.font.render(text, True, outline_green)
                outline_rect = outline_surface.get_rect(center=(base_cx + dx, base_cy + dy))
                self.image.blit(outline_surface, outline_rect)
            
            # 文字本體
            text_surface = self.font.render(text, True, black)
            text_rect = text_surface.get_rect(center=(base_cx, base_cy))
            self.image.blit(text_surface, text_rect)
            
            # 2. 遮罩：用背景色方塊蓋掉字體原本的點 (避免重疊或距離不夠)
            # 預設字體大小 30，中心在 y=16，點大約會在 y=26~30 之間
            mask_rect = pygame.Rect(12, 24, 16, 12)
            pygame.draw.rect(self.image, (255, 215, 0), mask_rect)

            # 3. 繪製手動的點 (外框+本體) - 畫在新的位置
            # 點的外框
            pygame.draw.circle(self.image, outline_green, (base_cx, dot_cy), dot_r + 2)
            # 點的本體
            pygame.draw.circle(self.image, black, (base_cx, dot_cy), dot_r)
            
        else:
            self.image.fill((139, 69, 19)) # 褐色 (已撞擊)
            pygame.draw.rect(self.image, (100, 50, 0), (0, 0, 40, 40), 4)

    def hit(self):
        if self.active:
            self.active = False
            self.bump_timer = 10 # 撞擊動畫計時
            self.draw_block()
            return self.reward
        return None

    def update(self):
        # 撞擊時的彈跳動畫
        if self.bump_timer > 0:
            if self.bump_timer > 5:
                self.rect.y -= 2
            else:
                self.rect.y += 2
            self.bump_timer -= 1
        else:
            self.rect.y = self.original_y

class SuperCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 60 # 顯示 1 秒
        self.frame = 0

    def update(self):
        self.rect.y -= 2 # 快速升起
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
        
        # 閃爍效果 (紅/黃交替)
        self.frame += 1
        self.image.fill((0,0,0,0))
        color = RED if (self.frame // 5) % 2 == 0 else YELLOW
        pygame.draw.circle(self.image, color, (15, 15), 14)
        pygame.draw.circle(self.image, WHITE, (15, 15), 10, 2)
        # 內部寫個 100
        # 這裡簡單畫個圖形就好，不用寫字了，因為外面會有 FloatText

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color=(0, 255, 0), size=30): # 預設大小加大
        super().__init__()
        self.font_name = pygame.font.match_font('arial', bold=True) # 使用粗體
        self.font = pygame.font.Font(self.font_name, size)
        
        # 製作描邊效果
        # 1. 建立文字本體
        text_surface = self.font.render(text, True, color)
        # 2. 建立黑色外框文字
        outline_surface = self.font.render(text, True, (0, 0, 0))
        
        # 建立一個夠大的容器來放含描邊的字 (加大邊界以免被切到)
        w, h = text_surface.get_size()
        border = 6 # 加大邊界
        self.image = pygame.Surface((w + border*2, h + border*2), pygame.SRCALPHA)
        
        # 繪製黑色外框 (8方向偏移)
        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in offsets:
            self.image.blit(outline_surface, (dx + border, dy + border))
            
        # 繪製本體
        self.image.blit(text_surface, (border, border))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 60 # 顯示 1 秒
        self.vel_y = -2 # 上升速度稍微快一點
        
    def update(self):
        self.rect.y += self.vel_y
        # 加入簡單的減速效果，讓文字飄動更有質感
        self.vel_y *= 0.95 
        
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
