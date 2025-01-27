import os
import sys
from random import choice
import pygame
import copy

FPS = 50

cell_width = cell_height = 120
dict_of_tiles = {'.': 'grass', '=': 'road', '#': 'railway', '~': 'river', 'x': 'border'}  # хз зачем
dict_of_sprites = {'bush': '*', 'stone': '+', 'log': '^', 'mini_bus': '№1^', 'police_car': '№2', 'fire_truck': '№3',
                   'train': '@@@'}
replacements = {'.': '..', '=': '==', '#': '##', '~': '~~', 'x': 'xx'}
coins_count = []
animation_frames_coin = 10


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
    for y, row in enumerate(level):
        row = row[0]
        if row == '.':
            g = Tile('grass', y)
            tiles_group.add(g)
            for x in (0, 1, 3, 4):
                sprite = g.generate_grass(x, y)
                if sprite != 'grass':
                    all_sprites.add(sprite)
                    level[y][x] = dict_of_sprites[sprite.sprite_type]
            # print(level)
            # print(all_sprites)
        elif row == '=':
            g = Tile('road', y)
            tiles_group.add(g)
            sprite = g.generate_road(0, y)
            all_sprites.add(sprite)
            level[y][0] = dict_of_sprites[sprite.sprite_type]
        elif row == '#':
            Tile('railway', y)
            g = Tile('railway', y)
            tiles_group.add(g)
            sprite = g.generate_railway(0, y)
            all_sprites.add(sprite)
            level[y][0] = dict_of_sprites[sprite.sprite_type]
        elif row == '~':
            g = Tile('river', y)
            tiles_group.add(g)
            random_x1 = choice([1, 2])
            random_x2 = choice([4, 3, 0])
            for x in (random_x1, random_x2):
                sprite = g.generate_river(x, y)
                if sprite != 'river':
                    all_sprites.add(sprite)
                    level[y][x] = dict_of_sprites[sprite.sprite_type]
        elif row == 'x':
            Tile('border', y)
        level[y] = [replacements.get(x, x) for x in level[y]]


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
        for i in range(4):
            s = choice(('.', '.', '.', '=', '=', '#', '~'))
            self.level.insert(0, [s for i in range(5)])

    def new_row(self):
        for i in range(11, 0, -1):
            self.level[i] = self.level[i - 1]
        new = choice(('.', '.', '.', '=', '=', '#', '~'))
        self.level[0] = [new for i in range(5)]

    def re_draw(self):
        for i in range(len(board.level)):
            if '~~' in board.level[i] or '==' in board.level[i] or '@@@' in board.level[i]:
                board.level[i] = [board.level[i][-1]] + board.level[i][:-1]





class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_y):
        super().__init__(tiles_group)
        self.pos_y = pos_y
        self.image = load_image(f"{tile_type}.jpg")
        self.image = pygame.transform.scale(self.image, (120 * 5, 120))
        self.rect = self.image.get_rect(left=0, top=self.pos_y * cell_height)

    def generate_grass(self, pos_x, pos_y):
        self.sprites = ['stone', 'bush', 'grass']
        sp = choice(self.sprites)
        if sp != 'grass':
            return Sprite(sp, pos_x, pos_y)
        return 'grass'

    def generate_road(self, pos_x, pos_y):
        self.sprites_cars = ['mini_bus', 'police_car', 'fire_truck']
        sp = choice(self.sprites_cars)
        return Sprite(sp, pos_x, pos_y)

    def generate_river(self, pos_x, pos_y):
        return Sprite('log', pos_x, pos_y)

    def generate_railway(self, pos_x, pos_y):
        return Sprite('train', pos_x, pos_y)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('coin_1.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(centerx=x + 19, top=y)
        self.frames = [load_image(f'coin_{i}.png') for i in range(1, 9)]
        self.frame_count = 0

    def animation(self):
        self.frame_count += 1
        if self.frame_count >= len(self.frames) * animation_frames_coin:
            self.frame_count = 0
        self.image = self.frames[self.frame_count // animation_frames_coin]
    # def coins_pos(self):
    #


class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.sprite_type = sprite_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = load_image(f"{sprite_type}.png")
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=pos_x * cell_width, top=self.pos_y * cell_height)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.on_log = False
        self.pos_x = 2
        self.pos_y = 5
        # self.frames = {'left': range(13, 17),
        #                'right': range(5, 9),
        #                'up': range(9, 13),
        #                'down': range(1, 5)}
        self.image = load_image("cat/9.png")
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=self.pos_x * cell_width, top=self.pos_y * cell_height)

    # def animation(self, condition):
    #     for i in self.frames[condition]:
    #         self.image = load_image(f'{i}.png')
    #     self.image = load_image("1.png")


all_moneys = pygame.sprite.Group()
count_money = 0
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
    pygame.display.set_caption('Выживание котенка')
    running = True
    render_level(board.level)
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:
                board.re_draw()
                for sprite in all_sprites:
                    if sprite.sprite_type in ('log','mini_bus', 'police_car', 'fire_truck','train'):
                        sprite.pos_x += 1
                        sprite.pos_x %= 5
                        sprite.rect.x = sprite.pos_x * cell_width
                if cat.on_log:
                    cat.pos_x += 1
                    cat.rect.x = cat.pos_x * cell_width
                    if cat.pos_x == 5:
                        print('уплыл')
                        running = False
                if board.level[5][cat.pos_x] in ('№1^', '№2', '№3', '@@@'):
                    print('лепешка')
                    running = False
                    # Нужно заменить на Gameover
                print(board.level)
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP
                    and board.level[cat.pos_y - 1][cat.pos_x] not in ('xx', '+', '*')):
                for obj in all_sprites:
                    obj.pos_y += 1
                    if obj.pos_y > 11:
                        all_sprites.remove(obj)
                        tiles_group.remove(obj)
                    obj.rect.y = obj.pos_y * cell_width
                for obj in tiles_group:
                    obj.pos_y += 1
                    if obj.pos_y > 11:
                        tiles_group.remove(obj)
                    obj.rect.y = obj.pos_y * cell_width
                if cat.pos_y == 5:
                    board.new_row()
                    render_level(board.level)
                else:
                    cat.pos_y -= 1
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and
                    board.level[cat.pos_y + 1][cat.pos_x] not in ('xx', '+', '*')):
                cat.pos_y += 1
                if cat.pos_y == 10:
                    print('орел унес')
                    running = False  # Нужно заменить на Gameover
                else:
                    for obj in all_sprites:
                        obj.pos_y -= 1
                        obj.rect.y = obj.pos_y * cell_width
                    for obj in tiles_group:
                        obj.pos_y -= 1
                        obj.rect.y = obj.pos_y * cell_width
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and
                    board.level[cat.pos_y][cat.pos_x - 1] not in ('xx', '+', '*')):
                if cat.pos_x > 0:
                    cat.pos_x -= 1
                    cat.rect.x -= cell_width
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and
                    board.level[cat.pos_y][cat.pos_x + 1] not in ('xx', '+', '*')):
                if cat.pos_x < 4:
                    cat.pos_x += 1
                    cat.rect.x += cell_width

            cell = board.level[cat.pos_y][cat.pos_x]
            if cell != '^':
                cat.on_log = False
            if cell == '^':
                cat.on_log = True
            if cell == '~~':
                print('утонул')
                running = False  # Нужно заменить на Gameover
            if cell in ('№1^', '№2', '№3', '@@@'):
                print('лепешка')
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
