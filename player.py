import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
from missile import Missile


class Player(CircleShape):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation = 0
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.blink_timer = 0
        self.visible = True
        self.start_position = pygame.Vector2(x, y)
        self.missiles_remaining = PLAYER_MISSILE_COUNT
        self.missile_timer = 0

        super().__init__(self.x, self.y, PLAYER_RADUIUS)

        self.timer = 0

    def respawn(self, reset_missiles=False):
        self.position = pygame.Vector2(self.start_position)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.is_invulnerable = True
        self.invulnerable_timer = PLAYER_RESPAWN_TIME
        self.blink_timer = PLAYER_BLINK_RATE
        self.visible = False
        
        # Reset missile count if starting a new game
        if reset_missiles:
            self.missiles_remaining = PLAYER_MISSILE_COUNT

    def shoot(self):
        if self.timer <= 0:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.math.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
            self.timer = PLAYER_SHOT_COOLDOWN
            
    def fire_missile(self):
        if self.missile_timer <= 0 and self.missiles_remaining > 0:
            missile = Missile(self.position.x, self.position.y, MISSILE_RADIUS)
            missile.velocity = pygame.math.Vector2(0, 1).rotate(self.rotation) * MISSILE_SPEED
            self.missile_timer = MISSILE_COOLDOWN
            self.missiles_remaining -= 1
            return True
        return False

    def draw(self, screen):
        if not self.is_invulnerable or self.visible:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        self.missile_timer -= dt
        
        # Update invulnerability
        if self.is_invulnerable:
            self.invulnerable_timer -= dt
            self.blink_timer -= dt
            
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = PLAYER_BLINK_RATE
                
            if self.invulnerable_timer <= 0:
                self.is_invulnerable = False
                self.visible = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_e]:
            self.fire_missile()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
