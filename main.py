import pygame
import sys
import random
import math
from board import Board
from player import Player
from properties import Property
from cards import CardDeck, create_chance_cards, create_community_chest_cards
from minigames import DiceRollGame, PropertyAuction, JailEscape

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOARD_SIZE = 800
BUTTON_HEIGHT = 40
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_BLUE = (135, 206, 235)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
PREMIUM_GREEN = (0, 80, 0)
PREMIUM_GREEN_HOVER = (0, 120, 0)
MAROON = (128, 0, 0)
MAROON_HOVER = (160, 0, 0)
BOARD_BG = (245, 245, 245)  # Lighter gray for board background
BOARD_BORDER = (80, 80, 80)  # Darker gray for board border
INFO_BG = (255, 255, 255, 220)  # More opaque white for info panel
BUTTON_BG = (255, 255, 255, 200)  # More opaque white for buttons
BOARD_SHADOW = (0, 0, 0, 30)  # Subtle shadow for board
BUTTON_SHADOW = (0, 0, 0, 40)  # Slightly stronger shadow for buttons

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monopoly Game")

# Load fonts
try:
    FONT_BOLD = pygame.font.Font("assets/fonts/PlayfairDisplaySemibold.ttf", 36)
    FONT_REGULAR = pygame.font.Font("assets/fonts/PlayfairDisplay-VariableFont_wght.ttf", 24)
    FONT_ITALIC = pygame.font.Font("assets/fonts/PlayfairDisplay-Italic-VariableFont_wght.ttf", 24)
