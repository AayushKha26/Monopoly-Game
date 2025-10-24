import pygame
import os

# Initialize Pygame
pygame.init()

# Create dice images
def create_dice_image(value, size=60):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Draw white background
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, size, size))
    pygame.draw.rect(surface, (0, 0, 0), (0, 0, size, size), 2)
    
    # Draw dots based on value
    dot_positions = {
        1: [(size//2, size//2)],
        2: [(size//4, size//4), (3*size//4, 3*size//4)],
        3: [(size//4, size//4), (size//2, size//2), (3*size//4, 3*size//4)],
        4: [(size//4, size//4), (size//4, 3*size//4), (3*size//4, size//4), (3*size//4, 3*size//4)],
        5: [(size//4, size//4), (size//4, 3*size//4), (size//2, size//2), (3*size//4, size//4), (3*size//4, 3*size//4)],
        6: [(size//4, size//4), (size//4, size//2), (size//4, 3*size//4), (3*size//4, size//4), (3*size//4, size//2), (3*size//4, 3*size//4)]
    }
    
    for pos in dot_positions[value]:
        pygame.draw.circle(surface, (0, 0, 0), pos, size//8)
    
    return surface

# Create dice images directory if it doesn't exist
os.makedirs("assets/images/dice", exist_ok=True)

# Generate dice images
for i in range(1, 7):
    dice_surface = create_dice_image(i)
    pygame.image.save(dice_surface, f"assets/images/dice{i}.png")

pygame.quit() 