import pygame
import random
import math

class MiniGame:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.running = False
        self.result = None
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.particles = []
        
    def create_particle(self, x, y, color):
        self.particles.append({
            'x': x,
            'y': y,
            'color': color,
            'size': random.randint(2, 5),
            'speed_x': random.uniform(-2, 2),
            'speed_y': random.uniform(-2, 2),
            'life': 1.0
        })
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['life'] -= 0.02
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self):
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            color = (*particle['color'], alpha)
            pygame.draw.circle(self.screen, color, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    def draw_result(self, text, color):
        font = pygame.font.Font(None, 48)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, 
                                                 self.screen.get_height()//2))
        self.screen.blit(text_surface, text_rect)
        
        # Draw continue prompt
        prompt_font = pygame.font.Font(None, 24)
        prompt = prompt_font.render("Press SPACE to continue", True, (255, 255, 255))
        prompt_rect = prompt.get_rect(center=(self.screen.get_width()//2, 
                                            self.screen.get_height()//2 + 50))
        self.screen.blit(prompt, prompt_rect)

class DiceRollGame(MiniGame):
    def __init__(self, screen, player):
        super().__init__(screen, player)
        self.dice_values = [1, 1]
        self.rolling = False
        self.roll_speed = 0.1
        self.roll_time = 0
        self.target_roll_time = 2.0
        self.dice_images = []
        self.load_dice_images()
    
    def load_dice_images(self):
        for i in range(1, 7):
            img = pygame.image.load(f"assets/images/dice{i}.png")
            img = pygame.transform.scale(img, (60, 60))
            self.dice_images.append(img)
    
    def start(self):
        self.running = True
        self.rolling = True
        self.roll_time = 0
        self.result = None
    
    def update(self):
        if not self.running:
            return
            
        self.animation_frame += self.animation_speed
        self.update_particles()
        
        if self.rolling:
            self.roll_time += self.roll_speed
            if self.roll_time >= self.target_roll_time:
                self.rolling = False
                self.dice_values = [random.randint(1, 6), random.randint(1, 6)]
                self.result = sum(self.dice_values)
                # Create particles for celebration
                for _ in range(20):
                    self.create_particle(
                        random.randint(0, self.screen.get_width()),
                        random.randint(0, self.screen.get_height()),
                        (255, 215, 0)
                    )
    
    def draw(self):
        if not self.running:
            return
            
        # Draw background
        self.screen.fill((0, 0, 0))
        
        # Draw dice
        dice_x = self.screen.get_width()//2 - 70
        dice_y = self.screen.get_height()//2 - 30
        
        if self.rolling:
            # Animate rolling dice
            for i in range(2):
                dice_value = random.randint(1, 6)
                self.screen.blit(self.dice_images[dice_value-1], 
                               (dice_x + i*80, dice_y))
        else:
            # Draw final dice values
            for i, value in enumerate(self.dice_values):
                self.screen.blit(self.dice_images[value-1], 
                               (dice_x + i*80, dice_y))
        
        # Draw particles
        self.draw_particles()
        
        # Draw result if available
        if self.result:
            self.draw_result(f"Rolled: {self.result}", (255, 215, 0))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.result:
                self.running = False
                self.player.receive_money(self.result * 10)  # Reward based on roll

class PropertyAuction(MiniGame):
    def __init__(self, screen, player, property):
        super().__init__(screen, player)
        self.property = property
        self.current_bid = property.price // 2
        self.min_bid = property.price // 4
        self.bid_increment = 10
        self.time_left = 10
        self.bidding = True
        self.winner = None
        self.font = pygame.font.Font(None, 36)
    
    def start(self):
        self.running = True
        self.bidding = True
        self.time_left = 10
        self.winner = None
    
    def update(self):
        if not self.running:
            return
            
        self.animation_frame += self.animation_speed
        self.update_particles()
        
        if self.bidding:
            self.time_left -= 0.016  # Approximately 60 FPS
            if self.time_left <= 0:
                self.bidding = False
                self.winner = self.player  # Default to current player if no other bids
    
    def draw(self):
        if not self.running:
            return
            
        # Draw background
        self.screen.fill((0, 0, 0))
        
        # Draw property info
        property_text = self.font.render(self.property.name, True, (255, 255, 255))
        price_text = self.font.render(f"Current Bid: ${self.current_bid}", True, (255, 215, 0))
        time_text = self.font.render(f"Time Left: {int(self.time_left)}s", True, (255, 255, 255))
        
        self.screen.blit(property_text, 
                        (self.screen.get_width()//2 - property_text.get_width()//2, 100))
        self.screen.blit(price_text, 
                        (self.screen.get_width()//2 - price_text.get_width()//2, 150))
        self.screen.blit(time_text, 
                        (self.screen.get_width()//2 - time_text.get_width()//2, 200))
        
        # Draw bidding controls
        if self.bidding:
            up_text = self.font.render("Press UP to bid higher", True, (255, 255, 255))
            down_text = self.font.render("Press DOWN to bid lower", True, (255, 255, 255))
            self.screen.blit(up_text, 
                           (self.screen.get_width()//2 - up_text.get_width()//2, 300))
            self.screen.blit(down_text, 
                           (self.screen.get_width()//2 - down_text.get_width()//2, 350))
        
        # Draw particles
        self.draw_particles()
        
        # Draw result if bidding is over
        if not self.bidding:
            self.draw_result(f"Property sold to {self.winner.name}!", (255, 215, 0))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.bidding:
                self.running = False
                if self.winner:
                    self.winner.buy_property(self.property)
            elif event.key == pygame.K_UP and self.bidding:
                self.current_bid += self.bid_increment
                self.create_particle(
                    random.randint(0, self.screen.get_width()),
                    random.randint(0, self.screen.get_height()),
                    (0, 255, 0)
                )
            elif event.key == pygame.K_DOWN and self.bidding:
                if self.current_bid - self.bid_increment >= self.min_bid:
                    self.current_bid -= self.bid_increment
                    self.create_particle(
                        random.randint(0, self.screen.get_width()),
                        random.randint(0, self.screen.get_height()),
                        (255, 0, 0)
                    )

class JailEscape(MiniGame):
    def __init__(self, screen, player):
        super().__init__(screen, player)
        self.bars = []
        self.setup_bars()
        self.key_position = (random.randint(100, 700), random.randint(100, 500))
        self.key_collected = False
        self.time_left = 30
        self.font = pygame.font.Font(None, 36)
    
    def setup_bars(self):
        # Create vertical bars
        for i in range(5):
            x = 200 + i * 100
            self.bars.append(pygame.Rect(x, 100, 20, 400))
        
        # Create horizontal bars
        for i in range(3):
            y = 150 + i * 100
            self.bars.append(pygame.Rect(100, y, 600, 20))
    
    def start(self):
        self.running = True
        self.key_collected = False
        self.time_left = 30
        self.key_position = (random.randint(100, 700), random.randint(100, 500))
    
    def update(self):
        if not self.running:
            return
            
        self.animation_frame += self.animation_speed
        self.update_particles()
        
        if not self.key_collected:
            self.time_left -= 0.016  # Approximately 60 FPS
            if self.time_left <= 0:
                self.running = False
    
    def draw(self):
        if not self.running:
            return
            
        # Draw background
        self.screen.fill((0, 0, 0))
        
        # Draw jail bars
        for bar in self.bars:
            pygame.draw.rect(self.screen, (128, 128, 128), bar)
        
        # Draw key
        if not self.key_collected:
            pygame.draw.circle(self.screen, (255, 215, 0), 
                             (int(self.key_position[0]), int(self.key_position[1])), 15)
        
        # Draw time
        time_text = self.font.render(f"Time Left: {int(self.time_left)}s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))
        
        # Draw particles
        self.draw_particles()
        
        # Draw result if key is collected
        if self.key_collected:
            self.draw_result("You found the key!", (255, 215, 0))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.key_collected:
                self.running = False
                self.player.use_jail_card()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.key_collected:
                # Check if clicked on key
                mouse_pos = pygame.mouse.get_pos()
                distance = math.sqrt((mouse_pos[0] - self.key_position[0])**2 + 
                                  (mouse_pos[1] - self.key_position[1])**2)
                if distance < 15:
                    self.key_collected = True
                    self.create_particle(
                        self.key_position[0],
                        self.key_position[1],
                        (255, 215, 0)
                    ) 