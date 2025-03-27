import pygame
import random
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
        self.is_thrusting = False
        self._triangle_points = []  # Cached triangle points for hitbox

        super().__init__(self.x, self.y, PLAYER_RADUIUS)

        self.timer = 0

    def is_colliding(self, circle):
        # Only use circle collision if we're invulnerable (for simplicity)
        if self.is_invulnerable:
            return False
        
        # Get updated triangle points
        tri_points = self.triangle()
        
        # Skip the initial circle vs circle check - use triangle directly
        
        # Check if any point of the triangle is inside the circle
        for point in tri_points:
            if pygame.math.Vector2.distance_to(pygame.Vector2(point), circle.position) <= circle.radius:
                return True
                
        # Check if the center of the circle is inside the triangle
        if self._point_in_triangle(circle.position, *tri_points):
            return True
            
        # Check if the circle intersects any of the triangle's edges
        if self._circle_intersects_line(circle, tri_points[0], tri_points[1]) or \
           self._circle_intersects_line(circle, tri_points[1], tri_points[2]) or \
           self._circle_intersects_line(circle, tri_points[2], tri_points[0]):
            return True
            
        return False
    
    def _point_in_triangle(self, p, a, b, c):
        # Check if point p is inside triangle abc
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
            
        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        # If all signs are the same, point is inside the triangle
        return not (has_neg and has_pos)
        
    def _circle_intersects_line(self, circle, p1, p2):
        # Check if circle intersects line segment p1-p2
        # Convert points to vectors
        p1 = pygame.Vector2(p1)
        p2 = pygame.Vector2(p2)
        
        # Vector from p1 to p2
        line_vec = p2 - p1
        line_len = line_vec.length()
        if line_len == 0:
            return False
            
        # Vector from p1 to circle center
        circle_vec = circle.position - p1
        
        # Project circle_vec onto line_vec
        proj = circle_vec.dot(line_vec) / line_len
        
        # Find closest point on line to circle
        if proj <= 0:
            closest = p1  # Circle is closest to p1
        elif proj >= line_len:
            closest = p2  # Circle is closest to p2
        else:
            # Circle is closest to a point on the line segment
            closest = p1 + line_vec * (proj / line_len)
            
        # Check if closest point is within circle radius
        dist = pygame.math.Vector2.distance_to(circle.position, closest)
        return dist <= circle.radius

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
            # Draw the player ship
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
            
            # Draw thruster flame when accelerating
            if self.is_thrusting:
                # Get the base of the ship
                forward = pygame.Vector2(0, 1).rotate(self.rotation)
                flame_base = self.position - forward * self.radius
                flame_width = self.radius * 0.6
                
                # Create flame points with randomized length
                left_edge = flame_base - forward.rotate(90) * flame_width * 0.5
                right_edge = flame_base + forward.rotate(90) * flame_width * 0.5
                tip = flame_base - forward * (self.radius * 0.5 + random.random() * self.radius * 0.3)
                
                # Draw the flame
                pygame.draw.polygon(screen, (255, 150, 50), [left_edge, right_edge, tip], 0)
            
        # Draw hitbox in debug mode - draw last so it's on top and visible
        # Even when player is invulnerable, showing the hitbox is useful for debugging
        if SHOW_HITBOXES:
            tri = self.triangle()
            # Draw more visibly with thicker lines and brighter color
            pygame.draw.polygon(screen, (0, 255, 0), tri, 3)  # Green triangle hitbox

    def triangle(self):
        # Use the same direction vectors as used in the draw method for consistency
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = forward.rotate(90)
        
        # Calculate points for the triangle matching the visible ship
        a = self.position + forward * self.radius  # Front nose of the ship
        b = self.position - forward * self.radius * 0.5 - right * self.radius / 1.5  # Left rear corner
        c = self.position - forward * self.radius * 0.5 + right * self.radius / 1.5  # Right rear corner
        
        # Cache the triangle points as tuples for collision detection
        self._triangle_points = [(a.x, a.y), (b.x, b.y), (c.x, c.y)]
        return self._triangle_points

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
        # If we have some velocity, gradually align a small amount with our new direction
        if self.velocity.length() > 0.5:
            speed = self.velocity.length()
            # Get forward direction
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            
            # Ensure drift factor is clamped to [0,1]
            drift = min(1.0, max(0.0, PLAYER_DRIFT_FACTOR * dt))
            
            # Blend between current velocity and direction facing with a very small factor
            # This gives subtle control with turning
            current_dir = self.velocity.normalize()
            new_dir = pygame.Vector2(
                current_dir.x * (1 - drift) + forward.x * drift,
                current_dir.y * (1 - drift) + forward.y * drift
            )
            if new_dir.length() > 0:  # Ensure we don't divide by zero
                new_dir = new_dir.normalize()
                # Apply the smoothed direction
                self.velocity = new_dir * speed

    def accelerate(self, dt, reverse=False):
        # Set thruster flag for visuals
        self.is_thrusting = not reverse
        
        # Direction of acceleration
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if reverse:
            forward = -forward
            factor = 0.7  # Slower when reversing
        else:
            factor = 1.0
            
        # Apply acceleration in the direction we're facing
        self.velocity += forward * PLAYER_ACCELERATION * factor * dt
        
        # Cap maximum speed
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    def decelerate(self, dt):
        # Apply deceleration if we have velocity
        if self.velocity.length() > 0:
            decel_amount = PLAYER_DECELERATION * dt
            
            # If deceleration would reverse direction, just stop
            if decel_amount > self.velocity.length():
                self.velocity = pygame.Vector2(0, 0)
            else:
                # Apply deceleration in the opposite direction of movement
                self.velocity -= self.velocity.normalize() * decel_amount

    def update(self, dt):
        self.timer -= dt
        self.missile_timer -= dt
        
        # Reset thruster flag
        self.is_thrusting = False
        
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
            self.accelerate(dt)
        elif keys[pygame.K_s]:
            self.accelerate(dt, reverse=True)
        else:
            # Apply gentle deceleration when not thrusting
            self.decelerate(dt)
            
        # Update position based on velocity
        self.position += self.velocity * dt
        
        # Screen wrapping
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def add_missiles(self, count):
        # Add missiles to player's inventory
        self.missiles_remaining += count
        # Reset missile cooldown as a bonus
        self.missile_timer = 0
