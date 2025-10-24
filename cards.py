import random
import pygame

class Card:
    def __init__(self, text, action):
        self.text = text
        self.action = action
        self.image = None
        self.load_image()
    
    def load_image(self):
        try:
            self.image = pygame.image.load(f"assets/images/cards/{self.text.lower().replace(' ', '_')}.png")
            self.image = pygame.transform.scale(self.image, (200, 120))
        except:
            self.image = None
    
    def draw(self, screen, x, y):
        if self.image:
            screen.blit(self.image, (x, y))
        else:
            # Draw card background
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 200, 120))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 200, 120), 2)
            
            # Draw card text
            font = pygame.font.Font(None, 20)
            words = self.text.split()
            for i, word in enumerate(words):
                text = font.render(word, True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + 100, y + 30 + i*20))
                screen.blit(text, text_rect)

class CardDeck:
    def __init__(self, cards):
        self.cards = cards
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw_card(self):
        if not self.cards:
            self.shuffle()
        return self.cards.pop()
    
    def add_card(self, card):
        self.cards.append(card)

def create_chance_cards():
    return [
        Card("Advance to Go", lambda player: player.move_to(0)),
        Card("Advance to Illinois Avenue", lambda player: player.move_to(24)),
        Card("Advance to St. Charles Place", lambda player: player.move_to(11)),
        Card("Advance to nearest Utility", lambda player: player.move_to_nearest_utility()),
        Card("Advance to nearest Railroad", lambda player: player.move_to_nearest_railroad()),
        Card("Bank pays you dividend of $50", lambda player: player.receive_money(50)),
        Card("Get Out of Jail Free", lambda player: player.add_jail_card()),
        Card("Go Back 3 Spaces", lambda player: player.move(-3)),
        Card("Go to Jail", lambda player: player.go_to_jail()),
        Card("Make general repairs on all your property", lambda player: player.pay_repairs()),
        Card("Pay poor tax of $15", lambda player: player.pay_money(15)),
        Card("Take a trip to Reading Railroad", lambda player: player.move_to(5)),
        Card("Take a walk on the Boardwalk", lambda player: player.move_to(39)),
        Card("You have been elected Chairman of the Board", lambda player: player.pay_each_player(50)),
        Card("Your building loan matures", lambda player: player.receive_money(150)),
        Card("You have won a crossword competition", lambda player: player.receive_money(100))
    ]

def create_community_chest_cards():
    return [
        Card("Advance to Go", lambda player: player.move_to(0)),
        Card("Bank error in your favor", lambda player: player.receive_money(200)),
        Card("Doctor's fee", lambda player: player.pay_money(50)),
        Card("From sale of stock you get $45", lambda player: player.receive_money(45)),
        Card("Get Out of Jail Free", lambda player: player.add_jail_card()),
        Card("Go to Jail", lambda player: player.go_to_jail()),
        Card("Grand Opera Night", lambda player: player.receive_money(50)),
        Card("Holiday Fund matures", lambda player: player.receive_money(100)),
        Card("Income tax refund", lambda player: player.receive_money(20)),
        Card("Life insurance matures", lambda player: player.receive_money(100)),
        Card("Pay hospital fees of $100", lambda player: player.pay_money(100)),
        Card("Pay school fees of $50", lambda player: player.pay_money(50)),
        Card("Receive $25 consultancy fee", lambda player: player.receive_money(25)),
        Card("You are assessed for street repairs", lambda player: player.pay_repairs()),
        Card("You have won second prize in a beauty contest", lambda player: player.receive_money(10)),
        Card("You inherit $100", lambda player: player.receive_money(100))
    ] 