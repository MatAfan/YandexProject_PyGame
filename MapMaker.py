import pygame

BLACK = 0
WHITE = 1
COLOURS = ['White', 'Black']
MAPS_DIR = "maps"
filename = 'testmap.txt'


class Board:
    # создание поля
    def __init__(self, width, height, left, top, cell_size, start_colour):
        self.width = width
        self.height = height
        self.board = [[start_colour] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size

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
                pygame.draw.rect(screen, COLOURS[self.board[row][col]], (self.left + col * self.cell_size + 1,
                                                                         self.top + row * self.cell_size + 1,
                                                                         self.cell_size - 2, self.cell_size - 2), 0)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, pos):
        if 0 <= pos[0] - self.left <= self.width * self.cell_size and 0 <= pos[1] - self.top <= self.height * self.cell_size:
            return (pos[0] - self.left) // self.cell_size, (pos[1] - self.top) // self.cell_size
        return None

    def on_click(self, cell):
        if cell:
            col, row = cell[0], cell[1]
            self.board[row][col] = (self.board[row][col] + 1) % len(COLOURS)


# поле 5 на 7
board = Board(15, 15, 10, 10, 30, 1)
size = width, height = 470, 470
running = True
screen = pygame.display.set_mode(size)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_file = open(f'{MAPS_DIR}/{filename}', 'w')
            for x in board.board:
                total = ''
                for y in x:
                    total += str(y) + ' '
                print(total[:-1], file=save_file)
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()