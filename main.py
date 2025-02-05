import os
import sys
from random import choice
import pygame
from pygame import *

pygame.init()

FPS = 50

cell_width = cell_height = 120
dict_of_tiles = {'.': 'grass', '=': 'road', '#': 'railway', '~': 'river', 'x': 'border'}  # хз зачем
dict_of_sprites = {'coin': '0', 'bush': '*', 'stone': '+', 'log': '^', 'mini_bus': '№1', 'police_car': '№2',
                   'fire_truck': '№3',
                   'train': '@@@'}
replacements = {'.': '..', '=': '==', '#': '##', '~': '~~', 'x': 'xx'}
coins = []
animation_frames_coin = 10
count_money = 0
pygame.init()
pygame.mixer.init()


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
    # pygame.mixer.Channel(0).play(sound_start, loops=-1)
    pygame.mixer.music.load('data/start_sound.mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mixer.music.get_busy():  # Проверяем, играет ли музыка
                    pygame.mixer.music.stop()
                return main()

        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    pygame.display.set_caption("GAME OVEEER!")
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('game_over.jpg'), (750, 750))
    screen.blit(fon, (0, 0))
    pygame.mixer.music.load('data/start_sound.mp3')
    pygame.mixer.music.play(-1)
    font = pygame.font.Font(None, 32)
    text = ''
    rect = pygame.Rect(210, 550, 300, 40)
    active = False
    PINK = (255, 189, 228)
    ACTIVE_PINK = (255, 71, 182)
    while True:
        current_color = ACTIVE_PINK if active else PINK
        # Рендерим текст ввода
        pygame.draw.rect(screen, 'white', (210, 550, 300, 40))
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (rect.x + 5, rect.y + 5))  # Смещаем текст на 5 пикселей
        pygame.draw.rect(screen, current_color, rect, 2)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]  # Удаление символа
                    elif event.key == pygame.K_RETURN:
                        print("ник:", text)  # Обработка нажатия Enter
                        text = ''
                    else:
                        text += event.unicode
                elif not active:
                    if pygame.mixer.music.get_busy():  # Проверяем, играет ли музыка
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/start_sound.mp3')
                        pygame.mixer.music.play(-1)
                        global all_sprites, tiles_group, player_group, board, cat
                        all_sprites = pygame.sprite.Group()
                        tiles_group = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        board = Board()
                        cat = Player()
                        player_group.add(cat)
                        main()


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
            random_x = choice([0, 1, 2, 3, 4])
            sprite = g.generate_road(random_x, y)
            all_sprites.add(sprite)
            level[y][random_x] = dict_of_sprites[sprite.sprite_type]
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
            new = self.choice_new_row(self.level[0])
            self.level.insert(0, [new for i in range(5)])

    def new_row(self):
        new = self.choice_new_row(self.level[0])
        for i in range(11, 0, -1):
            self.level[i] = self.level[i - 1]
        self.level[0] = [new for i in range(5)]

    def re_draw(self):
        for i in range(len(board.level)):
            if '~~' in board.level[i] or '==' in board.level[i] or '@@@' in board.level[i]:
                board.level[i] = [board.level[i][-1]] + board.level[i][:-1]
            # if '~~' in board.level[i] and '~~' in board.level[i+1] or '~~' in board.level[i] and '~~' in board.level[i-1]:
            #     board.level[i] = [board.level[i][0]] + board.level[i][0:]
            # for el_ind in range(len(board.level[i])):
            #     if el == '^' or el == '..' or el == '==' or el == '##':

    # def coin_pos(self):
    #     for i in range(len(board.level)):
    #         for j in range(5):
    #             if board.level[i][j] == '^' or board.level[i][j] == '..' or board.level[i][j] == '==' or board.level[i][
    #                 j] == '##':
    #                 spr = choice(['coin', 'empty', 'empty'])
    #                 if spr == 'coin':
    #                     all_moneys.add((j, i))
    #                 pass

    def choice_new_row(self, row):
        if '..' in row or '.' in row:
            return choice(('.', '=', '=', '#', '~'))
        elif '=' in row or '~' in row or '#' in row or '==' in row or '~~' in row or '##' in row:
            return '.'


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_y):
        super().__init__(tiles_group)
        self.pos_y = pos_y
        self.image = load_image(f"{tile_type}.jpg")
        self.image = pygame.transform.scale(self.image, (120 * 5, 120))
        self.rect = self.image.get_rect(left=0, top=self.pos_y * cell_height)

    def generate_grass(self, pos_x, pos_y):
        self.sprites = ['stone', 'bush', 'grass', 'grass', 'grass', 'coin']
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


