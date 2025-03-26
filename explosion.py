import pygame
import random
import math
from constants import *

class ExplosionParticle:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize() * random.uniform(EXPLOSION_SPEED * 0.5, EXPLOSION_SPEED)
        self.radius = random.uniform(2, 5)
        self.lifetime = EXPLOSION_DURATION
        self.color = color
        self.base_color = color
        self.alpha = 255

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        self.alpha = max(0, int(255 * (self.lifetime / EXPLOSION_DURATION)))
        # Slow down over time
        self.velocity *= 0.95
        
    def draw(self, screen):
        if self.alpha <= 0:
            return
            
        color = list(self.base_color)
        # Create a new color with the current alpha
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            surface, 
            (*color, self.alpha), 
            (self.radius, self.radius), 
            self.radius
        )
        screen.blit(surface, (self.position.x - self.radius, self.position.y - self.radius))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color=(255, 200, 100)):
        if hasattr(self.__class__, "containers") and self.__class__.containers is not None:
            pygame.sprite.Sprite.__init__(self, self.containers)
        else:
            pygame.sprite.Sprite.__init__(self)
            
        self.position = pygame.Vector2(x, y)
        self.particles = []
        
        # Create particles based on size
        num_particles = int(EXPLOSION_PARTICLES * (size / ASTEROID_MIN_RADIUS))
        
        for _ in range(num_particles):
            # Add some color variation
            particle_color = (
                min(255, color[0] + random.randint(-20, 20)),
                min(255, color[1] + random.randint(-20, 20)),
                min(255, color[2] + random.randint(-20, 20))
            )
            self.particles.append(ExplosionParticle(x, y, particle_color))
        
        self.lifetime = EXPLOSION_DURATION

    def update(self, dt):
        self.lifetime -= dt
        
        for particle in self.particles:
            particle.update(dt)
            
        # Remove explosion when all particles are done
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen) 