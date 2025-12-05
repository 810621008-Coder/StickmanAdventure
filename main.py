import pygame
import sys
from settings import *
from player import Player
from platforms import Platform
from items import Coin, Portal, Princess
from enemy import Enemy, FallingEnemy
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
        
        self.world_shift_x = 0 # 紀錄世界卷軸偏移量
        
        # 讀取當前關卡資料
        level_data = LEVELS[self.current_level_index]
        
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

        # 建立 Boss
        if 'boss' in level_data:
            boss_data = level_data['boss']
            boss = Boss(boss_data['x'], boss_data['y'], boss_data['type'])
            self.all_sprites.add(boss)
            self.bosses.add(boss)

        # 建立傳送門 (如果有靜態設定的話，但現在我們改用動態生成)
        if 'portal' in level_data:
            portal = Portal(*level_data['portal'])
            self.all_sprites.add(portal)
            self.portals.add(portal)
        
        # 建立玩家
        self.player = Player()
        self.all_sprites.add(self.player)
        
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
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                # 跳關密技
                if event.key == pygame.K_F1:
                    self.level_complete = True
                    self.playing = False

    def update(self):
        # 更新所有物件狀態
        self.all_sprites.update()
        
        # 1. 平台碰撞偵測
        # 只有在「往下掉」的時候才偵測碰撞，這樣才能從平台下方跳上去
        if self.player.vel_y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # 確保是踩在平台上方，而不是撞到側面
                lowest = hits[0]
                if self.player.rect.bottom < lowest.rect.bottom: 
                    self.player.rect.bottom = lowest.rect.top
                    self.player.vel_y = 0
                    self.player.on_ground = True

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
                    # 被撞死
                    self.lives -= 1
                    print(f"Ouch! Lives left: {self.lives}")
                    if self.lives > 0:
                        self.respawn_player()
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
                    self.lives -= 1
                    if self.lives > 0:
                        self.respawn_player()
                    else:
                        self.playing = False
                        self.level_complete = False

        # 子彈擊中玩家
        hits = pygame.sprite.spritecollide(self.player, self.bullets, True)
        if hits:
            self.lives -= 1
            if self.lives > 0:
                self.respawn_player()
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
                        # Boss 死亡後的事件
                        level_data = LEVELS[self.current_level_index]
                        if 'portal_spawn' in level_data:
                            # 修正：生成位置需要加上目前的世界偏移量
                            spawn_x, spawn_y = level_data['portal_spawn']
                            portal = Portal(spawn_x + self.world_shift_x, spawn_y)
                            self.all_sprites.add(portal)
                            self.portals.add(portal)
                        if 'princess_spawn' in level_data:
                            spawn_x, spawn_y = level_data['princess_spawn']
                            princess = Princess(spawn_x + self.world_shift_x, spawn_y)
                            self.all_sprites.add(princess)
                            self.princesses.add(princess)
                else:
                    # 被 Boss 撞傷
                    self.lives -= 1
                    if self.lives > 0:
                        self.respawn_player()
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

    def respawn_player(self):
        # 尋找最近的安全平台
        # 1. 找出所有在螢幕內的平台
        safe_platforms = []
        for plat in self.platforms:
            if 0 < plat.rect.centerx < SCREEN_WIDTH:
                safe_platforms.append(plat)
        
        if safe_platforms:
            # 2. 找到離玩家最近的平台 (或是最左邊的，比較安全)
            # 這裡簡單選擇最左邊的平台，避免重生在怪堆裡
            target_plat = min(safe_platforms, key=lambda p: p.rect.x)
            self.player.rect.centerx = target_plat.rect.centerx
            self.player.rect.bottom = target_plat.rect.top - 10
        else:
            # 如果沒有平台，就回到螢幕中間 (備案)
            self.player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            
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
        for portal in self.portals:
            portal.rect.x += shift_x
        for boss in self.bosses:
            boss.rect.x += shift_x
        for bullet in self.bullets:
            bullet.rect.x += shift_x
        for princess in self.princesses:
            princess.rect.x += shift_x

    def draw(self):
        # 繪製畫面
        self.screen.fill(BLACK) # 背景填黑
        
        # 畫出所有精靈 (包含主角和平台)
        self.all_sprites.draw(self.screen)
        
        # 繪製 UI
        self.draw_text(f"Score: {self.score}", 22, WHITE, 10, 10)
        self.draw_text(f"Lives: {self.lives}", 22, WHITE, 10, 40)
        
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
        self.screen.fill(BLACK)
        self.draw_text("YOU WIN!", 48, YELLOW, SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 4)
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
        game.new()
        if game.level_complete:
            game.current_level_index += 1
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
