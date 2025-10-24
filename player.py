import pygame
import math

class Player:
    def __init__(self, name, color, money):
        self.name = name
        self.color = color
        self.money = money
        self.position = 0
        self.properties = []
        self.jail_cards = 0
        self.jail_turns = 0
        self.moving = False
        self.target_position = 0
        self.move_speed = 0.1  # Slower movement speed
        self.current_move = 0
        self.total_spaces = 40  # Total number of spaces on the board
        self.path_positions = []  # List to store positions along the path
        
        # Visual properties
        self.rotation = 0
        self.scale = 1.0
        self.target_scale = 1.0
        self.shadow_offset = 5
        self.animation_state = "idle"  # idle, moving, jumping, celebrating
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.bounce_height = 0
        self.target_bounce_height = 0
        self.celebration_rotation = 0
        self.target_celebration_rotation = 0
        
    def move(self, spaces):
        if self.jail_turns > 0:
            self.jail_turns -= 1
            return
            
        # Calculate new position
        self.target_position = (self.position + spaces) % self.total_spaces
        self.moving = True
        self.current_move = 0
        
        # Generate path positions
        self.path_positions = []
        current_pos = self.position
        for _ in range(spaces):
            current_pos = (current_pos + 1) % self.total_spaces
            self.path_positions.append(current_pos)
        
        # Check if passing GO
        if self.target_position < self.position:
            self.money += 200  # Collect $200 for passing GO
            
    def move_to(self, position):
        self.target_position = position
        self.moving = True
        self.animation_state = "moving"
    
    def move_to_nearest_utility(self):
        current_pos = self.position
        utility_positions = [12, 28]  # Electric Company and Water Works
        nearest = min(utility_positions, key=lambda x: (x - current_pos) % 40)
        self.move_to(nearest)
    
    def move_to_nearest_railroad(self):
        current_pos = self.position
        railroad_positions = [5, 15, 25, 35]
        nearest = min(railroad_positions, key=lambda x: (x - current_pos) % 40)
        self.move_to(nearest)
    
    def go_to_jail(self):
        self.position = 10  # Jail position
        self.jail_turns = 0
        self.animation_state = "jumping"
        self.target_bounce_height = 30
    
    def add_jail_card(self):
        self.jail_cards += 1
    
    def use_jail_card(self):
        if self.jail_cards > 0:
            self.jail_cards -= 1
            self.animation_state = "celebrating"
            self.target_celebration_rotation = 180
            return True
        return False
    
    def pay_repairs(self):
        total_cost = 0
        for property in self.properties:
            if property.houses > 0:
                total_cost += property.houses * 25
            if property.hotel:
                total_cost += 100
        self.pay_money(total_cost)
    
    def pay_each_player(self, amount):
        # This will be handled by the game class
        return amount
    
    def update(self, board_x, board_y, board_size):
        if not self.moving:
            return
            
        # Update movement
        self.current_move += self.move_speed
        if self.current_move >= 1.0:
            self.position = self.target_position
            self.moving = False
            self.current_move = 0
            self.path_positions = []
            return
            
        # Calculate current position based on path
        path_index = int(self.current_move * len(self.path_positions))
        if path_index >= len(self.path_positions):
            path_index = len(self.path_positions) - 1
        current_pos = self.path_positions[path_index]
        
        # Calculate position on board
        space_size = board_size / 11  # 11 spaces per side
        if current_pos < 10:  # Bottom row (right to left)
            self.x = board_x + board_size - (current_pos + 1) * space_size
            self.y = board_y + board_size - space_size
        elif current_pos < 20:  # Left side (bottom to top)
            self.x = board_x
            self.y = board_y + board_size - (current_pos - 9) * space_size
        elif current_pos < 30:  # Top row (left to right)
            self.x = board_x + (current_pos - 19) * space_size
            self.y = board_y
        else:  # Right side (top to bottom)
            self.x = board_x + board_size - space_size
            self.y = board_y + (current_pos - 29) * space_size
            
        # Update visual effects
        if self.moving:
            self.scale = 1.2  # Slightly larger while moving
            if self.target_position < self.position:  # Passing GO
                self.rotation += 5  # Rotate while passing GO
        else:
            self.scale = 1.0
            self.rotation = 0
            
        # Smooth scale transition
        self.scale += (self.target_scale - self.scale) * 0.1
        
        # Update animation frame
        self.animation_frame += self.animation_speed
        
        # Handle different animation states
        if self.animation_state == "moving":
            # Calculate target coordinates
            target_x, target_y = self.get_position_coordinates(board_x, board_y, board_size, self.target_position)
            
            # Move towards target
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.move_speed:
                self.x = target_x
                self.y = target_y
                self.position = self.target_position
                self.moving = False
                self.animation_state = "idle"
                self.target_scale = 1.0
                self.rotation = 0
            else:
                self.x += (dx/distance) * self.move_speed
                self.y += (dy/distance) * self.move_speed
                # Add slight bounce while moving
                self.bounce_height = math.sin(self.animation_frame * 4) * 5
        
        elif self.animation_state == "jumping":
            # Update bounce height
            self.bounce_height += (self.target_bounce_height - self.bounce_height) * 0.2
            if abs(self.target_bounce_height - self.bounce_height) < 0.1:
                self.target_bounce_height = 0
                if self.target_bounce_height == 0:
                    self.animation_state = "idle"
        
        elif self.animation_state == "celebrating":
            # Update celebration rotation
            self.celebration_rotation += (self.target_celebration_rotation - self.celebration_rotation) * 0.2
            if abs(self.target_celebration_rotation - self.celebration_rotation) < 1:
                self.celebration_rotation = 0
                self.animation_state = "idle"
        
        # Update scale
        self.target_scale += (1.0 - self.target_scale) * 0.1
    
    def draw(self, screen):
        board_size = 600
        board_x = (screen.get_width() - board_size) // 2
        board_y = (screen.get_height() - board_size) // 2
        
        if not self.moving:
            self.x, self.y = self.get_position_coordinates(board_x, board_y, board_size, self.position)
        
        # Apply bounce height
        current_y = self.y - self.bounce_height
        
        # Create token surface
        token_size = 30
        token_surface = pygame.Surface((token_size * 2, token_size * 2), pygame.SRCALPHA)
        
        # Draw shadow
        shadow_surface = pygame.Surface((token_size * 2, token_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 100), 
                         (token_size + self.shadow_offset, token_size + self.shadow_offset), 
                         token_size)
        screen.blit(shadow_surface, 
                   (self.x - token_size + self.shadow_offset, 
                    current_y - token_size + self.shadow_offset))
        
        # Draw token
        pygame.draw.circle(token_surface, self.color, (token_size, token_size), token_size)
        pygame.draw.circle(token_surface, (0, 0, 0), (token_size, token_size), token_size, 2)
        
        # Draw token design
        pygame.draw.circle(token_surface, (255, 255, 255), (token_size, token_size), token_size - 4)
        pygame.draw.circle(token_surface, self.color, (token_size, token_size), token_size - 6)
        
        # Scale and rotate token
        scaled_size = int(token_size * 2 * self.scale)
        scaled_token = pygame.transform.scale(token_surface, (scaled_size, scaled_size))
        
        # Apply rotation based on animation state
        if self.animation_state == "celebrating":
            rotated_token = pygame.transform.rotate(scaled_token, self.celebration_rotation)
        else:
            rotated_token = pygame.transform.rotate(scaled_token, self.rotation)
        
        # Draw token
        screen.blit(rotated_token, 
                   (self.x - rotated_token.get_width()//2, 
                    current_y - rotated_token.get_height()//2))
        
        # Draw player name with background
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.x = int(self.x + 40)
        text_rect.y = int(current_y + 25)
        
        # Draw name background
        pygame.draw.rect(screen, (255, 255, 255, 200), text_rect.inflate(10, 5))
        screen.blit(text, text_rect)
        
        # Draw jail status
        if self.jail_turns > 0:
            jail_text = font.render("JAIL", True, (255, 0, 0))
            jail_rect = jail_text.get_rect()
            jail_rect.x = int(self.x + 40)
            jail_rect.y = int(current_y + 45)
            screen.blit(jail_text, jail_rect)
    
    def get_position_coordinates(self, board_x, board_y, board_size, pos):
        space_size = board_size / 11  # 11 spaces per side
        if pos < 10:  # Bottom row (right to left)
            x = board_x + board_size - (pos + 1) * space_size
            y = board_y + board_size - space_size
        elif pos < 20:  # Left side (bottom to top)
            x = board_x
            y = board_y + board_size - (pos - 9) * space_size
        elif pos < 30:  # Top row (left to right)
            x = board_x + (pos - 19) * space_size
            y = board_y
        else:  # Right side (top to bottom)
            x = board_x + board_size - space_size
            y = board_y + (pos - 29) * space_size
        return x, y
    
    def buy_property(self, property):
        if self.money >= property.price:
            self.money -= property.price
            self.properties.append(property)
            property.owner = self
            self.animation_state = "celebrating"
            self.target_celebration_rotation = 180
            return True
        return False
    
    def pay_rent(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def receive_money(self, amount):
        self.money += amount
        self.animation_state = "celebrating"
        self.target_celebration_rotation = 180
    
    def pay_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def add_property(self, property):
        self.properties.append(property)
        property.owner = self
    
    def remove_property(self, property):
        if property in self.properties:
            self.properties.remove(property)
            property.owner = None
    
    def get_total_worth(self):
        worth = self.money
        for property in self.properties:
            worth += property.price
        return worth
    
    def is_bankrupt(self):
        return self.money < 0 and self.get_total_worth() < 0 