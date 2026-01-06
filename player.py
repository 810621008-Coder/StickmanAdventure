import pygame
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 使用透明背景，並以此基礎繪製火柴人
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # 設定初始位置 (螢幕中間偏下)
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # 速度與加速度向量
        self.vel_y = 0
        self.vel_x = 0
        self.acc_x = 0
        
        # 是否在地面上 (用於判斷能否跳躍)
        self.on_ground = False

        # 無敵狀態
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 2000 # 2秒

        # 載入音效
        try:
            self.jump_sound = pygame.mixer.Sound('jump.wav')
            self.jump_sound.set_volume(0.5)
        except:
            self.jump_sound = None

        # 裝備狀態
        self.has_sword = False
        self.has_shield = False
        self.is_attacking = False
        self.is_blocking = False
        self.attack_time = 0
        self.block_time = 0
        self.attack_cooldown = 500
        self.last_attack_time = 0

        # 動畫與狀態
        self.facing_right = True
        self.walk_count = 0 
        
        # 初始化一次圖像
        self.update_image()

    def update_image(self):
        # 清除畫布 (填入透明色)
        temp_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        temp_image.fill((0, 0, 0, 0))
        
        color = PLAYER_COLOR
        if self.is_attacking:
            color = YELLOW
        elif self.is_blocking:
            color = BLUE
            
        # 計算動畫偏移 (走路擺動)
        # 用 sin 函數產生 -1 到 1 的擺動
        swing = math.sin(self.walk_count) * 10
        swing_y = math.cos(self.walk_count) * 2 # 微微的上下起伏
        
        # 身體各部位座標 (預設面向右)
        head_pos = (20, 12 + int(abs(swing_y)))
        neck_pos = (20, 22 + int(abs(swing_y)))
        hip_pos = (20, 45 + int(abs(swing_y)))
        
        arm_pivot = (20, 30 + int(abs(swing_y)))
        
        # 繪製頭部
        pygame.draw.circle(temp_image, color, head_pos, 10, 2)
        
        # 繪製帽子 (紅色棒球帽)
        # 帽頂 (半圓)
        pygame.draw.arc(temp_image, RED, (10, head_pos[1]-12, 20, 20), 0, 3.14, 10) 
        # 帽舌 (往右指)
        pygame.draw.line(temp_image, RED, (head_pos[0], head_pos[1]-7), (head_pos[0]+16, head_pos[1]-5), 4)

        # 繪製身體
        pygame.draw.line(temp_image, color, neck_pos, hip_pos, 2)
        
        # 繪製腿部 (走路動畫)
        if self.on_ground and (self.acc_x != 0 or self.vel_x != 0):
            # 左腳 (後腳)
            pygame.draw.line(temp_image, color, hip_pos, (20 - swing, 60), 2)
            # 右腳 (前腳)
            pygame.draw.line(temp_image, color, hip_pos, (20 + swing, 60), 2)
        else:
            # 站立或跳躍中
            pygame.draw.line(temp_image, color, hip_pos, (15, 60), 2)
            pygame.draw.line(temp_image, color, hip_pos, (25, 60), 2)

        # 繪製手臂與裝備
        if self.is_attacking:
            # 攻擊姿勢：右手舉起劍
            # 右手
            pygame.draw.line(temp_image, color, arm_pivot, (35, 20), 2)
            # 劍
            pygame.draw.line(temp_image, (150, 75, 0), (35, 20), (38, 17), 3) 
            pygame.draw.line(temp_image, (200, 200, 200), (38, 17), (50, 5), 4)
            # 左手
            pygame.draw.line(temp_image, color, arm_pivot, (10, 40), 2)
            
        elif self.is_blocking:
            # 防禦姿勢：左手持盾在前
            # 左手
            pygame.draw.line(temp_image, color, arm_pivot, (25, 35), 2)
            # 盾牌
            pygame.draw.circle(temp_image, BLUE, (30, 35), 12)
            pygame.draw.circle(temp_image, WHITE, (30, 35), 12, 1)
            # 右手
            pygame.draw.line(temp_image, color, arm_pivot, (10, 40), 2)
            
        else:
            # 一般姿勢 (手臂擺動與腿相反)
            if self.on_ground and (self.acc_x != 0 or self.vel_x != 0):
                # 左手 (對應右腳，所以offset相反: -swing)
                pygame.draw.line(temp_image, color, arm_pivot, (20 - swing * 0.8, 40), 2)
                # 右手 (對應左腳，所以offset: +swing)
                # 但為了自然，手通常和對側腳同步。
                # 右手(前) vs 左腳(後) -> swing vs -swing
                # 這裡簡單處理：
                pygame.draw.line(temp_image, color, arm_pivot, (20 + swing * 0.8, 40), 2)
            else:
                 pygame.draw.line(temp_image, color, arm_pivot, (30, 40), 2)
                 pygame.draw.line(temp_image, color, arm_pivot, (10, 40), 2)

            # 顯示背在身上的裝備
            if self.has_sword:
                pygame.draw.line(temp_image, (200, 200, 200), (22, 35), (22, 50), 2)
            if self.has_shield:
                 pygame.draw.circle(temp_image, BLUE, (15, 35), 8, 1)

        # 根據方向翻轉圖像
        if not self.facing_right:
            temp_image = pygame.transform.flip(temp_image, True, False)
            
        self.image = temp_image

    def jump(self):
        # 只有在地面上時才能跳躍
        if self.on_ground:
            self.vel_y = PLAYER_JUMP
            self.on_ground = False
            if self.jump_sound:
                self.jump_sound.play()

    def attack(self):
        now = pygame.time.get_ticks()
        if self.has_sword and not self.is_attacking and now - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = True
            self.attack_time = now
            self.last_attack_time = now
            # 更新外觀
            self.update_image()

    def defend(self):
        if self.has_shield and not self.is_blocking:
            self.is_blocking = True
            self.block_time = pygame.time.get_ticks()
            self.update_image()

    def update(self):
        # 檢查攻擊狀態
        if self.is_attacking:
            if pygame.time.get_ticks() - self.attack_time > 200: # 攻擊持續 0.2 秒
                self.is_attacking = False
                # self.update_image() # 移到下方統一更新

        # 檢查防禦狀態
        if self.is_blocking:
            if pygame.time.get_ticks() - self.block_time > SHIELD_DURATION:
                self.is_blocking = False
                # self.update_image()

        self.acc_x = 0
        
        # 取得按鍵輸入
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT]:
            self.acc_x = -PLAYER_ACC
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT]:
            self.acc_x = PLAYER_ACC
            self.facing_right = True
            moving = True
            
        # 更新動畫計數器
        if moving and not self.is_attacking and not self.is_blocking:
            self.walk_count += 0.5 # 控制動畫速度
        else:
            # 停止時重置雙腳並攏 (或保持最後狀態，這裡選歸零讓它站好)
            if self.walk_count != 0 and int(self.walk_count) % 31 != 0: # 簡單的平滑歸零邏輯
                 self.walk_count = 0 
        
        # 每一禎都更新圖像以呈現動畫
        self.update_image()
        
        # 檢查無敵狀態 (必須在 update_image 之後執行，否則 alpha 會被重置)
        if self.invincible:
            if pygame.time.get_ticks() - self.invincible_start_time > self.invincible_duration:
                self.invincible = False
                self.image.set_alpha(255) # 恢復不透明
            else:
                # 閃爍效果
                # 改用 100ms 間隔，並且切換完全透明與不透明，視覺效果最強烈
                if (pygame.time.get_ticks() // 100) % 2 == 0:
                    self.image.set_alpha(0) # 完全透明 (消失)
                else:
                    self.image.set_alpha(255) # 正常顯示

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
