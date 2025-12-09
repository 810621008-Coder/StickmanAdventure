import pygame
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 80)) # 加高一點
        self.image.fill(CYAN) # 改成亮青色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 20 # 稍微往上提一點，確保不會埋在地板裡

class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 20

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((30, 30))
        if type == 'sword':
            self.image.fill((200, 200, 200)) # 銀色
        elif type == 'shield':
            self.image.fill((0, 0, 200)) # 藍色
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 60))
        self.image.fill((0, 150, 0)) # 綠色水管
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
