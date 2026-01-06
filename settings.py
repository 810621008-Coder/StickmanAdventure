# 遊戲設定檔
# 這裡存放所有的常數，方便調整遊戲參數

# 螢幕設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Stickman Adventure"

# 顏色定義 (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)      # 敵人顏色
GREEN = (0, 255, 0)    # 主角顏色
BLUE = (0, 0, 255)     # 其他物件
YELLOW = (255, 255, 0) # 金幣顏色
PURPLE = (128, 0, 128) # 傳送門顏色
CYAN = (0, 255, 255)   # 傳送門顏色 (更亮)
ORANGE = (255, 165, 0) # 小 Boss 顏色
DARK_RED = (139, 0, 0) # 大 Boss 顏色
PINK = (255, 192, 203) # 公主顏色
GRAY = (100, 100, 100) # 地板顏色
DARK_GREEN = (0, 100, 0) # 食人花顏色

# 玩家設定
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = GREEN
PLAYER_ACC = 0.5      # 加速度 (控制移動滑順度)
PLAYER_FRICTION = -0.12 # 摩擦力 (控制停下來的速度)
PLAYER_GRAVITY = 0.8  # 重力
PLAYER_JUMP = -16     # 跳躍力 (負值代表向上)
PLAYER_LIVES = 5      # 玩家初始生命
SWORD_DAMAGE = 1      # 劍攻擊力
SHIELD_DURATION = 500 # 盾牌防禦持續時間 (毫秒)

# Boss 設定
BOSS_WIDTH = 50
BOSS_HEIGHT = 80
BOSS_JUMP_POWER = -15 # Boss 跳躍力
BOSS_DASH_SPEED = 10  # Boss 衝刺速度
BULLET_SPEED = 5
BULLET_COLOR = RED

# 地圖設定
# 關卡 1 資料
LEVEL_1 = {
    'platforms': [
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),           # 起始地板
        (SCREEN_WIDTH + 100, SCREEN_HEIGHT - 40, 600, 40),   # 第二塊地板
        (300, SCREEN_HEIGHT - 150, 200, 20),
        (600, SCREEN_HEIGHT - 300, 200, 20),
        (900, SCREEN_HEIGHT - 450, 200, 20),
        (1200, SCREEN_HEIGHT - 200, 200, 20),
        (1600, SCREEN_HEIGHT - 150, 200, 20),                # 新增補間平台
        (2000, SCREEN_HEIGHT - 40, 500, 40),                 # 終點地板
    ],
    'coins': [
        (400, SCREEN_HEIGHT - 100),
        (750, SCREEN_HEIGHT - 350),
        (1000, SCREEN_HEIGHT - 500),
        (1300, SCREEN_HEIGHT - 250),
        (1650, SCREEN_HEIGHT - 200), # 第五個平台上的金幣
        (1100, SCREEN_HEIGHT - 80),   # 第一個下水道口
        (1020, SCREEN_HEIGHT - 320),  # 第一個食人花左上方 (挑戰跳躍)
        (850, SCREEN_HEIGHT - 100),   # 第一個坑口 (地板缺口處)
        (1400, SCREEN_HEIGHT - 120),  # 第二個食人花正上方 (貼近食人花頂端)
    ],
    'enemies': [
        (500, SCREEN_HEIGHT - 40, 100),
        (700, SCREEN_HEIGHT - 40, 150),
        (1300, SCREEN_HEIGHT - 240, 100),
        (1600, SCREEN_HEIGHT - 190, 100), # 第五個平台上的敵人
    ],
    'pop_up_enemies': [
        (1100, SCREEN_HEIGHT - 40, 0),   # 第一個食人花 (無延遲)
        (1400, SCREEN_HEIGHT - 40, 100), # 第二個食人花 (延遲 100 幀)
    ],
    # 'portal': (2400, SCREEN_HEIGHT - 90), # 移除原本的靜態傳送門
    'boss': {
        'type': 'mini',
        'x': 2200,
        'y': SCREEN_HEIGHT - 40,
        'hp': 3
    },
    'portal_spawn': (2400, SCREEN_HEIGHT - 90), # Boss 死後傳送門出現的位置
    'length': 2500 # 關卡長度 (到達此處算過關)
}

