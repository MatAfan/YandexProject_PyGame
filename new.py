import random

import pygame

BLACK = 0
WHITE = 1


class Board:
    # создание поля
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.bombs = width * height // 20
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.start = False

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, 'White', (self.left + col * self.cell_size,
                                                   self.top + row * self.cell_size, self.cell_size,
                                                   self.cell_size), 1)
                if self.board[row][col] == 1:
                    pygame.draw.rect(screen, 'Red', (self.left + col * self.cell_size + 1,
                                                                         self.top + row * self.cell_size + 1,
                                                                         self.cell_size - 2, self.cell_size - 2), 0)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            if not self.start:
                self.start = True
                self.gen_bombs()
            self.on_click(cell)

    def get_cell(self, pos):
        if 0 <= pos[0] - self.left <= self.width * self.cell_size and 0 <= pos[1] - self.top <= self.height * self.cell_size:
            return (pos[0] - self.left) // self.cell_size, (pos[1] - self.top) // self.cell_size
        return None

    def on_click(self, cell):
        if not self.board[cell[1]][cell[0]]:
            neighbour_bombs = self.bombs()
            self.board[row][col] = (self.board[row][col] + 1) % 2

    def gen_bombs(self, cell):
        start_bombs = 0
        while start_bombs != self.bombs:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if x != cell[0] and y != cell[1] and not self.board[cell[0]][cell[1]]:
                self.board[x][y] = 1
                start_bombs += 1

        def bombs(self, cell):
            x, y = cell[0], cell[1]
            for xx in range(x - 1, x + 2):
                for yy in range(y - 1, y - 2):
                    if 0 < xx < self.width and 0 < yy < self.height:



# поле 5 на 7
board = Board(16, 16, 10, 10, 30)
size = width, height = 500, 500
running = True
screen = pygame.display.set_mode(size)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()