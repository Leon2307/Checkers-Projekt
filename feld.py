
class Feld:

    moeglicheZuege = []

    def __init__(self):
        self.white = False
        self.black = False
        self.player = False
        self.computer = False
        self.focused = False

    #Methoden zur Abfrage des Status
    def isWhite(self):
        return self.white

    def isBlack(self):
        return self.black
    
    def isPlayer(self):
        return self.player
    
    def isComputer(self):
        return self.computer

    def isFocused(self):
        return self.focused

    #Methoden zum setzen eines Status
    def makeWhite(self, bool):
        self.white = bool

    def makeBlack(self, bool):
        self.black = bool

    def makePlayer(self, bool):
        self.player = bool

    def makeComputer(self, bool):
        self.computer = bool

    def makeFocused(self, bool):
        self.focused = bool

    #Mögliche Züge berechnen
    def zügeBerechnen(self, feld):
        pass
    