import sys
import pygame
from pygame.sprite import Group, spritecollide
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for object in updatable:
            object.update(dt)
        for object in drawable:
            object.draw(screen)
        for asteroid in asteroids:
            if asteroid.is_colliding(player):
                print("Game over!")
                sys.exit()
            for shot in shots:
                if asteroid.is_colliding(shot):
                    shot.kill()
                    asteroid.split()

        pygame.display.flip()
        dt = clock.tick(60.0) / 1000
if __name__ == "__main__":
    main()
