import random

class Character:
    blue = 0
    red = 0
    green = 0
    white = 0

    def __init__(self, id, name) -> None:
        self.name = name
        self.id = id

    def addCrystal(self,color):
        if color == "blue":
            self.blue += 1
        elif color == "red":
            self.red += 1
        elif color == "green":
            self.green += 1
        elif color == "white":
            self.white += 1
        else:
            pass

    def listCrystals(self):
        return f"Blue: {self.blue}  Red: {self.red}  Green: {self.green}  White: {self.white}"

class PlayerCharacter(Character):
    location = (0,0)
    deck = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    def __init__(self, id, name) -> None:
        super().__init__(id, name)
        if id == "1":
            self.deck[2] = 17
            self.deck[6] = 16 
        elif id == "2":
            self.deck[15] = 19
            self.deck[0] = 18
        else:
            pass

class DummyCharacter(Character):
    crystals = {"1":"bbr","2":"rrw","3":"ggb","4":"wwg","5":"wwb","6":"rrg","7":"bbg"}
    deck = ["b","b","b","b","r","r","r","r","g","g","g","g","w","w","w","w"]

    def __init__(self, id, name) -> None:
        super().__init__(id, name)
        starting = self.crystals[id]
        for letter in starting:
            if letter == "b":
                self.blue += 1
            elif letter == "r":
                self.red += 1
            elif letter == "g":
                self.green += 1
            else:
                self.white += 1
        random.shuffle(self.deck)
    
    def addAA(self,color):
        if color == "blue":
            self.deck.append("b")
        elif color == "red":
            self.deck.append("r")
        elif color == "green":
            self.deck.append("g")
        elif color == "white":
            self.deck.append("w")
        else:
            pass