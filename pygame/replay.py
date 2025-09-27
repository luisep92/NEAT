# replay.py
import pickle
import neat
import pygame
import Colors
from MyGame import Map
from env import SimpleGridEnv


def load_winner(path="best-genome.pkl", cfg="neat-config.ini"):
    with open(path, "rb") as f:
        winner = pickle.load(f)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, cfg)
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    return net


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    net = load_winner()
    env = SimpleGridEnv()
    obs = env.reset()

    running = True
    done = False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        if not done:
            out = net.activate(obs)
            action = max(range(len(out)), key=lambda i: out[i])
            obs, reward, done, info = env.step(action)

        screen.fill(Colors.BLACK)
        # Renderiza usando tu Map original
        env.map.render(screen)

        if done and info.get("win"):
            size_x, size_y = screen.get_size()
            s = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
            s.fill((0, 255, 0, 90))
            screen.blit(s, (0, 0))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
