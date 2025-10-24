import pygame
import math
from properties import Property

class Board:
    def __init__(self):
        self.properties = []
        self.corner_spaces = [0, 10, 20, 30]  # GO, Jail, Free Parking, Go to Jail
        self.railroads = [5, 15, 25, 35]  # Reading, Pennsylvania, B&O, Short Line
        self.utilities = [12, 28]  # Electric Company, Water Works
        self.tax_spaces = [4, 38]  # Income Tax, Luxury Tax
        self.chance_spaces = [7, 22, 36]
        self.community_chest_spaces = [2, 17, 33]
        
        # Initialize all properties with official Monopoly values
        self.properties = [
            # Brown Properties
            Property("Mediterranean Avenue", 60, (139, 69, 19), 1),
            Property("Baltic Avenue", 60, (139, 69, 19), 3),
            
            # Light Blue Properties
            Property("Oriental Avenue", 100, (173, 216, 230), 6),
            Property("Vermont Avenue", 100, (173, 216, 230), 8),
            Property("Connecticut Avenue", 120, (173, 216, 230), 9),
            
            # Pink Properties
            Property("St. Charles Place", 140, (255, 192, 203), 11),
            Property("States Avenue", 140, (255, 192, 203), 13),
            Property("Virginia Avenue", 160, (255, 192, 203), 14),
            
            # Orange Properties
            Property("St. James Place", 180, (255, 165, 0), 16),
            Property("Tennessee Avenue", 180, (255, 165, 0), 18),
            Property("New York Avenue", 200, (255, 165, 0), 19),
            
            # Red Properties
            Property("Kentucky Avenue", 220, (255, 0, 0), 21),
            Property("Indiana Avenue", 220, (255, 0, 0), 23),
            Property("Illinois Avenue", 240, (255, 0, 0), 24),
            
            # Yellow Properties
            Property("Atlantic Avenue", 260, (255, 255, 0), 26),
            Property("Ventnor Avenue", 260, (255, 255, 0), 27),
            Property("Marvin Gardens", 280, (255, 255, 0), 29),
            
            # Green Properties
            Property("Pacific Avenue", 300, (0, 255, 0), 31),
            Property("North Carolina Avenue", 300, (0, 255, 0), 32),
            Property("Pennsylvania Avenue", 320, (0, 255, 0), 34),
            
            # Blue Properties
            Property("Park Place", 350, (0, 0, 255), 37),
            Property("Boardwalk", 400, (0, 0, 255), 39),
            
            # Railroads
            Property("Reading Railroad", 200, (128, 128, 128), 5),
            Property("Pennsylvania Railroad", 200, (128, 128, 128), 15),
            Property("B&O Railroad", 200, (128, 128, 128), 25),
            Property("Short Line", 200, (128, 128, 128), 35),
            
            # Utilities
            Property("Electric Company", 150, (255, 255, 255), 12),
            Property("Water Works", 150, (255, 255, 255), 28)
        ]
        
        # Load and scale images
        self.load_images()
        
    def load_images(self):
        # Load dice images
        self.dice_images = []
        for i in range(1, 7):
            img = pygame.image.load(f"assets/images/dice{i}.png")
            img = pygame.transform.scale(img, (40, 40))
            self.dice_images.append(img)
            
        # Load property images
        self.property_images = {}
        for property in self.properties:
            try:
                img = pygame.image.load(f"assets/images/properties/{property.name.lower().replace(' ', '_')}.png")
                img = pygame.transform.scale(img, (40, 40))
                self.property_images[property.name] = img
            except:
                continue
                
        # Load corner images
        self.corner_images = {}
        corner_names = ["go", "jail", "free_parking", "go_to_jail"]
        for name in corner_names:
            try:
                img = pygame.image.load(f"assets/images/corners/{name}.png")
                img = pygame.transform.scale(img, (60, 60))
                self.corner_images[name] = img
            except:
                continue
    
    def draw(self, screen, current_player, dice_roll):
        board_size = 600
        board_x = (screen.get_width() - board_size) // 2
        board_y = (screen.get_height() - board_size) // 2
        
        # Draw board background with shadow
        shadow_surface = pygame.Surface((board_size + 20, board_size + 20), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 100), 
                        (10, 10, board_size, board_size), border_radius=10)
        screen.blit(shadow_surface, (board_x - 10, board_y - 10))
        
        # Draw main board
        pygame.draw.rect(screen, (255, 255, 255), 
                        (board_x, board_y, board_size, board_size), border_radius=10)
        
        # Draw properties
        for i in range(40):
            x, y = self.get_space_coordinates(board_x, board_y, board_size, i)
            
            # Draw space background
            if i in self.corner_spaces:
                pygame.draw.rect(screen, (200, 200, 200), (x, y, 60, 60))
            elif i in self.railroads:
                pygame.draw.rect(screen, (180, 180, 180), (x, y, 60, 60))
            elif i in self.utilities:
                pygame.draw.rect(screen, (220, 220, 220), (x, y, 60, 60))
            elif i in self.tax_spaces:
                pygame.draw.rect(screen, (240, 240, 240), (x, y, 60, 60))
            elif i in self.chance_spaces:
                pygame.draw.rect(screen, (255, 255, 200), (x, y, 60, 60))
            elif i in self.community_chest_spaces:
                pygame.draw.rect(screen, (200, 255, 200), (x, y, 60, 60))
            else:
                property = self.get_property_at_position(i)
                if property:
                    pygame.draw.rect(screen, property.color, (x, y, 60, 60))
            
            # Draw space border
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 60, 60), 1)
            
            # Draw space content
            if i in self.corner_spaces:
                self.draw_corner_space(screen, x, y, i)
            elif i in self.railroads:
                self.draw_railroad_space(screen, x, y, i)
            elif i in self.utilities:
                self.draw_utility_space(screen, x, y, i)
            elif i in self.tax_spaces:
                self.draw_tax_space(screen, x, y, i)
            elif i in self.chance_spaces:
                self.draw_chance_space(screen, x, y)
            elif i in self.community_chest_spaces:
                self.draw_community_chest_space(screen, x, y)
            else:
                property = self.get_property_at_position(i)
                if property:
                    self.draw_property_space(screen, x, y, property)
        
        # Draw dice if rolled
        if dice_roll:
            dice_x = board_x + board_size + 20
            dice_y = board_y + board_size - 100
            for i, value in enumerate(dice_roll):
                screen.blit(self.dice_images[value-1], (dice_x + i*50, dice_y))
    
    def draw_corner_space(self, screen, x, y, position):
        corner_names = ["go", "jail", "free_parking", "go_to_jail"]
        if position in self.corner_spaces:
            idx = self.corner_spaces.index(position)
            if corner_names[idx] in self.corner_images:
                screen.blit(self.corner_images[corner_names[idx]], (x, y))
            else:
                font = pygame.font.Font(None, 20)
                text = font.render(corner_names[idx].replace('_', ' ').title(), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + 30, y + 30))
                screen.blit(text, text_rect)
    
    def draw_railroad_space(self, screen, x, y, position):
        railroad = self.get_property_at_position(position)
        if railroad:
            font = pygame.font.Font(None, 16)
            text = font.render(railroad.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + 30, y + 30))
            screen.blit(text, text_rect)
    
    def draw_utility_space(self, screen, x, y, position):
        utility = self.get_property_at_position(position)
        if utility:
            font = pygame.font.Font(None, 16)
            text = font.render(utility.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + 30, y + 30))
            screen.blit(text, text_rect)
    
    def draw_tax_space(self, screen, x, y, position):
        font = pygame.font.Font(None, 16)
        text = font.render("Tax", True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + 30, y + 30))
        screen.blit(text, text_rect)
    
    def draw_chance_space(self, screen, x, y):
        font = pygame.font.Font(None, 16)
        text = font.render("Chance", True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + 30, y + 30))
        screen.blit(text, text_rect)
    
    def draw_community_chest_space(self, screen, x, y):
        font = pygame.font.Font(None, 16)
        text = font.render("Community Chest", True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + 30, y + 30))
        screen.blit(text, text_rect)
    
    def draw_property_space(self, screen, x, y, property):
        # Draw property name
        font = pygame.font.Font(None, 16)
        text = font.render(property.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + 30, y + 15))
        screen.blit(text, text_rect)
        
        # Draw price
        price_text = font.render(f"${property.price}", True, (0, 0, 0))
        price_rect = price_text.get_rect(center=(x + 30, y + 45))
        screen.blit(price_text, price_rect)
        
        # Draw houses/hotel if any
        if property.houses > 0:
            for i in range(property.houses):
                house_x = x + 10 + i * 10
                house_y = y + 30
                pygame.draw.rect(screen, (0, 255, 0), (house_x, house_y, 8, 8))
        elif property.hotel:
            hotel_x = x + 25
            hotel_y = y + 30
            pygame.draw.rect(screen, (255, 0, 0), (hotel_x, hotel_y, 10, 10))
    
    def get_space_coordinates(self, board_x, board_y, board_size, position):
        if position < 10:  # Bottom row
            x = board_x + 60 + (board_size - 120) * (position / 10)
            y = board_y + board_size - 60
        elif position < 20:  # Right column
            x = board_x + board_size - 60
            y = board_y + 60 + (board_size - 120) * ((19 - position) / 10)
        elif position < 30:  # Top row
            x = board_x + 60 + (board_size - 120) * ((29 - position) / 10)
            y = board_y
        else:  # Left column
            x = board_x
            y = board_y + 60 + (board_size - 120) * ((position - 30) / 10)
        return x, y
    
    def get_property_at_position(self, position):
        for property in self.properties:
            if property.position == position:
                return property
        return None 