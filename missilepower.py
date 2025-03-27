import pygame
import random
from circleshape import CircleShape
from constants import *

class MissilePowerup(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, MISSILE_POWERUP_RADIUS)
        self.rotation = 0  # For visual effect
        self.pulse_timer = 0  # For pulsing effect
        self.pulse_direction = 1  # 1 for growing, -1 for shrinking
        self.visual_scale = 1.0  # Visual scaling (doesn't affect hitbox)
        
    def update(self, dt):
        # Rotate the powerup for visual effect
        self.rotation += MISSILE_POWERUP_ROTATION_SPEED * dt
        
        # Pulsing effect
        self.pulse_timer += dt
        if self.pulse_timer > 0.05:  # Update pulse every 0.05 seconds
            self.pulse_timer = 0
            self.visual_scale += 0.02 * self.pulse_direction
            if self.visual_scale > 1.2:
                self.visual_scale = 1.2
                self.pulse_direction = -1
            elif self.visual_scale < 0.8:
                self.visual_scale = 0.8
                self.pulse_direction = 1
                
    def draw(self, screen):
        # Draw the missile powerup as a missile icon
        # Base shape is a circle
        pygame.draw.circle(screen, (255, 100, 100), self.position, 
                         self.radius * self.visual_scale, 2)
        
        # Calculate points for a missile shape inside the circle
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        right = forward.rotate(90)
        
        # Missile body
        body_length = self.radius * 0.8 * self.visual_scale
        body_width = self.radius * 0.4 * self.visual_scale
        
        # Calculate missile points
        nose = self.position + forward * body_length
        left_fin = self.position - forward * body_length * 0.5 - right * body_width
        right_fin = self.position - forward * body_length * 0.5 + right * body_width
        left_base = self.position - forward * body_length * 0.3 - right * body_width * 0.6
        right_base = self.position - forward * body_length * 0.3 + right * body_width * 0.6
        
        # Draw the missile shape
        pygame.draw.polygon(screen, (255, 150, 150), [
            nose, left_base, left_fin, self.position - forward * body_length, 
            right_fin, right_base
        ], 0)
        
        # Draw a small "M" in the center
        font = pygame.font.Font(None, int(self.radius * 1.5))
        text = font.render("M", True, (50, 50, 50))
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)
        
        # Draw hitbox in debug mode
        if SHOW_HITBOXES:
            pygame.draw.circle(screen, (255, 150, 0), self.position, self.radius, 3) 