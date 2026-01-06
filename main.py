import pygame
import sys
from settings import *
from player import Player
from platforms import Platform
from items import Coin, Portal, Princess, Item, Pipe
from enemy import Enemy, FallingEnemy, PopUpEnemy
from boss import Boss, Bullet
import random

class Game:
    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font('arial') # 設定字型
        
        # 遊戲數值
        self.current_level_index = 0
        self.score = 0
        self.lives = PLAYER_LIVES
        self.jump_to_level = None # 用於指定跳轉的關卡索引

    def new(self):
        # 開始新關卡
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.falling_enemies = pygame.sprite.Group() # 獨立管理掉落敵人
        self.portals = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.princesses = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        
        self.end_game_items_spawned = False # 標記是否已經生成過關道具
        self.world_shift_x = 0 # 紀錄世界卷軸偏移量
        
        # 讀取當前關卡資料
        level_data = LEVELS[self.current_level_index]
        
        # 建立食人花 (先建立，這樣會畫在平台後面，看起來像從地底冒出來)
        self.pop_up_enemies = pygame.sprite.Group()
        if 'pop_up_enemies' in level_data:
            for pue in level_data['pop_up_enemies']:
                enemy = PopUpEnemy(*pue)
                self.all_sprites.add(enemy)
                self.pop_up_enemies.add(enemy)

        # 建立地圖
        for plat in level_data['platforms']:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            
        # 建立金幣
        for c in level_data['coins']:
            coin = Coin(*c)
            self.all_sprites.add(coin)
            self.coins.add(coin)

        # 建立敵人
        for e in level_data['enemies']:
            enemy = Enemy(*e)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        # 建立玩家 (先建立，以便傳給 Boss)
        self.player = Player()
        # 設定玩家初始位置 (避免出生在敵人堆裡或半空中)
        self.player.rect.centerx = 100
        self.player.rect.bottom = SCREEN_HEIGHT - 40 - 10
        self.all_sprites.add(self.player)

        # 建立 Boss
        if 'boss' in level_data:
            boss_data = level_data['boss']
            # 傳入 platforms 和 player 以便進行物理碰撞和追蹤
            boss = Boss(boss_data['x'], boss_data['y'], boss_data['type'], self.platforms, self.player)
            self.all_sprites.add(boss)
            self.bosses.add(boss)
        
        self.run()

    def draw_text(self, text, size, color, x, y):

        # 繪製文字的輔助函式
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        # 遊戲迴圈
        self.playing = True
        self.level_complete = False
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.playing:
                break
            self.update()
            self.draw()

    def events(self):
        # 處理事件 (按鍵、關閉視窗等)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            
            # 偵測按鍵按下
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_a:
                    self.player.attack()
                if event.key == pygame.K_s:
                    self.player.defend()
                
                # 指定跳關密技
                if event.key == pygame.K_F2:
                    print("Jump to Level 2 activated!")
                    self.jump_to_level = 1 # Level 2 index
                    self.playing = False
                if event.key == pygame.K_F3:
                    print("Jump to Level 3 activated!")
                    self.jump_to_level = 2 # Level 3 index
                    self.playing = False

                # 進入水管
                if event.key == pygame.K_DOWN:
                    self.check_pipe_entry()

    def check_pipe_entry(self):
        # 檢查是否站在水管上
        hits = pygame.sprite.spritecollide(self.player, self.pipes, False)
        if hits:
            level_data = LEVELS[self.current_level_index]
            if 'secret_spawn' in level_data:
                # 傳送到秘密區域
                spawn_x, spawn_y = level_data['secret_spawn']
                # 這裡需要注意：因為世界卷軸的關係，直接設定座標可能會錯位
                # 簡單作法：重置世界偏移，然後將玩家放到絕對座標
                # 但這樣會讓原本的地圖亂掉。
                # 更好的作法：計算相對位移。
                # 由於秘密區域是同一張地圖的一部分 (只是在很下面)，我們可以直接移動玩家
                self.player.rect.x = spawn_x
                self.player.rect.y = spawn_y
                # 為了讓鏡頭跟上，我們可能需要強制移動鏡頭
                # 但目前的 shift_world 是移動物體，不是移動鏡頭。
                # 所以如果我們把玩家瞬移到很遠的地方，鏡頭不會自動跟過去，
                # 而是玩家會跑出螢幕外。
                # 我們需要反向操作 shift_world 來「移動鏡頭」到玩家新位置。
                
                # 算出目標位置相對於螢幕中心的偏移
                target_screen_x = SCREEN_WIDTH // 2
                shift_needed = target_screen_x - self.player.rect.centerx
                self.shift_world(shift_needed)
                
                # 垂直方向我們沒有做卷軸，所以如果秘密區域在 y=1000，玩家會掉出螢幕。
                # 我們需要實作垂直卷軸，或者簡單地把秘密區域的所有物件往上移，
                # 把原本的物件暫時移走。
                # 這裡採用簡單作法：垂直瞬移所有物件
                shift_y = SCREEN_HEIGHT - 150 - self.player.rect.y # 讓玩家出現在螢幕下方
                for sprite in self.all_sprites:
                    sprite.rect.y += shift_y
                
                # 記錄這個垂直偏移，以便之後復原 (如果需要)
                # 但因為我們是單向進入，出來時會到另一個出口，所以直接設定出口位置即可。

    def update(self):
        # 更新所有物件狀態
        self.all_sprites.update()
        
        # 檢查是否掉出秘密區域 (回到主地圖)
        level_data = LEVELS[self.current_level_index]
        if 'pipe_exit' in level_data:
            # 如果玩家在秘密區域 (y 座標很大) 且走到了出口位置
            # 這裡簡化判定：如果玩家走到了出口 x 座標附近
            exit_x, exit_y = level_data['pipe_exit']
            # 注意：這裡的 exit_x 是絕對座標，需要考慮 world_shift
            # 但因為我們在秘密區域裡移動了 world_shift，所以座標系統是一致的
            
            # 簡單判定：如果玩家取得了劍和盾，就自動傳送回地面
            if self.player.has_sword and self.player.has_shield:
                 if 'exit_spawn' in level_data:
                    spawn_x, spawn_y = level_data['exit_spawn']
                    self.player.rect.x = spawn_x
                    self.player.rect.y = spawn_y
                    
                    # 調整水平鏡頭
                    target_screen_x = SCREEN_WIDTH // 3
                    shift_needed = target_screen_x - self.player.rect.centerx
                    self.shift_world(shift_needed)
                    
                    # 調整垂直位置 (把所有物件移回原位)
                    # 這比較麻煩，因為我們剛才亂動了 y 軸。
                    # 比較穩健的作法是重新載入關卡，但保留道具狀態。
                    # 這裡我們用一個簡單的 hack: 
                    # 假設秘密區域在 y=900~1000，地面在 y=500~600
                    # 我們剛才把 y=900 的東西移到了 y=500
                    # 現在要把 y=500 (原本的地面) 移回來
                    # 其實只要確保玩家回到地面時，地面的 y 座標是正確的即可。
                    # 我們重新對齊所有平台：
                    # 找到地面平台 (y 最接近 SCREEN_HEIGHT - 40 的)
                    # 算出它現在的 y 和目標 y 的差距，然後移動所有物件
                    
                    ground_plat = None
                    for p in self.platforms:
                        # 尋找原本的主地面 (寬度很大的那個)
                        if p.rect.width > 500 and p.rect.height == 40: 
                             ground_plat = p
                             break
                    
                    if ground_plat:
                        current_y = ground_plat.rect.y
                        target_y = SCREEN_HEIGHT - 40
                        diff_y = target_y - current_y
                        for sprite in self.all_sprites:
                            sprite.rect.y += diff_y

        # 1. 平台碰撞偵測
        # 只有在「往下掉」的時候才偵測碰撞，這樣才能從平台下方跳上去
        if self.player.vel_y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # 找出最高的平台 (rect.top 最小)
                lowest = min(hits, key=lambda p: p.rect.top)
                
                # 寬鬆判定：只要腳底沒有超過平台底部太多 (允許一點點穿透誤差)
                if self.player.rect.bottom < lowest.rect.bottom + 10: 
                    self.player.rect.bottom = lowest.rect.top
                    self.player.vel_y = 0
                    self.player.on_ground = True
                    
                    # 讓玩家跟隨平台移動
                    if hasattr(lowest, 'current_dx'):
                        self.player.rect.x += lowest.current_dx

        # 2. 鏡頭卷軸機制
        # 如果主角移動到螢幕右邊 1/3 處
        if self.player.rect.right >= SCREEN_WIDTH / 3 * 2:
            self.player.rect.right = SCREEN_WIDTH / 3 * 2
            scroll_speed = abs(self.player.vel_x)
            self.shift_world(-scroll_speed)
                
        # 如果主角移動到螢幕左邊 1/3 處 (往回走)
        if self.player.rect.left <= SCREEN_WIDTH / 3:
            self.player.rect.left = SCREEN_WIDTH / 3
            scroll_speed = abs(self.player.vel_x)
            self.shift_world(scroll_speed)

        # 3. 金幣碰撞偵測
        # True 代表碰撞後刪除金幣
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.score += 10 # 吃到金幣加 10 分
            print(f"Score: {self.score}")
        
        # 檢查是否滿足過關條件 (金幣全收集 + Boss 已死)
        if hits:
             self.try_spawn_exit()

        # 4. 敵人碰撞偵測 (戰鬥系統)
        # 這裡不使用 True，因為我們要先判斷是踩死還是被撞死
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            for enemy in hits:
                # 判斷是否為「踩頭」
                # 條件：主角正在往下掉，且主角底部在敵人中心點上方
                if self.player.vel_y > 0 and self.player.rect.bottom < enemy.rect.centery + 10:
                    enemy.kill() # 敵人死亡
                    self.player.vel_y = -12 # 主角彈起來
                    self.score += 50
                    print("Stomped enemy!")
                else:
                    # 如果無敵狀態，忽略傷害
                    if self.player.invincible:
                        continue

                    # 被撞死
                    self.lives -= 1
                    print(f"Ouch! Lives left: {self.lives}")
                    if self.lives > 0:
                        # 原地復活
                        self.respawn_player(pos=self.player.rect.center)
                    else:
                        self.playing = False
                        self.level_complete = False

        # 5. Boss 戰鬥系統
        # Boss 發射子彈
        for boss in self.bosses:
            bullet = boss.shoot()
            if bullet:
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)

        # 隨機生成掉落敵人 (限制數量)
        level_data = LEVELS[self.current_level_index]
        if level_data.get('falling_enemies', False):
            # 限制場上最多只有 2 隻掉落敵人
            if len(self.falling_enemies) < 2:
                if random.randrange(0, 200) < 1: # 0.5% 機率生成 (降低頻率)
                    enemy = FallingEnemy(self.platforms)
                    self.all_sprites.add(enemy)
                    self.falling_enemies.add(enemy)
                    # 注意：這裡不加入 self.enemies，因為 update 邏輯不同

        # 掉落敵人碰撞偵測 (與玩家)
        hits = pygame.sprite.spritecollide(self.player, self.falling_enemies, False)
        if hits:
            for enemy in hits:
                # 踩頭判定
                if self.player.vel_y > 0 and self.player.rect.bottom < enemy.rect.centery + 10:
                    enemy.kill()
                    self.player.vel_y = -12
                    self.score += 50
                else:
                    if self.player.invincible:
                        continue

                    self.lives -= 1
                    if self.lives > 0:
                        # 原地復活
                        self.respawn_player(pos=self.player.rect.center)
                    else:
                        self.playing = False
                        self.level_complete = False

        # 食人花碰撞偵測 (無法踩死)
        hits = pygame.sprite.spritecollide(self.player, self.pop_up_enemies, False)
        if hits:
            for enemy in hits:
                # 如果食人花完全縮下去 (HIDDEN)，就不會受傷
                if enemy.state == 'HIDDEN':
                    continue
                
                if self.player.invincible:
                    continue

                self.lives -= 1
                if self.lives > 0:
                    self.respawn_player(pos=self.player.rect.center)
                else:
                    self.playing = False
                    self.level_complete = False
                break # 只要撞到一個有效攻擊就處理

        # 道具碰撞偵測
        hits = pygame.sprite.spritecollide(self.player, self.items, True)
        for item in hits:
            if item.type == 'sword':
                self.player.has_sword = True
                print("Got Sword!")
            elif item.type == 'shield':
                self.player.has_shield = True
                print("Got Shield!")

        # 劍攻擊判定 (攻擊敵人)
        if self.player.is_attacking:
            # 建立一個臨時的攻擊判定框
            attack_rect = self.player.rect.copy()
            if self.player.vel_x >= 0: # 向右
                attack_rect.x += 40
            else: # 向左
                attack_rect.x -= 40
            
            # 攻擊敵人
            for enemy in self.enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.kill()
                    self.score += 50
            
            # 攻擊 Boss
            for boss in self.bosses:
                if attack_rect.colliderect(boss.rect):
                    boss.hp -= SWORD_DAMAGE
                    # 擊退 Boss
                    boss.rect.x += 50 if self.player.rect.centerx < boss.rect.centerx else -50
                    print(f"Boss HP: {boss.hp}")
                    if boss.hp <= 0:
                        boss.kill()
                        self.score += 1000
                        self.try_spawn_exit()

        # 子彈擊中玩家
        hits = pygame.sprite.spritecollide(self.player, self.bullets, True)
        if hits:
            # 如果正在防禦，且子彈從前方來
            blocked = False
            if self.player.is_blocking:
                # 簡單判定：只要防禦就擋住所有子彈
                blocked = True
            
            if not blocked and not self.player.invincible:
                self.lives -= 1
                if self.lives > 0:
                    self.respawn_player(pos=self.player.rect.center)
                else:
                    self.playing = False
                    self.level_complete = False

        # 玩家與 Boss 碰撞
        hits = pygame.sprite.spritecollide(self.player, self.bosses, False)
        if hits:
            for boss in hits:
                # 踩頭攻擊 Boss
                if self.player.vel_y > 0 and self.player.rect.bottom < boss.rect.centery + 20:
                    boss.hp -= 1
                    self.player.vel_y = -12 # 彈起
                    print(f"Boss HP: {boss.hp}")
                    if boss.hp <= 0:
                        boss.kill()
                        self.score += 500
                        self.try_spawn_exit()
                else:
                    # 檢查是否防禦衝撞
                    blocked = False
                    if self.player.is_blocking:
                        blocked = True
                        # 彈開玩家
                        self.player.vel_x = -10 if self.player.rect.centerx < boss.rect.centerx else 10
                    
                    if not blocked and not self.player.invincible:
                        # 被 Boss 撞傷
                        self.lives -= 1
                        if self.lives > 0:
                            self.respawn_player(pos=self.player.rect.center)
                        else:
                            self.playing = False
                            self.level_complete = False

        # 6. 掉落死亡偵測
        if self.player.rect.top > SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.respawn_player()
            else:
                self.playing = False
                self.level_complete = False

        # 6. 過關偵測 (碰到傳送門)
        hits = pygame.sprite.spritecollide(self.player, self.portals, False)
        if hits:
            self.playing = False
            self.level_complete = True

        # 7. 結局偵測 (碰到公主)
        hits = pygame.sprite.spritecollide(self.player, self.princesses, False)
        if hits:
            self.playing = False
            self.level_complete = True # 這裡會觸發 victory screen，因為已經是最後一關了

    def try_spawn_exit(self):
        # 檢查是否滿足過關條件：Boss 已死且金幣全收集
        # 注意：boss.kill() 會將 boss 從 self.bosses 移除，所以檢查 len(self.bosses) == 0 即可
        # 同理，金幣被吃掉後也會從 self.coins 移除
        if len(self.bosses) == 0 and len(self.coins) == 0 and not self.end_game_items_spawned:
            self.end_game_items_spawned = True
            self.spawn_end_game_items()

    def spawn_end_game_items(self):
        # 生成過關物件 (傳送門或公主)
        level_data = LEVELS[self.current_level_index]
        if 'portal_spawn' in level_data:
            spawn_x, spawn_y = level_data['portal_spawn']
            portal = Portal(spawn_x + self.world_shift_x, spawn_y)
            self.all_sprites.add(portal)
            self.portals.add(portal)
        if 'princess_spawn' in level_data:
            spawn_x, spawn_y = level_data['princess_spawn']
            princess = Princess(spawn_x + self.world_shift_x, spawn_y)
            self.all_sprites.add(princess)
            self.princesses.add(princess)

    def respawn_player(self, pos=None):
        # 啟動無敵狀態
        self.player.invincible = True
        self.player.invincible_start_time = pygame.time.get_ticks()

        # 如果有指定位置 (例如原地復活)，就直接使用
        if pos:
            self.player.rect.center = pos
            self.player.vel_y = 0
            self.player.vel_x = 0
            # 稍微往上提一點，避免卡在地板裡
            self.player.rect.y -= 10
            return

        # 尋找最近的安全平台 (包含螢幕外的)
        # 1. 找出所有靜止平台
        static_platforms = [p for p in self.platforms if getattr(p, 'move_x', 0) == 0 and getattr(p, 'move_y', 0) == 0]
        
        if not static_platforms:
            # 如果沒有靜止平台，就用所有平台
            static_platforms = list(self.platforms)

        # 2. 篩選出位於玩家左側（身後）的平台
        # 我們使用玩家當前的 x 座標來判斷
        current_x = self.player.rect.centerx
        behind_platforms = [p for p in static_platforms if p.rect.centerx < current_x]

        if behind_platforms:
            # 選擇最右邊的（離玩家最近的）
            target_plat = max(behind_platforms, key=lambda p: p.rect.centerx)
        else:
            # 如果左側沒有平台（例如剛開始就死掉），就選最左邊的平台
            target_plat = min(static_platforms, key=lambda p: p.rect.centerx)

        # 3. 調整鏡頭，確保重生平台在螢幕範圍內
        # 我們希望重生平台位於螢幕左側約 1/3 處，這樣玩家有視野往右走
        target_screen_x = SCREEN_WIDTH // 3
        shift_needed = target_screen_x - target_plat.rect.centerx
        
        # 移動世界
        self.shift_world(shift_needed)
        
        # 4. 將玩家放置在平台上方
        self.player.rect.centerx = target_plat.rect.centerx
        self.player.rect.bottom = target_plat.rect.top - 10
        self.player.vel_y = 0
        self.player.vel_x = 0

    def shift_world(self, shift_x):
        # 讓世界中的物體移動 (產生卷軸效果)
        self.world_shift_x += shift_x
        for plat in self.platforms:
            plat.rect.x += shift_x
        for coin in self.coins:
            coin.rect.x += shift_x
        for enemy in self.enemies:
            enemy.rect.x += shift_x
        for enemy in self.falling_enemies:
            enemy.rect.x += shift_x
        for enemy in self.pop_up_enemies:
            enemy.rect.x += shift_x
        for portal in self.portals:
            portal.rect.x += shift_x
        for boss in self.bosses:
            boss.rect.x += shift_x
        for bullet in self.bullets:
            bullet.rect.x += shift_x
        for princess in self.princesses:
            princess.rect.x += shift_x
        for item in self.items:
            item.rect.x += shift_x
        for pipe in self.pipes:
            pipe.rect.x += shift_x

    def draw(self):
        # 繪製畫面
        self.screen.fill(BLACK) # 背景填黑
        
        # 畫出所有精靈 (包含主角和平台)
        self.all_sprites.draw(self.screen)
        
        # 繪製 UI
        self.draw_text(f"Score: {self.score}", 22, WHITE, 10, 10)
        self.draw_text(f"Lives: {self.lives}", 22, WHITE, 10, 40)
        
        # 顯示裝備狀態
        if self.player.has_sword:
            self.draw_text("SWORD", 18, YELLOW, 10, 70)
        if self.player.has_shield:
            self.draw_text("SHIELD", 18, BLUE, 10, 90)
        
        # 更新顯示
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, RED, SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 4)
        self.draw_text(f"Score: {self.score}", 22, WHITE, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def show_victory_screen(self):
        if not self.running:
            return
            
        # 播放勝利音效
        try:
            victory_sound = pygame.mixer.Sound('victory.wav')
            victory_sound.play()
        except:
            pass
            
        self.screen.fill(BLACK)
        self.draw_text("PRINCESS SAVED!", 48, PINK, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 4)
        self.draw_text("YOU WIN!", 32, YELLOW, SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 50)
        self.draw_text(f"Final Score: {self.score}", 22, WHITE, SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

if __name__ == "__main__":
    game = Game()
    game.show_start_screen()
    while game.running:
        pygame.event.clear() # 清除殘留的事件，避免按鍵連點導致連續跳關
        game.new()

        # 檢查是否有指定跳關
        if game.jump_to_level is not None:
            game.current_level_index = game.jump_to_level
            game.jump_to_level = None
            # 確保索引不超出範圍
            if game.current_level_index >= len(LEVELS):
                game.current_level_index = 0
            continue

        if game.level_complete:
            game.current_level_index += 1
            # 稍微延遲一下，避免連續跳關
            pygame.time.delay(200)
            if game.current_level_index >= len(LEVELS):
                game.show_victory_screen()
                game.current_level_index = 0
                game.score = 0
                game.lives = PLAYER_LIVES
                game.show_start_screen()
        else:
            game.show_go_screen()
            game.current_level_index = 0
            game.score = 0
            game.lives = PLAYER_LIVES
            game.show_start_screen()
            
    pygame.quit()
    sys.exit()
