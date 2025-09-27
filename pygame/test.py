import pygame
from MyGame import Map, WORLD_HEIGHT, WORLD_WIDTH
import Colors

# Inicializar pygame
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

clock = pygame.time.Clock()
game_map = Map(WORLD_WIDTH, WORLD_HEIGHT)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def main():
    pygame.display.set_caption("Laberinto")

    # Bucle principal
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Rellenar el fondo6
        screen.fill(Colors.BLACK)

        handle_input(events)
        render_map()

        if has_win():
            (size_x, size_y) = screen.get_size()
            pygame.draw.rect(screen, Colors.GREEN, (0, 0, size_x, size_y))

        # Actualizar pantalla
        pygame.display.flip()

        clock.tick(20)

    pygame.quit()


def render_map():
    game_map.render(screen)


def handle_input(events):
    for event in events:
        # una vez cuando se presiona
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player("up")
            if event.key == pygame.K_DOWN:
                move_player("down")
            if event.key == pygame.K_LEFT:
                move_player("left")
            if event.key == pygame.K_RIGHT:
                move_player("right")


def move_player(direction: str):

    _direction = (0, 0)
    if direction == "up":
        _direction = (0, -1)
    if direction == "down":
        _direction = (0, 1)
    if direction == "left":
        _direction = (-1, 0)
    if direction == "right":
        _direction = (1, 0)

    (x, y) = game_map.player.get_position(game_map)
    game_map.move_player(x + _direction[0], y + _direction[1])


def has_win() -> bool:
    return game_map.goal.get_position(game_map) == game_map.player.get_position(game_map)


main()