# class Coin(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = load_image('coin_1.png')
#         self.frames = [load_image(f'coin_{i}.png') for i in range(1, 9)]
#         self.image = pygame.transform.scale(self.image, (120, 120))
#         # self.rect = self.image.get_rect(left=x*cell_width, top=y * cell_height)
#         self.rect = self.image.get_rect(left=1 * cell_width, top=1 * cell_height)
#         self.frame = 0  # текущий кадр
#         self.last_update = pygame.time.get_ticks()
#         self.frame_rate = 50  # как быстро кадры меняются
#
#     def animation_coins(self):
#         self.frame += 1
#         if self.frame >= len(self.frames) * animation_frames_coin:
#             self.frame = 0
#         self.image = self.frames[self.frame // animation_frames_coin]
#
#     def generate_coins(self):
#         self.sprites_cars = ['coin', 'empty', 'empty']
#         sp = choice(self.sprites_cars)
#         return sp
#
#     def hide(self):  # исчезание монет при контакте с игроком
#         global count_money
#         count_money += 1
#         all_moneys.remove(self)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.sprite_type = sprite_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        if sprite_type == 'coin':
            self.frame = 0
            self.image = load_image('coin_1.png')
            self.frames = [load_image(f'coin_{i}.png') for i in range(1, 9)]
            self.image = pygame.transform.scale(self.image, (70, 70))
            self.rect = self.image.get_rect(left=self.pos_x * cell_width + 25, top=self.pos_y * cell_height + 25)
        else:
            self.image = load_image(f"{sprite_type}.png")
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.scale(self.image, (120, 120))
            self.rect = self.image.get_rect(left=self.pos_x * cell_width, top=self.pos_y * cell_height)

    def animation_coin(self):
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.image = self.frames[self.frame]
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(left=self.pos_x * cell_width + 25, top=self.pos_y * cell_height + 25)


