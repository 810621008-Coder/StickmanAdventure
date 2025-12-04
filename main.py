import pygame
import sys
from settings import *
from player import Player
from platforms import Platform
from items import Coin
from enemy import Enemy

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
        self.score = 0
        self.lives = PLAYER_LIVES

        # 建立精靈群組
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group() # 敵人群組
        
        # 建立地圖
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            
        # 建立金幣
        for c in COIN_LIST:
            coin = Coin(*c)
            self.all_sprites.add(coin)
            self.coins.add(coin)

        # 建立敵人
        for e in ENEMY_LIST:
            enemy = Enemy(*e)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
        
        # 建立玩家
        self.player = Player()
        self.all_sprites.add(self.player)

    def draw_text(self, text, size, color, x, y):

        # 繪製文字的輔助函式
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def run(self):

        # 遊戲主迴圈
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # 處理事件 (按鍵、關閉視窗等)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 偵測按鍵按下
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

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
                        self.player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        self.player.vel_y = 0
                        self.player.vel_x = 0
                    else:
                        self.running = False

        # 5. 掉落死亡偵測
        if self.player.rect.top > SCREEN_HEIGHT:
            self.lives -= 1
            print(f"Lives left: {self.lives}")
            if self.lives > 0:
                # 重生
                self.player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                self.player.vel_y = 0
                self.player.vel_x = 0
                # 簡單重置地圖位置 (為了簡化，這裡暫時不重置卷軸，可能會導致重生在空中，
                # 之後章節我們會做更完整的關卡重置)
            else:
                self.running = False # 遊戲結束

    def shift_world(self, shift_x):
        # 讓世界中的物體移動 (產生卷軸效果)
        for plat in self.platforms:
            plat.rect.x += shift_x
        for coin in self.coins:
            coin.rect.x += shift_x
        for enemy in self.enemies:
            enemy.rect.x += shift_x

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

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
