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
    def __init__(self, x, y, type, platforms=None, player=None):
        super().__init__()
        self.type = type
        self.platforms = platforms
        self.player = player
        
        if type == 'mini':
            width, height = BOSS_WIDTH, BOSS_HEIGHT
            color = ORANGE
            self.hp = 3
            self.shoot_delay = 2000
        elif type == 'big':
            width, height = BOSS_WIDTH * 1.5, BOSS_HEIGHT * 1.5
            color = DARK_RED
            self.hp = 5
            self.shoot_delay = 1500
        elif type == 'final':
            width, height = BOSS_WIDTH * 2, BOSS_HEIGHT * 2
            color = (100, 0, 100) # 深紫色
            self.hp = 8
            self.shoot_delay = 1000
        
        self.image = pygame.Surface((int(width), int(height)))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        
        self.speed = 2
        self.direction = -1 # 初始向左
        self.move_counter = 0
        self.last_shot = pygame.time.get_ticks()
        
        # 最終 Boss 特殊能力
        self.vel_y = 0
        self.on_ground = True
        self.is_dashing = False
        self.dash_timer = 0
        self.action_timer = pygame.time.get_ticks()
        self.state = 'IDLE' # IDLE, JUMP, DASH

    def update(self):
        # 重力
        self.vel_y += PLAYER_GRAVITY
        self.rect.y += self.vel_y
        
        # 平台碰撞 (Y軸)
        if self.platforms:
            hits = pygame.sprite.spritecollide(self, self.platforms, False)
            if hits:
                # 找出最低的平台 (rect.top 最小)
                if self.vel_y > 0:
                    lowest = hits[0]
                    if self.rect.bottom < lowest.rect.bottom + 10:
                        self.rect.bottom = lowest.rect.top
                        self.vel_y = 0
                        self.on_ground = True
        else:
            # 備用：如果沒有傳入 platforms，使用簡單地面判定
            if self.rect.bottom > SCREEN_HEIGHT - 40:
                self.rect.bottom = SCREEN_HEIGHT - 40
                self.vel_y = 0
                self.on_ground = True

        # 移動邏輯
        if self.type == 'mini':
            # 小 Boss: 簡單左右巡邏
            self.rect.x += self.speed * self.direction
            self.move_counter += 1
            if self.move_counter > 100:
                self.direction *= -1
                self.move_counter = 0
        elif self.type == 'big':
            # 大 Boss: 移動範圍更大，速度稍快
            self.rect.x += self.speed * self.direction * 1.5
            self.move_counter += 1
            if self.move_counter > 150:
                self.direction *= -1
                self.move_counter = 0
            
            # 跳躍邏輯 (隨機跳躍)
            if self.on_ground and random.randint(0, 100) < 2: # 2% 機率跳躍
                self.vel_y = -15
                self.on_ground = False
                
            # 空中也能發射子彈 (main.py 會呼叫 shoot)
            
        elif self.type == 'final':
            self.update_final_boss()

    def update_final_boss(self):
        now = pygame.time.get_ticks()
        
        # 距離檢查：如果玩家太遠，不進行 AI 運算 (保持原地)
        dist = abs(self.player.rect.centerx - self.rect.centerx) if self.player else 5000
        if dist > 1000:
            return
        
        # 面向玩家
        if self.player and not self.is_dashing:
            if self.player.rect.centerx < self.rect.centerx:
                self.direction = -1
            else:
                self.direction = 1

        if self.is_dashing:
            self.rect.x += BOSS_DASH_SPEED * self.direction
            if now - self.dash_timer > 300: # 衝刺 0.3 秒
                self.is_dashing = False
                self.state = 'IDLE'
                self.action_timer = now
            return

        # 隨機行動
        if now - self.action_timer > 2000: # 每 2 秒決定一次行動
            # 根據距離決定行動
            # dist 已經計算過了
            
            if dist < 200: # 近距離
                action = random.choice(['JUMP', 'DASH', 'DASH']) # 傾向衝刺
            else:
                action = random.choice(['JUMP', 'MOVE', 'MOVE']) # 傾向移動
                
            if action == 'JUMP' and self.on_ground:
                self.vel_y = BOSS_JUMP_POWER
                self.on_ground = False
                self.state = 'JUMP'
            elif action == 'DASH':
                self.is_dashing = True
                self.dash_timer = now
                self.state = 'DASH'
            
            self.action_timer = now

        # 隨機跳躍 (即使在移動中)
        if self.on_ground and not self.is_dashing and random.randint(0, 100) < 2:
             self.vel_y = BOSS_JUMP_POWER
             self.on_ground = False
             self.state = 'JUMP'

        # 一般移動 (允許空中移動，增加難度)
        if not self.is_dashing:
            # 檢查前方是否有地板，避免掉下去
            next_x = self.rect.centerx + (self.speed * self.direction * 30) # 預判前方
            
            on_platform = False
            if self.platforms:
                for plat in self.platforms:
                    # 檢查點是否在平台範圍內 (x 軸範圍內，且 y 軸在腳下附近)
                    if plat.rect.left <= next_x <= plat.rect.right and \
                       plat.rect.top <= self.rect.bottom + 50 <= plat.rect.bottom: # 寬鬆判定
                        on_platform = True
                        break
            
            # 如果在空中，或者前方有路，就移動
            if not self.on_ground or on_platform:
                self.rect.x += self.speed * self.direction

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # 發射子彈 (方向跟隨 Boss 面向)
            return Bullet(self.rect.centerx, self.rect.centery, self.direction)
        return None
