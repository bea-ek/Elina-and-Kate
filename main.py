import os
import sys
from random import choice

import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    # создание поля
    def __init__(self):
        self.width = 5  # Кол-во клеток в ширину
        self.height = 7  # в высоту
        self.board = [Grass() for _ in range(self.height)]
        # Значения положения поля по умолчанию
        self.left = 0
        self.top = 0
        for i in range(4):
            cell = choice((Grass(), Grass(), Grass(), River(), Road(), Road(), Railway()))
            self.board[i] = cell

    # настройка положения поля
    def set_view(self, left, top):
        self.left = left
        self.top = top

    # отрисовка
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(self.board[y].image, (
                    x * 120 + self.left, y * 120 + self.top))
            if self.board[y].__class__ == Grass:
                for x in range(self.width):
                    screen.blit(self.board[y].row[x], (
                        x * 120 + self.left, y * 120 + self.top))


class Grass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("grass.jpg")
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.row = [choice((Tree().image, Stone().image, self.image, self.image)),
                    choice((Tree().image, Stone().image, self.image, self.image)), self.image,
                    choice((Tree().image, Stone().image, self.image, self.image)),
                    choice((Tree().image, Stone().image, self.image, self.image))]


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("tree.jpg")
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))



class Stone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("stone.jpg")
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (120, 120))


class River(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("river2.jpg")  # либо river.jpg
        self.image = pygame.transform.scale(self.image, (120, 120))


class Road(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("road.jpg")
        self.image = pygame.transform.scale(self.image, (120, 120))


class Railway(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("railway.jpg")
        self.image = pygame.transform.scale(self.image, (120, 120))


def main():
    pygame.init()
    size = 600, 840
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    board = Board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        board.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
