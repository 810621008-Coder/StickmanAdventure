import pygame
import random
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        # 加長 Surface 以容納火焰尾巴
        self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED * direction
        self.direction = direction
        self.anim_frame = 0

    def update(self):
        self.rect.x += self.speed
        
        # 動態火焰動畫
        self.anim_frame += 1
        self.image.fill((0, 0, 0, 0)) # 清空
        
        # 根據方向決定繪製位置
        # 如果向右 (speed > 0)，火球在右邊，尾巴在左邊
        if self.direction > 0:
            head_center = (30, 10)
            tail_direction = -1
        else:
            head_center = (10, 10)
            tail_direction = 1
            
        # 繪製火焰尾巴 (隨機閃爍長短)
        tail_length = random.randint(10, 25)
        tail_points = []
        tail_points.append(head_center) # 起點
        tail_points.append((head_center[0] + tail_length * tail_direction, 5)) # 上尾
        tail_points.append((head_center[0] + (tail_length+5) * tail_direction, 10)) # 中尖
        tail_points.append((head_center[0] + tail_length * tail_direction, 15)) # 下尾
        
        pygame.draw.polygon(self.image, (255, 100, 0), tail_points) # 橘色底
        
        # 內部亮黃色尾巴 (較短)
        inner_tail_length = tail_length - 5
        inner_points = []
        inner_points.append(head_center)
        inner_points.append((head_center[0] + inner_tail_length * tail_direction, 8))
        inner_points.append((head_center[0] + (inner_tail_length+3) * tail_direction, 10))
        inner_points.append((head_center[0] + inner_tail_length * tail_direction, 12))
        
        pygame.draw.polygon(self.image, (255, 255, 100), inner_points)

        # 火球本體
        pygame.draw.circle(self.image, (255, 80, 0), head_center, 10) # 深橘核心
        pygame.draw.circle(self.image, (255, 255, 0), head_center, 6) # 黃色中心
        
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
        
        self.image = pygame.Surface((int(width), int(height)), pygame.SRCALPHA)
        # 繪製 Boss 火柴人
        w, h = int(width), int(height)
        cx = w // 2
        line_width = 4 if self.type == 'mini' else 6
        
        # 頭部
        head_radius = w // 5
        head_cy = head_radius + 5
        pygame.draw.circle(self.image, color, (cx, head_cy), head_radius, line_width)
        
        # 身體
        body_start_y = head_cy + head_radius
        body_end_y = h - h // 3
        pygame.draw.line(self.image, color, (cx, body_start_y), (cx, body_end_y), line_width)
        
        # 手臂 (張牙舞爪)
        pygame.draw.line(self.image, color, (cx, body_start_y + 10), (10, body_start_y - 10), line_width)
        pygame.draw.line(self.image, color, (cx, body_start_y + 10), (w - 10, body_start_y - 10), line_width)
        
        # 腿部
        pygame.draw.line(self.image, color, (cx, body_end_y), (cx - w // 3, h), line_width)
        pygame.draw.line(self.image, color, (cx, body_end_y), (cx + w // 3, h), line_width)
        
        # 憤怒的臉
        eye_y = head_cy - 2
        eye_offset = head_radius // 2
        # 眼睛
        pygame.draw.circle(self.image, WHITE, (cx - eye_offset, eye_y), line_width)
        pygame.draw.circle(self.image, WHITE, (cx + eye_offset, eye_y), line_width)
        # 怒眉
        pygame.draw.line(self.image, BLACK, (cx - eye_offset - 5, eye_y - 5), (cx - eye_offset + 2, eye_y), 2)
        pygame.draw.line(self.image, BLACK, (cx + eye_offset + 5, eye_y - 5), (cx + eye_offset - 2, eye_y), 2)

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
        self.is_shooting = False # 用於顯示發射動作
        self.shoot_anim_timer = 0
        self.state = 'IDLE' # IDLE, JUMP, DASH

    def update(self):
        # 重力
        self.vel_y += PLAYER_GRAVITY
        self.rect.y += self.vel_y
        
        # 處理發射動畫計時
        if self.is_shooting:
             if pygame.time.get_ticks() - self.shoot_anim_timer > 300: # 發射動作維持 0.3 秒
                 self.is_shooting = False
                 self.update_image()
        
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
            
            # 邊緣偵測 (防止掉落)
            # 檢查前方地板
            next_x = self.rect.centerx + (self.speed * self.direction * 20) # 預判前方
            safe_to_move = False
            if self.platforms:
                for plat in self.platforms:
                     # 檢查前方是否仍有地板 (且同一高度)
                     if plat.rect.left <= next_x <= plat.rect.right and \
                        plat.rect.top >= self.rect.bottom - 5:
                         safe_to_move = True
                         break
            
            if safe_to_move:
                self.rect.x += self.speed * self.direction
                self.move_counter += 1
                if self.move_counter > 100:
                    self.direction *= -1
                    self.move_counter = 0
            else:
                self.direction *= -1 # 前方無路，立即回頭
                self.move_counter = 0
                
        elif self.type == 'big':
            # 大 Boss: 移動範圍更大，速度稍快
            
            # 邊緣偵測 (防止掉落)
            next_x = self.rect.centerx + (self.speed * self.direction * 30) # 預判更遠一點因為速度快
            safe_to_move = False
            if self.platforms:
                for plat in self.platforms:
                     if plat.rect.left <= next_x <= plat.rect.right and \
                        plat.rect.top >= self.rect.bottom - 5:
                         safe_to_move = True
                         break
            
            if safe_to_move:
                self.rect.x += self.speed * self.direction * 1.5
                self.move_counter += 1
                if self.move_counter > 150:
                    self.direction *= -1
                    self.move_counter = 0
            else:
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
        
        # 跡離檢查：如果玩家太遠，不進行 AI 運算 (保持原地)
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
            else:
                # 前方無路，轉向
                self.direction *= -1

    def shoot(self):
        if self.type in ['mini', 'big']:
             # 追蹤玩家 (如果夠近)
            dist_x = self.player.rect.centerx - self.rect.centerx
            if abs(dist_x) < 500: # 視野範圍
                if dist_x > 0:
                     self.direction = 1
                else:
                     self.direction = -1
            
            # 定時射擊
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.is_shooting = True # 觸發發射動作
                self.shoot_anim_timer = now
                self.update_image()
                return Bullet(self.rect.centerx, self.rect.centery, self.direction)
        return None

    def update_image(self):
        # 繪製 Boss 火柴人
        w, h = self.image.get_width(), self.image.get_height()
        cx = w // 2
        line_width = 4 if self.type == 'mini' else 6
        color = ORANGE
        if self.type == 'big': color = DARK_RED
        elif self.type == 'final': color = (100, 0, 100)
        
        self.image.fill((0, 0, 0, 0)) # 清空
        
        # 頭部
        head_radius = w // 5
        head_cy = head_radius + 5
        pygame.draw.circle(self.image, color, (cx, head_cy), head_radius, line_width)
        
        # 身體
        body_start_y = head_cy + head_radius
        body_end_y = h - h // 3
        pygame.draw.line(self.image, color, (cx, body_start_y), (cx, body_end_y), line_width)
        
        # 手臂
        if self.is_shooting:
            # 發射動作：手平舉指向玩家方向
            arm_y = body_start_y + 10
            if self.direction > 0: # 向右
                 pygame.draw.line(self.image, color, (cx, arm_y), (w - 5, arm_y), line_width) # 右手平舉
                 pygame.draw.line(self.image, color, (cx, arm_y), (10, arm_y + 20), line_width) # 左手放鬆
            else: # 向左
                 pygame.draw.line(self.image, color, (cx, arm_y), (5, arm_y), line_width) # 左手平舉
                 pygame.draw.line(self.image, color, (cx, arm_y), (w - 10, arm_y + 20), line_width) # 右手放鬆
        else:
            # 一般 (張牙舞爪)
            pygame.draw.line(self.image, color, (cx, body_start_y + 10), (10, body_start_y - 10), line_width)
            pygame.draw.line(self.image, color, (cx, body_start_y + 10), (w - 10, body_start_y - 10), line_width)
        
        # 腿部
        pygame.draw.line(self.image, color, (cx, body_end_y), (cx - w // 3, h), line_width)
        pygame.draw.line(self.image, color, (cx, body_end_y), (cx + w // 3, h), line_width)
        
        # 憤怒的臉
        eye_y = head_cy - 2
        eye_offset = head_radius // 2
        # 眼睛
        pygame.draw.circle(self.image, WHITE, (cx - eye_offset, eye_y), line_width)
        pygame.draw.circle(self.image, WHITE, (cx + eye_offset, eye_y), line_width)
        # 怒眉
        pygame.draw.line(self.image, BLACK, (cx - eye_offset - 5, eye_y - 5), (cx - eye_offset + 2, eye_y), 2)
        pygame.draw.line(self.image, BLACK, (cx + eye_offset + 5, eye_y - 5), (cx + eye_offset - 2, eye_y), 2)
