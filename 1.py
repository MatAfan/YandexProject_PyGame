import pygame
from random import randint as r

COLOURS = ['Yellow', 'Magenta']


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.board = [[r(0, 1) for l in range(width)] for k in range(height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.turn = 0

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
                if self.board[row][col] == 0:
                    pygame.draw.circle(screen, COLOURS[0], (self.left + col * self.cell_size
                                                            + self.cell_size // 2,
                                                            self.top + row * self.cell_size
                                                            + self.cell_size // 2),
                                                            self.cell_size // 2 - 3)
                elif self.board[row][col] == 1:
                    pygame.draw.circle(screen, COLOURS[1], (self.left + col * self.cell_size
                                                            + self.cell_size // 2,
                                                            self.top + row * self.cell_size
                                                            + self.cell_size // 2),
                                                            self.cell_size // 2 - 3)



    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, pos):
        if 0 <= pos[0] - self.left <= self.width * self.cell_size and \
                0 <= pos[1] - self.top <= self.height * self.cell_size:

            return (pos[0] - self.left) // self.cell_size, (pos[1] - self.top) // self.cell_size
        return None

    def on_click(self, cell):
        if cell:
            row, col = cell[0], cell[1]
            for x in range(len(self.board)):
                self.board[x][row] = (self.board[x][row] + 1) % 2
            for y in range(len(self.board[col])):
                self.board[col][y] = (self.board[col][y] + 1) % 2
            self.board[col][row] = (self.board[col][row] + 1) % 2
            self.turn = (self.turn + 1) % 2


size = width, height = 500, 500
board = Board(16, 16, 10, 10, 32)

running = True
screen = pygame.display.set_mode(size)

screen.fill((0, 0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

    board.render(screen)
    pygame.display.flip()