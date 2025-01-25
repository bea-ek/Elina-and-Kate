import os
import sys
from random import choice
import pygame
import copy

FPS = 50

cell_width = cell_height = 120
dict_of_tiles = {'.': 'grass', '=': 'road', '#': 'railway', '~': 'river', 'x': 'border'}  # хз зачем
dict_of_sprites = {'bush': '*', 'stone': '+', 'log': '^'}
replacements = {'.': '..'}
sp_sprites_move=[]

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Crazy Road)))")
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('rules.jpg'), (600, 840))
    screen.blit(fon, (0, 0))
    screen.blit(pygame.transform.scale(load_image('cat_rules.jpg'), (180, 180)), (300, 200))
    # screen.blit(pygame.transform.scale(load_image('start.jpg'), (300, 180)), (100, 400))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return main()
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def render_level(level):
    for y, row in enumerate(level[5:12]):
        row = row[0]
        if row == '.':
            g = Tile('grass', y)
            tiles_group.add(g)
            for x in (0, 1, 3, 4):
                sprite = g.generate_grass(x, y)
                if sprite != 'grass':
                    all_sprites.add(sprite)
                    level[y + 5][x] = dict_of_sprites[sprite.sprite_type]
            level[y + 5] = [replacements.get(x, x) for x in level[y + 5]]
            print(level)
            print(all_sprites)
        elif row == '=':
            g = Tile('road', y)
            tiles_group.add(g)
        elif row == '#':
            Tile('railway', y)
        elif row == '~':
            g = Tile('river', y)
            tiles_group.add(g)
            random_x1 = choice([1, 2])
            random_x2 = choice([4, 3, 0])
            for x in (random_x1, random_x2):
                sprite = g.generate_river(x, y)
                if sprite != 'river':
                    all_sprites.add(sprite)
                    level[y + 5][x] = dict_of_sprites[sprite.sprite_type]
            level[y + 5] = [replacements.get(x, x) for x in level[y + 5]]

        elif row == 'x':
            Tile('border', y)
    # return Player(2, 10)
# def spr_update(x,g):
#     speed=10
#     while True:
#         pygame.time.delay(30)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#         x += speed
#         screen.blit(g, (x, y))
#         pygame.display.update()
class Board:
    # создание поля
    def __init__(self):
        self.level = [['.' for i in range(5)] for j in range(2)] + [['x' for i2 in range(5)] for j2 in range(6)]
        for i in range(9):
            s = choice(('.', '.', '.', '=', '=', '#', '~'))
            self.level.insert(0, [s for i in range(5)])
    def new_row(self):
        for i in range(17):
            self.level[i - 1] = self.level[i]
        self.level[16] = choice(('.', '.', '.', '=', '=', '#', '~'))
    def re_draw(self):
        for i in range(len(board.level)):
            if '~' in board.level[i]:
                board.level[i] = [board.level[i][-1]] + board.level[i][:-1]
            if '~' in board.level[i]:
                g = Tile('river', i)
                tiles_group.add(g)
                for j in range(len(board.level[i])):
                    if board.level[j] == '^':
                        sprite = g.generate_river(i, j)
                        if sprite != 'river':
                            all_sprites.add(sprite)
                            level[y + 5][x] = dict_of_sprites[sprite.sprite_type]





class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(f"{tile_type}.jpg")
        self.image = pygame.transform.scale(self.image, (120 * 5, 120))
        self.rect = self.image.get_rect(left=0, top=pos_y * cell_height)
    def generate_grass(self, pos_x, pos_y):
        self.sprites = ['stone', 'bush', 'grass']
        sp = choice(self.sprites)
        if sp != 'grass':
            return Sprite(sp, pos_x, pos_y)
        return 'grass'

    def generate_river(self, pos_x, pos_y):
        return Sprite('log', pos_x, pos_y)


# class Log(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = load_image("log.png")
#         self.image = pygame.transform.scale(self.image, (120, 120))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.sprite_type = sprite_type
        self.image = load_image(f"{sprite_type}.png")
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=pos_x * cell_width, top=pos_y * cell_height)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.pos_x = 2
        self.pos_y = 5
        self.image = load_image(f"9.jpg")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=self.pos_x * cell_width, top=self.pos_y * cell_height)


class Mini_Bus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("mini_bus.png")
        self.image = pygame.transform.scale(self.image, (120, 120))


class Police_Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("police_car.png")
        self.image = pygame.transform.scale(self.image, (120, 120))


class Fire_truck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("fire_truck.png")
        self.image = pygame.transform.scale(self.image, (240, 120))


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
board = Board()
cat = Player()
player_group.add(cat)


def main():
    pygame.init()
    size = 600, 840
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    running = True
    k=0
    render_level(board.level)

    while running:
        k+=1
        # print(k)
        if k>1000:
            board.re_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()

    # print(board.level)
    pygame.quit()


if __name__ == '__main__':
    start_screen()
# class Bush(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__(all_sprites)
#         self.image = load_image("bush.png")
#         self.image.set_colorkey((0, 0, 0))
#         self.image = pygame.transform.scale(self.image, (120, 120))
#         self.rect = self.image.get_rect().move(x * cell_width, y * cell_height)
#
#
# class Stone(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__(all_sprites)
#         self.image = load_image("stone.png")
#         self.image.set_colorkey((0, 0, 0))
#         self.image = pygame.transform.scale(self.image, (120, 120))
#         self.rect = self.image.get_rect(left=x, top=120)


# class River(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = load_image("river2.jpg")  # либо river.jpg
#         self.image = pygame.transform.scale(self.image, (120, 120))
#
#
# class Road(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = load_image("road.jpg")
#         self.image = pygame.transform.scale(self.image, (120, 120))
#
#
# class Railway(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = load_image("railway.jpg")
#         self.image = pygame.transform.scale(self.image, (120, 120))
# class Grass(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = load_image("grass.jpg")
#         self.image = pygame.transform.scale(self.image, (120, 120))
#         self.row = [choice((Bush().image, Stone().image, self.image, self.image)),
#                     choice((Bush().image, Stone().image, self.image, self.image)), self.image,
#                     choice((Bush().image, Stone().image, self.image, self.image)),
#                     choice((Bush().image, Stone().image, self.image, self.image))]
