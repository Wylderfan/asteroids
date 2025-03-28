import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self.__class__, "containers") and self.__class__.containers is not None:
            super().__init__(self.__class__.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def is_colliding(self, circle):
        dist = pygame.math.Vector2.distance_to(self.position, circle.position)
        return (self.radius + circle.radius) > dist

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass
