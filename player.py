import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 暫時用綠色方塊代表主角
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        
        # 設定初始位置 (螢幕中間偏下)
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # 速度與加速度向量
        self.vel_y = 0
        self.vel_x = 0
        self.acc_x = 0
        
        # 是否在地面上 (用於判斷能否跳躍)
        self.on_ground = False

    def jump(self):
        # 只有在地面上時才能跳躍
        if self.on_ground:
            self.vel_y = PLAYER_JUMP
            self.on_ground = False

    def update(self):
        self.acc_x = 0
        
        # 取得按鍵輸入
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc_x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc_x = PLAYER_ACC

        # 應用物理公式
        # 1. 加上摩擦力 (讓移動更自然，不會無限加速)
        self.acc_x += self.vel_x * PLAYER_FRICTION
        
        # 2. 更新速度
        self.vel_x += self.acc_x
        self.vel_y += PLAYER_GRAVITY # 加上重力
        
        # 3. 更新位置
        self.rect.x += self.vel_x + 0.5 * self.acc_x
        self.rect.y += self.vel_y
        
        # 簡單的邊界檢查 (防止跑出螢幕左邊)
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0

        # 注意：我們移除了原本的「地板碰撞」程式碼
        # 現在碰撞偵測會交由 main.py 統一處理，以便支援多個平台
