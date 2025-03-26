import pygame
from circleshape import CircleShape
from constants import *

class Missile(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.timer = 0  # For animation effects

    def draw(self, screen):
        # Draw the missile as a filled circle with a trail
        pygame.draw.circle(screen, (255, 100, 100), self.position, self.radius)
        
        # Draw a small trail behind the missile
        if self.velocity.length() > 0:
            direction = self.velocity.normalize()
            trail_pos = self.position - direction * self.radius * 2
            pygame.draw.circle(screen, (255, 200, 100), trail_pos, self.radius * 0.7)
            
            # Second trail segment
            trail_pos2 = trail_pos - direction * self.radius * 1.5
            pygame.draw.circle(screen, (255, 200, 200), trail_pos2, self.radius * 0.4)

    def update(self, dt):
        self.position += self.velocity * dt
        self.timer += dt 