# 關卡 2 資料 (稍微難一點)
LEVEL_2 = {
    'platforms': [
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        (400, SCREEN_HEIGHT - 200, 200, 20),
        (700, SCREEN_HEIGHT - 350, 200, 20),
        (1000, SCREEN_HEIGHT - 500, 200, 20),
        (1300, SCREEN_HEIGHT - 300, 200, 20, 2, 0, 150), # 第四個平台左右移動 (速度2, 距離150)
        (1600, SCREEN_HEIGHT - 150, 200, 20),
        (2000, SCREEN_HEIGHT - 40, 800, 40), # Boss 戰場地
    ],
    'coins': [
        (450, SCREEN_HEIGHT - 250),
        (750, SCREEN_HEIGHT - 400),
        (1050, SCREEN_HEIGHT - 550),
        (1350, SCREEN_HEIGHT - 350),
        (1620, SCREEN_HEIGHT - 200), # 第五個漂浮平台左側上方
    ],
    'enemies': [
        (400, SCREEN_HEIGHT - 240, 100),
        (700, SCREEN_HEIGHT - 390, 100),
        (1000, SCREEN_HEIGHT - 540, 100),
        (1600, SCREEN_HEIGHT - 190, 100),
    ],
    'falling_enemies': True, # 啟用掉落敵人
    # 'portal': (2700, SCREEN_HEIGHT - 90), # 移除傳送門
    'boss': {
        'type': 'big',
        'x': 2400,
        'y': SCREEN_HEIGHT - 40,
        'hp': 5
    },
    'portal_spawn': (2700, SCREEN_HEIGHT - 90), # Boss 死後傳送門出現的位置
    'length': 2800
}

# 關卡 3 資料 (最終決戰)
LEVEL_3 = {
    'platforms': [
        (0, SCREEN_HEIGHT - 40, 1000, 40), # 加長起始地板
        (400, SCREEN_HEIGHT - 200, 200, 20),
        (700, SCREEN_HEIGHT - 320, 200, 20, 2, 0, 150), # 第二個漂浮平台左右移動
        (1075, SCREEN_HEIGHT - 400, 150, 20, 0, 2, 220), # 第三個漂浮平台變短且上下移動 (範圍加大，讓玩家能從下方跳上來)
        (1300, SCREEN_HEIGHT - 320, 200, 20, 2, 0, 150), # 第四個漂浮平台左右移動
        (1600, SCREEN_HEIGHT - 200, 200, 20),
        (1800, SCREEN_HEIGHT - 40, 1200, 40), # Boss 戰場地
        
        # 新增：第三平台下方的地面島
        (1050, SCREEN_HEIGHT - 40, 200, 40),

        # 秘密區域平台 (位於地下 y=1000 處)
        (0, 1000, 800, 40),
        (200, 900, 100, 20),
        (500, 900, 100, 20),
    ],
    'coins': [
        (450, SCREEN_HEIGHT - 250),
        (750, SCREEN_HEIGHT - 370),
        (1050, SCREEN_HEIGHT - 490),
        (1350, SCREEN_HEIGHT - 370),
        (1650, SCREEN_HEIGHT - 250),
        (720, SCREEN_HEIGHT - 380), # 第二個漂浮平台上方 (斜向排列 1)
        (760, SCREEN_HEIGHT - 420), # 第二個漂浮平台上方 (斜向排列 2)
        (800, SCREEN_HEIGHT - 460), # 第二個漂浮平台上方 (斜向排列 3)
        (1150, SCREEN_HEIGHT - 120), # 食人花頭頂上方
        (1220, SCREEN_HEIGHT - 80),  # 食人花右側
    ],
    'enemies': [
        (600, SCREEN_HEIGHT - 40, 150), # 將敵人移遠一點，避免開場被撞
        (1000, SCREEN_HEIGHT - 480, 100),
        (1600, SCREEN_HEIGHT - 240, 100),
        # 秘密區域守衛
        (200, 960, 100),
        (500, 960, 100),
    ],
    'pop_up_enemies': [
        (1150, SCREEN_HEIGHT - 40, 0, 200, 100), # 地面島上的食人花 (頻率較慢)
    ],
    'falling_enemies': True,
    'boss': {
        'type': 'final',
        'x': 2600,
        'y': SCREEN_HEIGHT - 40,
        'hp': 8
    },
    'princess_spawn': (2900, SCREEN_HEIGHT - 80),
    'length': 3000,
    
    # 特殊物件
    'pipe': (100, SCREEN_HEIGHT - 40 - 60), # 通往秘密區域的入口 (x, y)
    'secret_spawn': (50, 900), # 進入秘密區域後的重生點
    'pipe_exit': (750, 940), # 離開秘密區域的出口
    'exit_spawn': (200, SCREEN_HEIGHT - 40), # 離開後的重生點
    'items': [
        ('sword', 220, 850), # 劍的位置 (秘密區域)
        ('shield', 520, 850), # 盾的位置 (秘密區域)
    ]
}

# 所有關卡清單
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]
