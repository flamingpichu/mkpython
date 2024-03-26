import random
import json
import operator
import character

class Game:
    #countryTiles = list(range(2,16))
    countryTiles = list(range(2,6))
    coreTiles = list(range(16,22))
    cityTiles = list(range(22,26))
    characters = {"1":"Tovak","2":"Arythea","3":"Goldyx","4":"Norowas","5":"Wolfhawk","6":"Krang","7":"Braevelar"}
    playerCharacters = []

    def __init__(self, mapShape, numPlayer, country, core, city) -> None:
        self.numPlayer = numPlayer
        self.tileDeck = self.generateTileDeck(country,core,city)
        setupTiles = [0]
        if mapShape == "Wedge":
            setupTiles.append(self.tileDeck.pop(0))
            setupTiles.append(self.tileDeck.pop(0))
        else:
            pass
        self.map = Map(mapShape, setupTiles)

        while len(self.playerCharacters) < numPlayer:
            print(self.characters)
            characterId = input()
            if characterId in self.characters:
                selectedCharacter = self.characters.pop(characterId)
                print(f"{selectedCharacter}")
                self.playerCharacters.append(character.PlayerCharacter(characterId,selectedCharacter))
                print(self.characters)
            else:
                print("invalid character")
        dummyId = random.choice(list(self.characters.keys()))
        self.dummy = character.DummyCharacter(dummyId,self.characters[dummyId])

    def generateTileDeck(self, country, core, city):
        brownTiles = random.sample(self.coreTiles,core) + random.sample(self.cityTiles,city)
        random.shuffle(brownTiles)
        greenTiles = random.sample(self.countryTiles,country)
        return greenTiles + brownTiles

    def showConfig(self):
        return f"Map Shape: {self.map.shape}\nNumber of Players: {self.numPlayer}"
    
    def showTileDeck(self):
        return f"Tiles Remaining: {len(self.tileDeck)}"
    
    def isNextTileBrown(self) -> bool:
        return self.tileDeck[0] > 15

class Map:
    map = {}
    maxY = 1
    centers = []
    tileFile = "g:/Documents/PersonalProjects/MageKnight/data/tiles.json"

    def __init__(self, shape, tiles) -> None:
        self.shape = shape
        f = open(self.tileFile)
        tileData = json.load(f)
        initialCenters = [(0,0)]
        if shape == "Wedge":
            initialCenters.append((1,2))
            initialCenters.append((3,-1))
        else:
            pass
        for i in range(len(tiles)):
            self.addTile(tileData[tiles[i]]["layout"],initialCenters[i])
        f.close()

    def isNewCenter(self,hex) -> bool:
        pass
    
    def addTile(self,tileData,centerHex,orientation = "default"):
        hexTransform = [(0,0),(-1,0),(-1,1),(0,1),(1,0),(1,-1),(0,-1)]
        for i in range(len(hexTransform)):
            coords = tuple(map(operator.add, centerHex, hexTransform[i]))
            if coords[1] == self.maxY:
                self.maxY = coords[1] + 1
            self.map[coords] = Hex(coords[0],coords[1],tileData[i]["terrain"],tileData[i]["element"])
        self.centers.append(centerHex)
        self.map = dict(sorted(self.map.items(), key=operator.itemgetter(1), reverse=True))

    def showMap(self):
        mapString = ""
        currY = self.maxY
        for hex in self.map.values():
            if currY == hex.y:
                mapString += f"   {hex.getMapString()}"
            else:
                currY = hex.y
                mapString += f"\n\n{self.offset(hex)}{hex.getMapString()}"
        return mapString
    
    def offset(self,hex):
        whitespace = "   "
        steps = 2*hex.x + hex.y +2
        return whitespace * steps
    
    def explore(self,hex):
        hexTransform = [(0,0),(-1,0),(-1,1),(0,1),(1,0),(1,-1),(0,-1)]
        for i in range(len(hexTransform)):
            coords = tuple(map(operator.add, hex, hexTransform[i]))
            if coords not in self.map:
                if self.isNewCenter(coords):
                    pass
    
class Hex:
    unsafeElements = ["keep","tower","orc","dragon","city"]
    terrainMap = {"plain":"p","forest":"f","desert":"d","hill":"h","mountain":"m","lake":"l","waste":"w","swamp":"s","none":"x"}
    elementMap = {"none":"--","village":"VL","church":"MO","keep":"KP","tower":"MT","orc":"OR","dragon":"DG",
                  "mineW":"MW","mineR":"MR","mineG":"MG","mineB":"MB","portal":"PO","glade":"GL"}

    def __init__(self, x, y, terrain, element) -> None:
        self.x = x
        self.y = y
        self.z = 0-x-y
        self.terrain = terrain
        self.element = element
        self.conquered = False
        self.safe = element not in self.unsafeElements
        self.occupied = False

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and -self.x-self.y == -other.x-other.y
    
    def __lt__(self, other) -> bool:
        return self.y < other.y or self.y == other.y and self.x > other.x
    
    def __le__(self, other) -> bool:
        pass

    def __gt__(self, other) -> bool:
        pass

    def __ge__(self, other) -> bool:
        pass

    def getMapString(self):
        return f"{self.terrainMap[self.terrain] + self.elementMap[self.element]}"
    
    def getNeighbours(self):
        hexTransform = [(-1,0),(-1,1),(0,1),(1,0),(1,-1),(0,-1)]
        neighbours = []
        for i in range(len(hexTransform)):
            neighbours.append(tuple(map(operator.add, (self.x, self.y), hexTransform[i])))
        return neighbours
         
def main():
    game = Game("Wedge",1,2,2,2)
    print(game.showConfig())
    print(game.map.showMap())
    print(game.isNextTileBrown())
    print(game.map.centers)
    print(f"Dummy: {game.dummy.name}")
    print(game.dummy.listCrystals())
    print(game.dummy.deck)
    print(game.playerCharacters[0].listCrystals())

if __name__ == "__main__":
    main()