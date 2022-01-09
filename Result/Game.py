from imports import *


class Labyrinth:
    def __init__(self, filename, free_tile, finish_tile):
        self.map = []
        with open(f"{MAPS_DIR}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tile
        self.finish_tile = finish_tile

    def render(self, screen):
        tiles = {0: load_image("Wall.png"), 1: load_image("Field.png"), 2: load_image("Finish.png")}
        for y in range(self.height):
            for x in range(self.width):
                x, y = x * self.tile_size, y * self.tile_size
                tile = pygame.sprite.Sprite(all_sprites)
                tile.image = tiles[self.get_tile_id((x, y))]
                tile.rect = tile.image.get_rect()
                tile.rect.x = x
                tile.rect.y = y

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


class Hero:
    def __init__(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        x, y = self.x * TILE_SIZE, self.y * TILE_SIZE
        all_sprites.add(AnimatedSprite(load_image("Player.png"), 8, 2, 50, 50, all_sprites))


class Game:
    def __init__(self, labyrinth, hero):
        self.labyrinth = labyrinth
        self.hero = hero

    def render(self, screen):
        self.labyrinth.render(screen)
        self.hero.render(screen)

    def update(self):
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


all_sprites = pygame.sprite.Group()


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    labyrinth = Labyrinth('testmap.txt', [0, 2], 2)
    for y in range(len(labyrinth.map)):
        if '3' in labyrinth.map[y]:
            hero_x = labyrinth.map[y].index('3')
            hero_y = y
            hero = Hero((hero_x, hero_y))

            game = Game(labyrinth, hero)

            clock = pygame.time.Clock()
            start_screen(screen, clock)
            break
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        game.render(screen)
        game.update()
        pygame.display.flip()
        clock.tick(FPS)
    final_screen(screen, clock)
    pygame.quit()


main()