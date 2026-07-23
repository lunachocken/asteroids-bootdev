import sys

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event

from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


class Game:
    def __init__(self) -> None:
        print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
        print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        self.player: Player | None = None
        self.init_player()

        self.init_asteroids()
        self.spawn_asteroid_field()
        self.init_shot()

    def init_shot(self):
        Shot.containers = (self.shots, self.drawable, self.updatable)

    def init_asteroids(self):
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable,)

    def init_player(self):
        # Create player
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2
        Player.containers = (self.updatable, self.drawable)
        self.player = Player(x, y)

    def spawn_asteroid_field(self):
        self.asteroid_field = AsteroidField()

    def gameloop(self):
        while True:
            # updatable = self.updatable
            # drawable = self.drawable
            asteroids = self.asteroids
            shots = self.shots
            log_state()
            asteroid: Asteroid
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()

                if asteroid.collides_with(self.player):
                    log_event("player_hit")
                    print("Game Over!")
                    sys.exit()

            self.dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.screen.fill("black")

            # Player Section
            # self.player.update(self.dt)
            self.updatable.update(self.dt)
            # self.drawable.draw(self.screen)
            for asteroid in self.drawable:
                asteroid.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    Game().gameloop()
