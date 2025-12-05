# 遊戲設定檔
# 這裡存放所有的常數，方便調整遊戲參數

# 螢幕設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "火柴人冒險 (Stickman Adventure)"

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

# 玩家設定
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = GREEN
PLAYER_ACC = 0.5      # 加速度 (控制移動滑順度)
PLAYER_FRICTION = -0.12 # 摩擦力 (控制停下來的速度)
PLAYER_GRAVITY = 0.8  # 重力
PLAYER_JUMP = -16     # 跳躍力 (負值代表向上)
PLAYER_LIVES = 5      # 玩家初始生命

# Boss 設定
BOSS_WIDTH = 50
BOSS_HEIGHT = 80
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
    ],
    'enemies': [
        (500, SCREEN_HEIGHT - 40, 100),
        (700, SCREEN_HEIGHT - 40, 150),
        (1300, SCREEN_HEIGHT - 240, 100),
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
        (1300, SCREEN_HEIGHT - 300, 200, 20),
        (1600, SCREEN_HEIGHT - 150, 200, 20),
        (2000, SCREEN_HEIGHT - 40, 800, 40), # Boss 戰場地
    ],
    'coins': [
        (450, SCREEN_HEIGHT - 250),
        (750, SCREEN_HEIGHT - 400),
        (1050, SCREEN_HEIGHT - 550),
        (1350, SCREEN_HEIGHT - 350),
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
    'princess_spawn': (2700, SCREEN_HEIGHT - 90), # Boss 死後公主出現的位置
    'length': 2800
}

# 所有關卡清單
LEVELS = [LEVEL_1, LEVEL_2]