class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.anim = [load_image(f'eagle\{i}.png') for i in range(1, 4)]  # загрузка твоих картинок для анимации
        self.image = self.anim[0]
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=2 * cell_width - 12, top=0 * cell_height)
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame == len(self.anim):
            self.frame = 0
        self.image = self.anim[self.frame]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.count_money = 0
        self.on_log = False
        self.pos_x = 2
        self.pos_y = 5
        self.dead = False
        self.frames = {'left': [pygame.transform.scale(load_image(f"cat/{i}.png"), (120, 120)) for i in range(13, 17)],
                       'right': [pygame.transform.scale(load_image(f"cat/{i}.png"), (120, 120)) for i in range(5, 9)],
                       'up': [pygame.transform.scale(load_image(f"cat/{i}.png"), (120, 120)) for i in range(9, 13)],
                       'down': [pygame.transform.scale(load_image(f"cat/{i}.png"), (120, 120)) for i in range(1, 5)]}
        self.image = load_image("cat/9.png")
        self.frame = 0
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=self.pos_x * cell_width, top=self.pos_y * cell_height)

    def animation(self, condition):
        self.frame += 1
        if self.frame == len(self.frames[condition]):
            self.image = load_image("cat/9.png")
            self.frame = 0
            pass
        self.image = self.frames[condition][self.frame]

    # def animation(self, condition):
    #     for i in self.frames[condition]:
    #         self.image = load_image(f'{i}.png')
    #     self.image = load_image("1.png")


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
    MYEVENTTYPE1 = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE1, 1000)
    MYEVENTTYPE2 = pygame.USEREVENT + 2
    pygame.time.set_timer(MYEVENTTYPE2, 0)
    pygame.mixer.music.load('data/main_sound.mp3')
    pygame.mixer.music.play(1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE2:
                if eagle.rect.y > 4 * cell_height:
                    cat.rect.y += 0.5 * cell_height
                eagle.rect.y += 0.5 * cell_height
                eagle.update()
                if cat.rect.y > 7 * cell_height:
                    game_over()
            if event.type == MYEVENTTYPE1:
                board.re_draw()
                for sprite in all_sprites:
                    if sprite.sprite_type in ('log', 'mini_bus', 'police_car', 'fire_truck', 'train'):
                        sprite.pos_x += 1
                        sprite.pos_x %= 5
                        sprite.rect.x = sprite.pos_x * cell_width
                    if sprite.sprite_type == 'coin':
                        sprite.animation_coin()
                if cat.on_log:
                    cat.pos_x += 1
                    cat.rect.x = cat.pos_x * cell_width
                    if cat.pos_x == 5:
                        print('уплыл')
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load('data/water_sound.mp3')
                            pygame.mixer.music.play(1)
                        game_over()
                if board.level[5][cat.pos_x] in ('№1', '№2', '№3', '@@@'):
                    print('лепешка')
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/die_sound.mp3')
                        pygame.mixer.music.play(1)

                    # Нужно заменить на Gameover
                print(board.level)
            if not cat.dead:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP
                        and board.level[cat.pos_y - 1][cat.pos_x] not in ('xx', '+', '*')):
                    for obj in all_sprites:
                        obj.pos_y += 1
                        if obj.pos_y > 11:
                            all_sprites.remove(obj)
                            tiles_group.remove(obj)
                        obj.rect.y = obj.pos_y * cell_width
                        if obj.sprite_type == 'coin':
                            obj.rect.y += 25
                            if (obj.pos_x, obj.pos_y) == (cat.pos_x, 5):
                                obj.kill()
                                cat.count_money += 1
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
                    cat.animation('up')
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and
                        board.level[cat.pos_y + 1][cat.pos_x] not in ('xx', '+', '*')):
                    cat.pos_y += 1
                    if cat.pos_y == 10:
                        eagle = Eagle()
                        player_group.add(eagle)
                        MYEVENTTYPE2 = pygame.USEREVENT + 2
                        pygame.time.set_timer(MYEVENTTYPE2, 120)
                        print('орел унес')
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load('data/eagle_sound.mp3')
                            pygame.mixer.music.play(1)
                    else:
                        for obj in all_sprites:
                            obj.pos_y -= 1
                            obj.rect.y = obj.pos_y * cell_width
                            if obj.sprite_type == 'coin':
                                obj.rect.y += 25
                                if (obj.pos_x, obj.pos_y) == (cat.pos_x, 5):
                                    obj.kill()
                                    cat.count_money += 1
                        for obj in tiles_group:
                            obj.pos_y -= 1
                            obj.rect.y = obj.pos_y * cell_width
                    cat.animation('down')
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and
                        board.level[cat.pos_y][cat.pos_x - 1] not in ('xx', '+', '*')):
                    if cat.pos_x > 0:
                        cat.pos_x -= 1
                        cat.rect.x -= cell_width
                    cat.animation('left')
                    for obj in all_sprites:
                        if obj.sprite_type == 'coin' and (obj.pos_x, obj.pos_y) == (cat.pos_x, 5):
                            obj.kill()
                            cat.count_money += 1
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and
                        board.level[cat.pos_y][cat.pos_x + 1] not in ('xx', '+', '*')):
                    if cat.pos_x < 4:
                        cat.pos_x += 1
                        cat.rect.x += cell_width
                    cat.animation('right')
                    for obj in all_sprites:
                        if obj.sprite_type == 'coin' and (obj.pos_x, obj.pos_y) == (cat.pos_x, 5):
                            obj.kill()
                            cat.count_money += 1
                cell = board.level[cat.pos_y][cat.pos_x]
                if cell != '^':
                    cat.on_log = False
                if cell == '^':
                    cat.on_log = True
                if cell == '~~':
                    cat.dead = True
                    print('утонул')
                    # Проверяем, играет ли музыка
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/water_sound.mp3')
                        pygame.mixer.music.play(1)

                        # Нужно добавить Gameover
                if cell in ('№1', '№2', '№3', '@@@'):
                    cat.dead = True
                    print('лепешка')
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/die_sound.mp3')
                        pygame.mixer.music.play(1)
            else:
                pygame.time.wait(1000)
                game_over()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
    # print(board.level)
    pygame.quit()


if __name__ == '__main__':
    start_screen()
