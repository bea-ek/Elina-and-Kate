import os
import sys
from random import choice

import pygame

FPS = 50

cell_width = cell_height = 120

level = ['.', '.', 'x', 'x', 'x', 'x', 'x', 'x']
for i in range(9):
    level.insert(0, choice(('.', '.', '.', '=', '=', '#', '~')))


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


def new_row():
    for i in range(17):
        level[i - 1] = level[i]
    level[16] = choice(('.', '.', '.', '=', '=', '#', '~'))


def generate_level():
    for y, row in enumerate(level[5:-5]):
        if row == '.':
            Tile('grass', y)
        elif row == '_':
            Tile('border', y)
        elif row == '=':
            Tile('road', y)
        elif row == '#':
            Tile('railway', y)
        elif row == '~':
            Tile('river', y)
        elif row == 'x':
            Tile('border', y)
    # return Player(2, 10)


# class Board:
#     # создание поля
#     def __init__(self):
#         self.width = 5  # Кол-во клеток в ширину
#         self.height = 7  # в высоту
#         self.board = [Grass() for _ in range(self.height)]
#         # Значения положения поля по умолчанию
#         self.left = 0
#         self.top = 0
#         for i in range(4):
#             cell = choice((Grass(), Grass(), Grass(), River(), Road(), Road(), Railway()))
#             self.board[i] = cell
#
#     # настройка положения поля
#     def set_view(self, left, top):
#         self.left = left
#         self.top = top
#
#     # отрисовка
#     def render(self, screen):
#         for y in range(self.height):
#             for x in range(self.width):
#                 screen.blit(self.board[y].image, (
#                     x * 120 + self.left, y * 120 + self.top))
#             if self.board[y].__class__ == Grass:
#                 for x in range(self.width):
#                     screen.blit(self.board[y].row[x], (
#                         x * 120 + self.left, y * 120 + self.top))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(f"{tile_type}.jpg")
        self.image = pygame.transform.scale(self.image, (120 * 5, 120))
        self.rect = self.image.get_rect().move(
            0, cell_height * pos_y)
        if tile_type == 'grass':
            for cell in range(5):
                if cell != 2:
                    if self.f(cell, pos_y):
                        all_sprites.append(self.f(cell, pos_y))

    def f(self, cell, pos_y):
        self.sprites = [Bush(100, 100).image, Stone(200, 100).image, None]
        self.rand_sprites = choice(self.sprites).get_rect().move(
            cell * 120, cell_height * pos_y)
        return self.rand_sprites


class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image("bush.png")
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=x, top=y)


class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image("stone.jpg")
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(left=x, top=120)


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


# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__(player_group, all_sprites)
#         self.rect = self.image.get_rect(left=x, top=y)

class Log(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("log.png")
        self.image = pygame.transform.scale(self.image, (120, 120))


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


def main():
    pygame.init()
    size = 600, 840
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        generate_level()
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start_screen()
