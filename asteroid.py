import random

import pygame
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from circleshape import CircleShape
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            surface=screen,
            color="white",
            center=self.position,
            radius=self.radius,
            width=LINE_WIDTH,
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        asteroid1_velocity = self.velocity.rotate(angle)
        asteroid2_velocity = self.velocity.rotate(-angle)
        # new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_radius = self.radius - (self.radius / 8)

        as1 = Asteroid(self.position.x, self.position.y, new_radius)
        as1.velocity = asteroid1_velocity * 1.2

        as2 = Asteroid(self.position.x, self.position.y, new_radius)
        as2.velocity = asteroid2_velocity * 1.2
