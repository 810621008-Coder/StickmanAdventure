import math
import random
import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # 繪製紅色怪物 (像是一個紅色的小幽靈或史萊姆)
        # 身體 (圓頂 + 下方矩形)
        pygame.draw.circle(self.image, RED, (15, 15), 15)
        pygame.draw.rect(self.image, RED, (0, 15, 30, 15))
        
        # 憤怒的眼睛
        # 眼白
        pygame.draw.circle(self.image, WHITE, (10, 12), 4)
        pygame.draw.circle(self.image, WHITE, (20, 12), 4)
        # 眼珠
        pygame.draw.circle(self.image, BLACK, (10, 12), 2)
        pygame.draw.circle(self.image, BLACK, (20, 12), 2)
        # 眉毛 (斜線表現憤怒)
        pygame.draw.line(self.image, BLACK, (5, 8), (12, 11), 2)
        pygame.draw.line(self.image, BLACK, (25, 8), (18, 11), 2)

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
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # 繪製尖刺球
        # 核心
        pygame.draw.circle(self.image, (100, 100, 100), (15, 15), 10)
        # 尖刺 (十字和斜向線條)
        pygame.draw.line(self.image, (200, 200, 200), (15, 0), (15, 30), 2)
        pygame.draw.line(self.image, (200, 200, 200), (0, 15), (30, 15), 2)
        pygame.draw.line(self.image, (200, 200, 200), (5, 5), (25, 25), 2)
        pygame.draw.line(self.image, (200, 200, 200), (5, 25), (25, 5), 2)
        
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

class PopUpEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, delay=0, hidden_time=100, wait_time=60):
        super().__init__()
        self.x = x
        self.base_y = y
        self.width = 40
        self.max_height = 60
        self.current_height = 0
        self.image = pygame.Surface((self.width, 1))
        self.image.fill(DARK_GREEN)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        
        self.state = 'HIDDEN' # HIDDEN, RISING, WAITING, LOWERING
        self.timer = -delay # 負值代表延遲啟動
        self.hidden_time = hidden_time
        self.wait_time = wait_time
        self.speed = 2
        self.animation_count = 0

    def update(self):
        self.animation_count += 0.1 # 控制擺動速度
        
        if self.state == 'HIDDEN':
            self.timer += 1
            if self.timer > self.hidden_time:
                self.state = 'RISING'
                self.timer = 0
        
        elif self.state == 'RISING':
            self.current_height += self.speed
            if self.current_height >= self.max_height:
                self.current_height = self.max_height
                self.state = 'WAITING'
            self.update_image()
            
        elif self.state == 'WAITING':
            self.timer += 1
            if self.timer > self.wait_time:
                self.state = 'LOWERING'
                self.timer = 0
            self.update_image() # 呼叫 update_image 來產生擺動
                
        elif self.state == 'LOWERING':
            self.current_height -= self.speed
            if self.current_height <= 0:
                self.current_height = 0
                self.state = 'HIDDEN'
            self.update_image()

    def update_image(self):
        # 保存當前的中心點 x 座標 (因為世界卷軸會改變它)
        current_centerx = self.rect.centerx
        
        if self.current_height > 0:
            self.image = pygame.Surface((self.width + 20, int(self.current_height)), pygame.SRCALPHA)
            
            # 計算頭部擺動偏移
            # 幅度約正負 10 像素
            head_offset_x = math.sin(self.animation_count) * 10
            
            # 確保圖像中心對齊
            img_center_x = (self.width + 20) // 2
            
            # 莖 (動態彎曲效果很難做，用直線連接底部和頭部)
            start_pos = (img_center_x, int(self.current_height))
            end_pos = (img_center_x + head_offset_x, 30 if self.current_height >=30 else int(self.current_height))
            
            # 莖 (綠色) - 使用簡單的直線
            pygame.draw.line(self.image, DARK_GREEN, start_pos, end_pos, 8)
            
            # 頭部 (紅色，只有當高度足夠時才畫完整的頭)
            if self.current_height >= 30:
                # 頭部中心
                head_x = img_center_x + head_offset_x
                head_y = 15
                
                # 頭部圓形
                pygame.draw.circle(self.image, RED, (int(head_x), int(head_y)), 15)
                
                # 根據擺動方向決定面向 (向右擺看向右，向左擺看向左)
                facing_right = head_offset_x > 0
                
                if facing_right:
                    # 嘴巴 (向右張開)
                    pygame.draw.polygon(self.image, BLACK, [(head_x, head_y), (head_x + 12, head_y - 8), (head_x + 12, head_y + 8)])
                    # 牙齒
                    pygame.draw.polygon(self.image, WHITE, [(head_x + 5, head_y - 2), (head_x + 10, head_y - 5), (head_x + 8, head_y)])
                    # 眼睛 (向右看) - 畫在左上方
                    pygame.draw.circle(self.image, WHITE, (int(head_x) - 5, int(head_y) - 5), 4)
                    pygame.draw.circle(self.image, BLACK, (int(head_x) - 3, int(head_y) - 5), 2)
                else:
                    # 嘴巴 (向左張開)
                    pygame.draw.polygon(self.image, BLACK, [(head_x, head_y), (head_x - 12, head_y - 8), (head_x - 12, head_y + 8)])
                    # 牙齒
                    pygame.draw.polygon(self.image, WHITE, [(head_x - 5, head_y - 2), (head_x - 10, head_y - 5), (head_x - 8, head_y)])
                    # 眼睛 (向左看) - 畫在右上方
                    pygame.draw.circle(self.image, WHITE, (int(head_x) + 5, int(head_y) - 5), 4)
                    pygame.draw.circle(self.image, BLACK, (int(head_x) + 3, int(head_y) - 5), 2)

            self.rect = self.image.get_rect()
            self.rect.size = (self.width + 20, int(self.current_height))
            self.rect.midbottom = (current_centerx, self.base_y)
        else:
            # 保持一個極小的 rect 以免出錯，但設為透明
            self.image = pygame.Surface((self.width, 1), pygame.SRCALPHA)
            self.image.set_alpha(0)
            self.rect = self.image.get_rect()
            self.rect.centerx = current_centerx
            self.rect.bottom = self.base_y