except FileNotFoundError as e:
    print(f"Error loading fonts: {e}")
    print("Using system fonts as fallback")
    FONT_BOLD = pygame.font.SysFont("arial", 36, bold=True)
    FONT_REGULAR = pygame.font.SysFont("arial", 24)
    FONT_ITALIC = pygame.font.SysFont("arial", 24, italic=True)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = 30
        self.alpha = 255
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.alpha = int((self.lifetime / 30) * 255)
        
    def draw(self, screen):
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*self.color, self.alpha), (self.size, self.size), self.size)
        screen.blit(surface, (self.x - self.size, self.y - self.size))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particles(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
            
    def update(self):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()
            
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

class Dice:
    def __init__(self):
        self.values = [1, 1]
        self.rolling = False
        self.roll_frames = 0
        self.roll_duration = 30
        self.size = 120  # Increased dice size
        self.rotation = 0
        self.rotation_speed = 15
        self.shadow_offset = 8
        self.final_values = [1, 1]
        self.animation_complete = False
        # Center position for animation
        self.center_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        # Final position after animation
        self.final_pos = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 150)
        self.current_pos = self.final_pos
        
    def roll(self):
        self.rolling = True
        self.roll_frames = 0
        self.rotation = 0
        self.final_values = [random.randint(1, 6), random.randint(1, 6)]
        self.animation_complete = False
        self.current_pos = self.center_pos  # Start from center
        
    def update(self):
        if self.rolling:
            self.roll_frames += 1
            self.rotation += self.rotation_speed
            
            # During animation, show random values and stay in center
            if self.roll_frames < self.roll_duration:
                self.values = [random.randint(1, 6), random.randint(1, 6)]
                return False
            else:
                self.rolling = False
                self.values = self.final_values
                self.rotation = 0
                self.animation_complete = True
                self.current_pos = self.final_pos  # Move to corner
                return True
        return False

    def draw(self, screen):
        if not self.rolling and not self.animation_complete:
            return
            
        # Add screen darkening effect during roll
        if self.rolling:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
        # Draw two dice side by side
        for i, value in enumerate(self.values):
            x_offset = i * (self.size + 40) - (self.size + 40) // 2  # Center the pair of dice
            
            # Draw shadow
            shadow_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, (0, 0, 0, 100), (0, 0, self.size, self.size))
            shadow = pygame.transform.rotate(shadow_surface, self.rotation)
            screen.blit(shadow, (self.current_pos[0] + x_offset - shadow.get_width()//2 + self.shadow_offset,
                               self.current_pos[1] - shadow.get_height()//2 + self.shadow_offset))
            
            # Draw dice with rounded corners
            dice_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(dice_surface, WHITE, (0, 0, self.size, self.size), border_radius=10)
            pygame.draw.rect(dice_surface, BLACK, (0, 0, self.size, self.size), 2, border_radius=10)
            
            # Draw larger dots
            dot_size = 8
            dot_positions = {
                1: [(self.size//2, self.size//2)],
                2: [(self.size//3, self.size//3), (2*self.size//3, 2*self.size//3)],
                3: [(self.size//3, self.size//3), (self.size//2, self.size//2), (2*self.size//3, 2*self.size//3)],
                4: [(self.size//3, self.size//3), (2*self.size//3, self.size//3),
                    (self.size//3, 2*self.size//3), (2*self.size//3, 2*self.size//3)],
                5: [(self.size//3, self.size//3), (2*self.size//3, self.size//3),
                    (self.size//2, self.size//2),
                    (self.size//3, 2*self.size//3), (2*self.size//3, 2*self.size//3)],
                6: [(self.size//3, self.size//3), (self.size//3, self.size//2), (self.size//3, 2*self.size//3),
                    (2*self.size//3, self.size//3), (2*self.size//3, self.size//2), (2*self.size//3, 2*self.size//3)]
            }
            
            for pos in dot_positions[value]:
                pygame.draw.circle(dice_surface, BLACK, pos, dot_size)
            
            # Rotate and draw dice
            rotated_dice = pygame.transform.rotate(dice_surface, self.rotation)
            screen.blit(rotated_dice, (self.current_pos[0] + x_offset - rotated_dice.get_width()//2,
                                     self.current_pos[1] - rotated_dice.get_height()//2))
            
            # Draw total during animation
            if self.rolling:
                total_text = FONT_BOLD.render(f"Rolling...", True, WHITE)
                screen.blit(total_text, (WINDOW_WIDTH//2 - total_text.get_width()//2, 
                                       WINDOW_HEIGHT//2 + self.size))
            elif self.animation_complete:
                total = sum(self.values)
                total_text = FONT_BOLD.render(f"Total: {total}", True, BLACK)
                screen.blit(total_text, (self.current_pos[0] - total_text.get_width()//2,
                                       self.current_pos[1] + self.size))

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.rolling:
                self.roll_dice()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
            elif event.key == pygame.K_b and not self.rolling:  # Buy property
                current_player = self.players[self.current_player]
                property = self.board.get_property_at_position(current_player.position)
                if property and isinstance(property, Property):
                    if property.owner is None and current_player.money >= property.price:
                        current_player.money -= property.price
                        property.owner = current_player
            elif event.key == pygame.K_s and not self.rolling:  # Sell property
                current_player = self.players[self.current_player]
                property = self.board.get_property_at_position(current_player.position)
                if property and isinstance(property, Property):
                    if property.owner == current_player:
                        current_player.money += property.price // 2  # Sell for half price
                        property.owner = None
        
        # Handle roll dice button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.roll_button.check_click(event.pos):
                if not self.rolling:
                    self.roll_dice()
                return
            
            # Check property buttons
            current_player = self.players[self.current_player]
            property = self.board.get_property_at_position(current_player.position)
            if property and isinstance(property, Property):
                if property.owner is None and self.buy_button.check_click(event.pos):
                    if current_player.money >= property.price:
                        current_player.money -= property.price
                        property.owner = current_player
                elif property.owner == current_player and self.sell_button.check_click(event.pos):
                    current_player.money += property.price // 2
                    property.owner = None
            
        if self.current_minigame:
            self.current_minigame.handle_event(event)

    def update_dice_roll(self):
        if not self.rolling:
            return
            
        # Update dice animation
        if self.dice.update():  # If dice animation is complete
            self.rolling = False
            current_player = self.players[self.current_player]
            total_roll = sum(self.dice.values)
            
            # Move player
            current_player.move(total_roll)
            
            # Add particle effects
            for i, value in enumerate(self.dice.values):
                x_offset = i * (self.dice.size + 40) - (self.dice.size + 40) // 2
                self.particle_system.add_particles(
                    self.dice.current_pos[0] + x_offset,
                    self.dice.current_pos[1],
                    current_player.color,
                    count=value * 3
                )
            
            # Check for special squares
            landed_property = self.board.get_property_at_position(current_player.position)
            if landed_property:
                if isinstance(landed_property, Property):
                    if landed_property.owner is None:  # Property is unowned
                        self.show_property_options(landed_property)
                    elif landed_property.owner != current_player:  # Pay rent
                        rent = landed_property.get_rent()
                        current_player.money -= rent
                        landed_property.owner.money += rent
                elif landed_property.type == "chance":
                    self.draw_chance_card()
                elif landed_property.type == "community_chest":
                    self.draw_community_chest_card()
            
            # Check for doubles
            if self.dice.values[0] == self.dice.values[1]:
                pass  # Player gets another turn
            else:
                self.next_player()

    def draw_chance_card(self):
        card = self.chance_deck.draw_card()
        self.show_card_animation("CHANCE", card)
        card.apply_effect(self.players[self.current_player])

    def draw_community_chest_card(self):
        card = self.community_chest_deck.draw_card()
        self.show_card_animation("COMMUNITY CHEST", card)
        card.apply_effect(self.players[self.current_player])

    def show_card_animation(self, card_type, card):
        # Create card surface
        card_width = 300
        card_height = 200
        card_surface = pygame.Surface((card_width, card_height))
        card_surface.fill(GOLD if card_type == "CHANCE" else BLUE)
        
        # Add card text
        title = FONT_BOLD.render(card_type, True, BLACK)
        description = FONT_REGULAR.render(card.description, True, BLACK)
        
        # Center text on card
        card_surface.blit(title, (card_width//2 - title.get_width()//2, 20))
        card_surface.blit(description, (card_width//2 - description.get_width()//2, 100))
        
        # Show card animation
        card_pos = (WINDOW_WIDTH//2 - card_width//2, WINDOW_HEIGHT//2 - card_height//2)
        self.screen.blit(card_surface, card_pos)
        pygame.display.flip()
        pygame.time.wait(2000)  # Show card for 2 seconds

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = FONT_REGULAR
        self.clicked = False
        self.click_time = 0
        self.click_delay = 0.5  # Delay between clicks in seconds
    
    def draw(self, screen):
        # Draw button shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect)
        
        # Draw button background
        pygame.draw.rect(screen, BUTTON_BG, self.rect)
        # Draw button border
        pygame.draw.rect(screen, self.current_color, self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.current_color = self.hover_color if self.is_hovered else self.color
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and not self.clicked:
                self.clicked = True
                self.click_time = pygame.time.get_ticks()
                return True
        return False
        
    def check_click(self, pos):
        current_time = pygame.time.get_ticks()
        if self.clicked and (current_time - self.click_time) / 1000 > self.click_delay:
            self.clicked = False
        return self.rect.collidepoint(pos) and not self.clicked

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Monopoly")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"  # menu, player_select, playing, auction, minigame
        self.board = Board()
        self.players = []
        self.current_player = 0
        self.dice_roll = None
        self.rolling = False
        self.roll_time = 0
        self.target_roll_time = 1.0
        self.current_minigame = None
        self.buy_button = None
        self.sell_button = None
        self.showing_property_options = False
        
        # Initialize card decks
        self.chance_deck = CardDeck(create_chance_cards())
        self.community_chest_deck = CardDeck(create_community_chest_cards())
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/PlayfairDisplaySemibold.ttf", 72)
            self.menu_font = pygame.font.Font("assets/fonts/PlayfairDisplay-VariableFont_wght.ttf", 36)
        except FileNotFoundError as e:
            print(f"Error loading fonts: {e}")
            print("Using system fonts as fallback")
            self.title_font = pygame.font.SysFont("arial", 72, bold=True)
            self.menu_font = pygame.font.SysFont("arial", 36)
        
        # Create menu buttons
        self.create_menu_buttons()
        
        self.dice = Dice()
        self.auction_property = None
        self.transition_alpha = 0
        self.transitioning = False
        self.any_player_moving = False
        self.particle_system = ParticleSystem()
        
        # Create menu buttons
        self.play_button = Button("Play Game", WINDOW_WIDTH//2 - 100, 300, 200, 50, PREMIUM_GREEN, PREMIUM_GREEN_HOVER)
        self.exit_button = Button("Exit Game", WINDOW_WIDTH//2 - 100, 400, 200, 50, RED, (200, 0, 0))
        
        # Create player selection buttons
        self.player_buttons = []
        for i in range(6):
            self.player_buttons.append(Button(
                str(i+1),  # text
                WINDOW_WIDTH//2 - 150 + i*50,  # x
                250,  # y
                40,  # width
                40,  # height
                BLUE,  # color
                LIGHT_BLUE  # hover_color
            ))
        
        # Create roll dice button
        self.roll_button = Button("Roll Dice", WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100, 120, 40, BLUE, LIGHT_BLUE)

    def create_menu_buttons(self):
        button_width = 200
        button_height = 50
        start_x = WINDOW_WIDTH//2 - button_width//2
        start_y = WINDOW_HEIGHT//2
        
        self.start_button = Button(
            "Start Game",  # text
            start_x,  # x
            start_y,  # y
            button_width,  # width
            button_height,  # height
            GREEN,  # color
            (0, 200, 0)  # hover_color
        )
        self.quit_button = Button(
            "Quit",  # text
            start_x,  # x
            start_y + 70,  # y
            button_width,  # width
            button_height,  # height
            RED,  # color
            (200, 0, 0)  # hover_color
        )
    
    def handle_menu_events(self, event):
        if self.play_button.handle_event(event):
            self.game_state = "player_select"
        elif self.exit_button.handle_event(event):
            self.running = False
    
    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.rolling:
                self.roll_dice()
            elif event.key == pygame.K_ESCAPE:
                if self.showing_property_options:
                    self.showing_property_options = False
                else:
                    self.game_state = "menu"
        
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check roll dice button
            if self.roll_button.check_click(event.pos):
                if not self.rolling:
                    self.roll_dice()
                return
            
            # Check property buttons if showing options
            if self.showing_property_options:
                current_player = self.players[self.current_player]
                property = self.board.get_property_at_position(current_player.position)
                
                if property and isinstance(property, Property):
                    if self.buy_button and property.owner is None:
                        if self.buy_button.check_click(event.pos):
                            if current_player.money >= property.price:
                                current_player.money -= property.price
                                property.owner = current_player
                    
                    elif self.sell_button and property.owner == current_player:
                        if self.sell_button.check_click(event.pos):
                            current_player.money += property.price // 2
                            property.owner = None
        
        if self.current_minigame:
            self.current_minigame.handle_event(event)
    
    def roll_dice(self):
        # Start dice roll animation
        self.rolling = True
        self.roll_time = 0
        self.dice.roll()  # Start dice animation
        
    def update_dice_roll(self):
        if not self.rolling:
            return
            
        # Update dice animation
        if self.dice.update():  # If dice animation is complete
            self.rolling = False
            current_player = self.players[self.current_player]
            total_roll = sum(self.dice.values)
            
            # Move player
            current_player.move(total_roll)
            
            # Add particle effects
            for i, value in enumerate(self.dice.values):
                x_offset = i * (self.dice.size + 40) - (self.dice.size + 40) // 2
                self.particle_system.add_particles(
                    self.dice.current_pos[0] + x_offset,
                    self.dice.current_pos[1],
                    current_player.color,
                    count=value * 3
                )
            
            # Check for special squares
            landed_property = self.board.get_property_at_position(current_player.position)
            if landed_property:
                if isinstance(landed_property, Property):
                    if landed_property.owner is None:  # Property is unowned
                        self.show_property_options(landed_property)
                    elif landed_property.owner != current_player:  # Pay rent
                        rent = landed_property.get_rent()
                        current_player.money -= rent
                        landed_property.owner.money += rent
                elif landed_property.type == "chance":
                    self.draw_chance_card()
                elif landed_property.type == "community_chest":
                    self.draw_community_chest_card()
            
            # Check for doubles
            if self.dice.values[0] == self.dice.values[1]:
                pass  # Player gets another turn
            else:
                self.next_player()
    
    def start_minigame(self, game_type):
        if game_type == "dice_roll":
            self.current_minigame = DiceRollGame(self.screen, self.players[self.current_player])
            self.current_minigame.start()
        elif game_type == "property_auction":
            property = self.board.get_property_at_position(self.players[self.current_player].position)
            if property:
                self.current_minigame = PropertyAuction(self.screen, self.players[self.current_player], property)
                self.current_minigame.start()
        elif game_type == "jail_escape":
            self.current_minigame = JailEscape(self.screen, self.players[self.current_player])
            self.current_minigame.start()
    
    def update(self):
        # Update dice
        self.dice.update()
        self.handle_transition()
        self.particle_system.update()
        
        if self.game_state == "playing":
            # Update current player
            self.players[self.current_player].update(
                (WINDOW_WIDTH - BOARD_SIZE)//2,
                (WINDOW_HEIGHT - BOARD_SIZE)//2,
                BOARD_SIZE
            )
            
            # Update dice roll
            self.update_dice_roll()
            
            # Update minigame if active
            if self.current_minigame:
                self.current_minigame.update()
                if not self.current_minigame.running:
                    self.current_minigame = None
                    self.next_player()
        elif self.game_state == "menu":
            # Update menu
            self.draw_menu()
        elif self.game_state == "player_select":
            # Update player selection
            self.draw_player_select()

    def draw(self):
        self.screen.fill(WHITE)
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "player_select":
            self.draw_player_select()
        elif self.game_state == "playing":
            self.draw_game()
            # Draw dice and particles
            self.dice.draw(self.screen)
            self.particle_system.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Draw background gradient with maroon tint
        for y in range(WINDOW_HEIGHT):
            color = (
                int(128 + 127 * (1 - y/WINDOW_HEIGHT)),  # Maroon base
                int(0 + 255 * (1 - y/WINDOW_HEIGHT)),
                int(0 + 255 * (1 - y/WINDOW_HEIGHT))
            )
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
        
        # Draw title with shadow and glow
        title = self.title_font.render("MONOPOLY", True, BLACK)
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2 + 2, 102))
        title = self.title_font.render("MONOPOLY", True, GOLD)
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
        
        # Draw decorative elements with maroon tint
        for i in range(5):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            pygame.draw.circle(self.screen, (128, 0, 0, 30), (x, y), 2)
        
        # Draw buttons
        self.play_button.draw(self.screen)
        self.exit_button.draw(self.screen)
    
    def draw_player_select(self):
        # Draw background gradient
        for y in range(WINDOW_HEIGHT):
            color = (
                int(200 * (1 - y/WINDOW_HEIGHT)),
                int(200 * (1 - y/WINDOW_HEIGHT)),
                int(255 * (1 - y/WINDOW_HEIGHT))
            )
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
        
        # Draw title with shadow
        title = self.title_font.render("Select Players", True, BLACK)
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2 + 2, 102))
        title = self.title_font.render("Select Players", True, BLUE)
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
        
        # Draw subtitle
        subtitle = FONT_REGULAR.render("Choose number of players (1-6):", True, BLACK)
        self.screen.blit(subtitle, (WINDOW_WIDTH//2 - subtitle.get_width()//2, 200))
        
        # Draw player buttons
        for button in self.player_buttons:
            button.draw(self.screen)
    
    def draw_game(self):
        # Draw board
        board_size = 800
        board_x = (self.screen.get_width() - board_size) // 2
        board_y = (self.screen.get_height() - board_size) // 2
        
        # Draw board shadow
        shadow_rect = pygame.Rect(board_x + 4, board_y + 4, board_size, board_size)
        pygame.draw.rect(self.screen, BOARD_SHADOW, shadow_rect)
        
        # Draw board background with gradient
        for y in range(board_y, board_y + board_size):
            color = (
                int(245 + 10 * (1 - (y - board_y)/board_size)),
                int(245 + 10 * (1 - (y - board_y)/board_size)),
                int(245 + 10 * (1 - (y - board_y)/board_size))
            )
            pygame.draw.line(self.screen, color, (board_x, y), (board_x + board_size, y))
        
        # Draw board border with shadow
        pygame.draw.rect(self.screen, BOARD_BORDER, (board_x, board_y, board_size, board_size), 2)
        
        # Draw properties
        self.board.draw(self.screen, self.players[self.current_player], self.dice.values)
        
        # Update and draw players
        self.any_player_moving = False
        for player in self.players:
            player.update(board_x, board_y, board_size)
            if player.moving:
                self.any_player_moving = True
            player.draw(self.screen)
        
        # Draw info panel with shadow
        current = self.players[self.current_player]
        info_text = f"Current Player: {current.name} (${current.money})"
        text = FONT_REGULAR.render(info_text, True, BLACK)
        text_rect = text.get_rect()
        text_rect.x = 10
        text_rect.y = 10
        panel_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 40), panel_rect.inflate(2, 2))
        pygame.draw.rect(self.screen, INFO_BG, panel_rect)
        self.screen.blit(text, text_rect)
        
        # Draw roll dice button
        self.roll_button.draw(self.screen)
        
        # Draw dice during animation or briefly after roll
        current_time = pygame.time.get_ticks()
        if self.rolling or (self.dice.animation_complete and current_time - self.roll_time < 2000):
            self.dice.draw(self.screen)
        
        # Draw minigame if active
        if self.current_minigame:
            self.current_minigame.draw()
        
        # Draw property options if showing
        if self.showing_property_options:
            current_player = self.players[self.current_player]
            property = self.board.get_property_at_position(current_player.position)
            if property and isinstance(property, Property):
                self.show_property_options(property)

    def handle_transition(self):
        if self.transitioning:
            self.transition_alpha += 5
            if self.transition_alpha >= 255:
                self.transitioning = False
                self.transition_alpha = 0
        else:
            self.transition_alpha = 0

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)
        self.dice_roll = None
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.game_state == "menu":
                    self.handle_menu_events(event)
                elif self.game_state == "player_select":
                    for i, button in enumerate(self.player_buttons):
                        if button.handle_event(event):
                            self.setup_players(i+1)
                            self.game_state = "playing"  # Explicitly set game state
                            break  # Break after setting up players
                elif self.game_state == "playing":
                    self.handle_game_events(event)
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def setup_players(self, num_players):
        colors = [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE]
        self.players = []
        for i in range(num_players):
            self.players.append(Player(f"Player {i+1}", colors[i], 500))
        self.current_player = 0
        self.rolling = False  # Reset rolling state
        self.dice_roll = [1, 1]  # Initialize with default dice values
        self.current_minigame = None  # Reset minigame state
        # Initialize board
        self.board = Board()
        # Initialize dice
        self.dice = Dice()
        # Initialize particle system
        self.particle_system = ParticleSystem()

    def show_property_options(self, property):
        self.showing_property_options = True
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Create property info surface with shadow
        info_width = 400
        info_height = 300
        info_surface = pygame.Surface((info_width, info_height))
        info_surface.fill(WHITE)
        
        # Add property information
        title = FONT_BOLD.render(property.name, True, BLACK)
        price = FONT_REGULAR.render(f"Price: ${property.price}", True, BLACK)
        rent = FONT_REGULAR.render(f"Rent: ${property.get_rent()}", True, BLACK)
        current_player = self.players[self.current_player]
        player_money = FONT_REGULAR.render(f"Your Money: ${current_player.money}", True, BLACK)
        
        # Center text on info surface
        info_surface.blit(title, (info_width//2 - title.get_width()//2, 40))
        info_surface.blit(price, (info_width//2 - price.get_width()//2, 100))
        info_surface.blit(rent, (info_width//2 - rent.get_width()//2, 140))
        info_surface.blit(player_money, (info_width//2 - player_money.get_width()//2, 180))
        
        # Add shadow to info surface
        info_shadow = pygame.Surface((info_width + 4, info_height + 4))
        info_shadow.fill((0, 0, 0, 40))
        
        # Position info box in center of screen
        info_pos = (WINDOW_WIDTH//2 - info_width//2, WINDOW_HEIGHT//2 - info_height//2)
        self.screen.blit(info_shadow, (info_pos[0] + 2, info_pos[1] + 2))
        self.screen.blit(info_surface, info_pos)
        
        # Add buttons with proper spacing
        button_y = info_pos[1] + info_height - 80
        
        # Create buttons based on property state
        if property.owner is None and current_player.money >= property.price:
            self.buy_button = Button("Buy Property", WINDOW_WIDTH//2 - 150, button_y, 300, 50, GREEN, (0, 200, 0))
            self.buy_button.draw(self.screen)
        elif property.owner == current_player:
            self.sell_button = Button("Sell Property", WINDOW_WIDTH//2 - 150, button_y, 300, 50, RED, (200, 0, 0))
            self.sell_button.draw(self.screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run() 