import sys
import pygame
from pygame.sprite import Group, spritecollide
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot
from missile import Missile

def game_over_screen(score):
    game_over_font = pygame.font.Font(None, MENU_TITLE_SIZE)
    score_font = pygame.font.Font(None, MENU_OPTION_SIZE)
    instruction_font = pygame.font.Font(None, SCORE_FONT_SIZE)
    
    game_over_text = game_over_font.render("GAME OVER", True, MENU_TITLE_COLOR)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    
    score_text = score_font.render(f"Final Score: {score}", True, MENU_OPTION_COLOR)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    instruction_text = instruction_font.render("Press Enter to return to menu", True, MENU_OPTION_COLOR)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    return
        
        screen.fill("black")
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()
        clock.tick(60)

def game_loop():
    
    # Initialize score and lives
    score = 0
    lives = PLAYER_LIVES
    font = pygame.font.Font(None, SCORE_FONT_SIZE)

    clock = pygame.time.Clock()
    dt = 0

    # Clear existing sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    missiles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Missile.containers = (missiles, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.respawn(reset_missiles=True)  # Reset missiles when starting new game
    asteroid_field = AsteroidField()
    asteroid_field.asteroid_group = asteroids
    asteroid_field.reset()  # Call reset after setting asteroid_group
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Return to main menu
                if event.key == pygame.K_e:
                    # Handle missile firing here (in addition to the key check in player update)
                    player.fire_missile()

        screen.fill("black")
        for object in updatable:
            object.update(dt)
        for object in drawable:
            object.draw(screen)
            
        # Check player collisions with asteroids
        for asteroid in asteroids:
            if asteroid.is_colliding(player) and not player.is_invulnerable:
                lives -= 1
                print(f"Lives remaining: {lives}")
                
                if lives <= 0:
                    print("Game over!")
                    game_over_screen(score)
                    return  # Return to main menu on game over
                else:
                    # Respawn player with invulnerability
                    player.respawn()
            
            # Check regular shot collisions
            for shot in shots:
                if asteroid.is_colliding(shot):
                    shot.kill()
                    if asteroid.split():
                        # Increase score when an asteroid is fully destroyed
                        score += SCORE_ASTEROID_SMALL
            
            # Check missile collisions - missiles destroy any asteroid on contact
            for missile in missiles:
                if asteroid.is_colliding(missile):
                    missile.kill()
                    # Calculate score based on asteroid size
                    if asteroid.radius >= ASTEROID_MIN_RADIUS * 3:
                        score += SCORE_ASTEROID_SMALL * 4  # Large asteroid
                    elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                        score += SCORE_ASTEROID_SMALL * 2  # Medium asteroid
                    else:
                        score += SCORE_ASTEROID_SMALL      # Small asteroid
                    
                    # Immediately destroy the asteroid without splitting
                    asteroid.kill()
        
        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(score_text, score_rect)
        
        # Display lives
        lives_text = font.render(f"Lives: ", True, (255, 255, 255))
        lives_rect = lives_text.get_rect(topleft=(20, 20))
        screen.blit(lives_text, lives_rect)
        
        # Draw life icons
        for i in range(lives):
            # Create a mini player triangle for each life
            mini_player_pos = pygame.Vector2(lives_rect.right + 30 + i * 30, lives_rect.centery)
            
            # Draw a small ship for each life
            radius = PLAYER_RADUIUS * 0.7
            forward = pygame.Vector2(0, -1)  # Point upward
            right = pygame.Vector2(1, 0) * radius / 1.5
            
            # Calculate triangle points
            a = mini_player_pos + forward * radius
            b = mini_player_pos - forward * radius - right
            c = mini_player_pos - forward * radius + right
            
            # Draw the triangle
            pygame.draw.polygon(screen, "white", [a, b, c], 1)
        
        # Display missile count
        missile_text = font.render(f"Missiles: {player.missiles_remaining}", True, (255, 100, 100))
        missile_rect = missile_text.get_rect(topleft=(20, 60))
        screen.blit(missile_text, missile_rect)
        
        # Display controls
        controls_text = font.render("Controls: W/A/S/D to move, SPACE to shoot, E for missiles, ESC for menu", True, (150, 150, 150))
        controls_rect = controls_text.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        screen.blit(controls_text, controls_rect)

        pygame.display.flip()
        dt = clock.tick(60.0) / 1000

def main_menu():
    selected_option = 0
    options = ["Play", "Quit"]
    
    title_font = pygame.font.Font(None, MENU_TITLE_SIZE)
    option_font = pygame.font.Font(None, MENU_OPTION_SIZE)
    instruction_font = pygame.font.Font(None, SCORE_FONT_SIZE)
    
    title_text = title_font.render("ASTEROIDS", True, MENU_TITLE_COLOR)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    
    instruction_text = instruction_font.render("Use arrow keys to navigate, Enter to select", True, MENU_OPTION_COLOR)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    
    # Create a simple player ship for visual effect (without containers)
    player_vis = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    # Save original Player.containers and temporarily set to None
    original_containers = Player.containers if hasattr(Player, 'containers') else None
    Player.containers = None
    
    menu_running = True
    clock = pygame.time.Clock()
    while menu_running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Play
                        game_loop()
                    elif selected_option == 1:  # Quit
                        pygame.quit()
                        sys.exit()
        
        screen.fill("black")
        
        # Rotate the player ship for visual effect
        player_vis.rotation += 30 * dt
        
        # Draw title
        screen.blit(title_text, title_rect)
        
        # Draw menu options
        for i, option in enumerate(options):
            color = MENU_SELECTED_COLOR if i == selected_option else MENU_OPTION_COLOR
            option_text = option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 70))
            screen.blit(option_text, option_rect)
        
        # Draw instructions
        screen.blit(instruction_text, instruction_rect)
        
        # Draw the player ship
        player_vis.draw(screen)
        
        pygame.display.flip()
    
    # Restore original containers
    Player.containers = original_containers

def main():
    global screen, clock
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
    pygame.display.set_caption("Asteroids")
    
    clock = pygame.time.Clock()
    
    main_menu()

if __name__ == "__main__":
    main()
