#сделал Андреянов Семён 27.12

window_size = width, height = 480, 480
fps = 20
maps_dir = 'maps'
tile_size = 32
event_enemy_type = 30


class Labyrinth:

    def __init__(self, filename, free_tiles, finish_tile):
        self.map = []
        with open(f'{maps_dir}/{filename}') as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.title_size = tile_size
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile
        self.last = ()

    def render(self, screen):
        color = {0: (0, 0, 0), 1: (248, 0, 120), 2: (0, 248, 0)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.title_size, y * self.title_size,
                                   self.title_size, self.title_size)
                screen.fill(color[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target):
        inf = 1000
        x, y = start
        distance = [[inf] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and self.is_free((next_x, next_y)) and  distance[next_y][next_x] == inf:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))

        x, y = target
        if distance[y][x] == inf or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y

    def find_random_way(self, start):
        x, y = start
        next_position = []
        for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
            next_x, next_y = x + dx, y + dy
            if self.is_free((next_x, next_y)):
                next_position.append((next_x, next_y))
        if self.last in next_position and len(next_position) > 1:
            next_position.remove(self.last)
        self.last = start
        return (random.choice(next_position))


class Hero:
    def __init__(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center_pos_hero = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
        pygame.draw.circle(screen, (255, 255, 255), center_pos_hero, tile_size // 2)


class Enemy:
    def __init__(self, position):
        self.x, self.y = position
        self.delay = 100
        pygame.time.set_timer(event_enemy_type, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center_pos_hero = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
        pygame.draw.circle(screen, (255, 0, 0), center_pos_hero, tile_size // 2)

class Enemy_Random:
    def __init__(self, position):
        self.x, self.y = position
        self.delay = 100
        pygame.time.set_timer(event_enemy_type, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center_pos_hero = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
        pygame.draw.circle(screen, (0, 0, 255), center_pos_hero, tile_size // 2)


class Game:
    def __init__(self, labyrinth, hero, enemy, enemy_random):
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemy = enemy
        self.enemy_random = enemy_random

    def render(self, screen):
        self.labyrinth.render(screen)
        self.hero.render(screen)
        self.enemy.render(screen)
        self.enemy_random.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.labyrinth.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def move_enemy(self):
        next_position = self.labyrinth.find_path_step(self.enemy.get_position(), self.hero.get_position())
        self.enemy.set_position(next_position)

    def move_random_enemy(self):
        next_position = self.labyrinth.find_random_way(self.enemy_random.get_position())
        self.enemy_random.set_position(next_position)


def main():
    pygame.init()
    screen = pygame.display.set_mode(window_size)

    labyrinth = Labyrinth('simple_map.txt', [0, 2], 2)
    hero = Hero((7, 7))
    enemy = Enemy((7, 1))
    enemy_random = Enemy_Random((1, 1))
    game = Game(labyrinth, hero, enemy, enemy_random)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == event_enemy_type:
                game.move_enemy()
                game.move_random_enemy()
        game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
