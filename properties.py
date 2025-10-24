class Property:
    def __init__(self, name, price, color, position):
        self.name = name
        self.price = price
        self.color = color
        self.position = position
        self.owner = None
        self.houses = 0
        self.hotel = False
        self.mortgaged = False
        
    def get_rent(self):
        if not self.owner or self.mortgaged:
            return 0
            
        base_rent = self.price // 10  # Base rent is 10% of property price
        
        if self.hotel:
            return base_rent * 5
        elif self.houses > 0:
            return base_rent * (self.houses + 1)
        else:
            return base_rent
    
    def can_build_house(self):
        if not self.owner or self.mortgaged or self.hotel:
            return False
        return self.houses < 4
    
    def can_build_hotel(self):
        if not self.owner or self.mortgaged:
            return False
        return self.houses == 4 and not self.hotel
    
    def build_house(self):
        if self.can_build_house():
            self.houses += 1
            return True
        return False
    
    def build_hotel(self):
        if self.can_build_hotel():
            self.houses = 0
            self.hotel = True
            return True
        return False
    
    def mortgage(self):
        if not self.mortgaged and not (self.houses > 0 or self.hotel):
            self.mortgaged = True
            return self.price // 2
        return 0
    
    def unmortgage(self):
        if self.mortgaged:
            self.mortgaged = False
            return (self.price // 2) * 1.1  # 10% interest
        return 0
    
    def get_mortgage_value(self):
        return self.price // 2
    
    def get_unmortgage_cost(self):
        return (self.price // 2) * 1.1  # 10% interest 