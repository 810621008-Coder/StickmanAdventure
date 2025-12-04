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
GRAY = (100, 100, 100) # 地板顏色

# 玩家設定
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = GREEN
PLAYER_ACC = 0.5      # 加速度 (控制移動滑順度)
PLAYER_FRICTION = -0.12 # 摩擦力 (控制停下來的速度)
PLAYER_GRAVITY = 0.8  # 重力
PLAYER_JUMP = -16     # 跳躍力 (負值代表向上)
PLAYER_LIVES = 3      # 玩家初始生命

# 地圖設定
# 格式: (x, y, width, height)
PLATFORM_LIST = [
    (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),           # 起始地板
    (SCREEN_WIDTH + 100, SCREEN_HEIGHT - 40, 600, 40),   # 第二塊地板 (有間隙)
    (300, SCREEN_HEIGHT - 150, 200, 20),                 # 懸空平台 1
    (600, SCREEN_HEIGHT - 300, 200, 20),                 # 懸空平台 2
    (900, SCREEN_HEIGHT - 450, 200, 20),                 # 懸空平台 3
    (1200, SCREEN_HEIGHT - 200, 200, 20),                # 懸空平台 4
]

# 金幣位置清單 (x, y)
COIN_LIST = [
    (400, SCREEN_HEIGHT - 100),
    (750, SCREEN_HEIGHT - 350),
    (1000, SCREEN_HEIGHT - 500),
    (1300, SCREEN_HEIGHT - 250),
]

# 敵人設定 (x, y, 巡邏距離)
ENEMY_LIST = [
    (500, SCREEN_HEIGHT - 40, 100),      # 地面上的敵人
    (700, SCREEN_HEIGHT - 40, 150),      # 地面上的敵人 2
    (1300, SCREEN_HEIGHT - 240, 100),    # 平台上的敵人
]
