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
        # 地面：整齊水平排列
        (150, SCREEN_HEIGHT - 100), (200, SCREEN_HEIGHT - 100), (250, SCREEN_HEIGHT - 100),
        
        # 第一個平台 (x=300)：簡單排列 (改為4枚)
        (330, SCREEN_HEIGHT - 200), (370, SCREEN_HEIGHT - 200), (410, SCREEN_HEIGHT - 200), (450, SCREEN_HEIGHT - 200),
        
        # 第二個平台 (x=600)：三角形排列
        (700, SCREEN_HEIGHT - 350), (680, SCREEN_HEIGHT - 380), (720, SCREEN_HEIGHT - 380),
        
        # 第三個平台 (x=900) & 問號磚：垂直挑戰 (左移)
        (920, SCREEN_HEIGHT - 500), (960, SCREEN_HEIGHT - 500), # 在問號磚下方
        (1150, SCREEN_HEIGHT - 560), # 懸空挑戰金幣 (維持不變)
        
        # 第四個平台 (x=1200)：拱形排列
        (1220, SCREEN_HEIGHT - 250), (1260, SCREEN_HEIGHT - 280), (1300, SCREEN_HEIGHT - 250),
        
        # 第五個平台 (x=1600)：水平接續 (改為3枚)
        (1630, SCREEN_HEIGHT - 200), (1670, SCREEN_HEIGHT - 200), (1710, SCREEN_HEIGHT - 200),

        # 下水道口與食人花周遭
        (1100, SCREEN_HEIGHT - 80), 
        (1020, SCREEN_HEIGHT - 320),
        (1400, SCREEN_HEIGHT - 120),
        
        # Boss 地面引導
        (2050, SCREEN_HEIGHT - 100), (2100, SCREEN_HEIGHT - 100),
        
        # Boss 地面尾端
        (2400, SCREEN_HEIGHT - 100), (2450, SCREEN_HEIGHT - 100),
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
    'length': 2500, # 關卡長度 (到達此處算過關)
    'question_blocks': [
        (1000, 50) # 第一關第四個平台上方
    ]
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
        # 起始區：斜上3枚金幣
        (200, SCREEN_HEIGHT - 100), (240, SCREEN_HEIGHT - 140), (280, SCREEN_HEIGHT - 180),
        
        # 第一個平台 (x=400)：金字塔排列 (6枚)
        (420, SCREEN_HEIGHT - 250), (460, SCREEN_HEIGHT - 250), (500, SCREEN_HEIGHT - 250), # 底層
        (440, SCREEN_HEIGHT - 290), (480, SCREEN_HEIGHT - 290),                             # 中層
        (460, SCREEN_HEIGHT - 330),                                                         # 頂層
        
        # 第二個平台 (x=700)：水平排列
        (750, SCREEN_HEIGHT - 400), (800, SCREEN_HEIGHT - 400),
        
        # 第三個平台 (x=1000)：菱形排列
        (1050, SCREEN_HEIGHT - 550), # 下
        (1080, SCREEN_HEIGHT - 580), # 左
        (1110, SCREEN_HEIGHT - 550), # 上
        (1080, SCREEN_HEIGHT - 520), # 右
        
        # 移動平台路徑上 (x=1300區域)：靜態懸浮金幣
        (1350, SCREEN_HEIGHT - 350), (1400, SCREEN_HEIGHT - 350), (1450, SCREEN_HEIGHT - 350),
        
        # 第五個平台 (x=1600)：階梯排列
        (1650, SCREEN_HEIGHT - 220), (1680, SCREEN_HEIGHT - 250), (1710, SCREEN_HEIGHT - 280),
        
        # Boss 地面：前後端雙拱 + 中間菱形
        # 前端拱形
        (2050, SCREEN_HEIGHT - 100), (2090, SCREEN_HEIGHT - 130), (2130, SCREEN_HEIGHT - 130), (2170, SCREEN_HEIGHT - 100),
        
        # 中間問號磚上方 (x=2400)：菱形排列 8 枚 (略寬)
        # 上半部
        (2400, SCREEN_HEIGHT - 380), # 最高點
        (2360, SCREEN_HEIGHT - 340), (2440, SCREEN_HEIGHT - 340), # 上中層
        (2320, SCREEN_HEIGHT - 300), (2480, SCREEN_HEIGHT - 300), # 中間最寬層
        # 下半部
        (2360, SCREEN_HEIGHT - 260), (2440, SCREEN_HEIGHT - 260), # 下中層
        (2400, SCREEN_HEIGHT - 220), # 最低點 (接近問號磚)

        # 尾端拱形
        (2630, SCREEN_HEIGHT - 100), (2670, SCREEN_HEIGHT - 130), (2710, SCREEN_HEIGHT - 130), (2750, SCREEN_HEIGHT - 100),
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
    'length': 2800,
    'question_blocks': [
        (1500, 150), # 第二關第四個平台(移動)最右邊上方
        (2380, SCREEN_HEIGHT - 170) # Boss 戰場中央 (高度約 430，離地 170，容易跳上，已修正置中)
    ]
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
        # 地面起始區 (整齊排列)
        (200, SCREEN_HEIGHT - 100), (240, SCREEN_HEIGHT - 100), (280, SCREEN_HEIGHT - 100), 
        (320, SCREEN_HEIGHT - 100), (360, SCREEN_HEIGHT - 100),
        
        # 第二個平台 (x=400) 上方：三角形排列
        (500, SCREEN_HEIGHT - 250),           # 頂
        (460, SCREEN_HEIGHT - 220), (540, SCREEN_HEIGHT - 220), # 底層

        # 第三個平台 (x=700) 上方：拱形排列
        (720, SCREEN_HEIGHT - 400), (760, SCREEN_HEIGHT - 430), (800, SCREEN_HEIGHT - 440),
        (840, SCREEN_HEIGHT - 430), (880, SCREEN_HEIGHT - 400),

        # 第四個平台 (x=1075) 上方：垂直排列 (稍往左移，懸空增加難度)
        (1060, SCREEN_HEIGHT - 450), (1060, SCREEN_HEIGHT - 490), (1060, SCREEN_HEIGHT - 530),

        # 第五個平台 (x=1300) 上方：水平排列
        (1350, SCREEN_HEIGHT - 370), (1390, SCREEN_HEIGHT - 370), (1430, SCREEN_HEIGHT - 370),

        # 第六個平台 (x=1600) 上方：矩形排列
        (1650, SCREEN_HEIGHT - 250), (1690, SCREEN_HEIGHT - 250),
        (1650, SCREEN_HEIGHT - 290), (1690, SCREEN_HEIGHT - 290),
        
        # 往 Boss 地面的跳躍引導
        (1750, SCREEN_HEIGHT - 150), (1800, SCREEN_HEIGHT - 100),

        # 食人花周圍
        (1150, SCREEN_HEIGHT - 120), (1220, SCREEN_HEIGHT - 80),

        # Boss 戰場問號磚 (x=2150) 上方的「巨大瑪利歐無敵星」 (放大版)
        # 1. 頂部尖端 (Top) - y=180 (極限跳躍高度)
        (2170, 180),
        
        # 2. 頭部 (Head)
        (2140, 210), (2170, 210), (2200, 210),
        (2110, 240), (2140, 240), (2170, 240), (2200, 240), (2230, 240),

        # 3. 手臂 (Arms) - 最寬處 y=270
        (2020, 270), (2050, 270), (2080, 270), (2110, 270), (2140, 270), (2170, 270), (2200, 270), (2230, 270), (2260, 270), (2290, 270), (2320, 270),

        # 4. 臉部 (Face) - 挖空眼睛位置 y=300
        (2050, 300), (2080, 300), (2110, 300),               # 左臉 (跳過 2140)
        (2170, 300),                                         # 鼻子 (跳過 2200)
        (2230, 300), (2260, 300), (2290, 300),               # 右臉

        # 5. 身體/腰部 (Waist) y=330
        (2080, 330), (2110, 330), (2140, 330), (2170, 330), (2200, 330), (2230, 330), (2260, 330),

        # 6. 腿部 (Legs) y=360
        (2050, 360), (2080, 360), (2110, 360),               # 左腿
        (2230, 360), (2260, 360), (2290, 360),               # 右腿
        
        # 7. 腳尖 (Feet) y=390 (接近問號磚)
        (2020, 390), (2050, 390),                            # 左腳尖
        (2290, 390), (2320, 390),                            # 右腳尖
    ],
    'enemies': [
        (600, SCREEN_HEIGHT - 40, 150),
        (500, SCREEN_HEIGHT - 240, 100), # 新增：駐守在第二個平台 (x=400) 的一般敵人
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
    ],
    'question_blocks': [
        (1150, 100), # 第三關第三個平台上方 (稍微右移)
        (2150, 410)  # Boss 戰場地上方 (輔助跳台，已調整位置以便跳上)
    ]
}

# 所有關卡清單
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]
