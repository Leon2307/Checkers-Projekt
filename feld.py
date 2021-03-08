
import zuege


class Feld:

    # [Feld zum hinbewegen, (Felder die rausgeworfen werden), Eckfeld über das gegangen wird]
    moeglicheZuege = []

    dZügePlayer = [[-1, 1], [-1, -1]]
    dZügeComputer = [[1, -1], [1, 1]]
    dZügeDame = [[-1, 1], [-1, -1], [1, -1], [1, 1]]

    def __init__(self, y, x):
        self.Y = y
        self.X = x
        self.white = False
        self.black = False
        self.player = False
        self.computer = False
        self.dame = False
        self.clicked = False
        self.moeglicherZug = False

    # Methoden zur Abfrage des Status
    def isWhite(self):
        return self.white

    def isBlack(self):
        return self.black

    def isPlayer(self):
        return self.player

    def isComputer(self):
        return self.computer

    def isDame(self):
        return self.dame

    def isClicked(self):
        return self.clicked

    def isMoeglicherZug(self):
        return self.moeglicherZug

    def getPunkte(self, index):

        # Wenn ein Eckpunkt enthalten ist werden 3, ansonsten 2 Punkte übermittelt
        if self.moeglicheZuege[index][2] != [None]:
            punkte = [self.getPosition()]
            for pos in self.moeglicheZuege[index][2]:
                punkte.append(pos.getPosition())
            punkte.append(self.moeglicheZuege[index][0].getPosition())
            return punkte
        return (self.getPosition(), self.moeglicheZuege[index][0].getPosition())

    def getPosition(self):
        return (self.X, self.Y)

    # Methoden zum setzen eines Status
    def makeWhite(self, bool):
        self.white = bool

    def makeBlack(self, bool):
        self.black = bool

    def makePlayer(self, bool):
        self.player = bool

    def makeComputer(self, bool):
        self.computer = bool

    def makeDame(self, bool):
        self.dame = bool

    def makeClicked(self, bool):
        self.clicked = bool

    def makeMoeglicherZug(self, bool):
        self.moeglicherZug = bool

    # Mögliche Züge berechnen
    def getZüge(self):
        return self.moeglicheZuege

    def zügeBerechnen(self, feld, player, y, x):

        self.moeglicheZuege = []

        if self.isPlayer() and player:

            # Für normale Steine
            if not self.isDame():
                moegZuege = zuege.zugzwang(feld, player, y, x, None, None, 0)
                if moegZuege != []:
                    self.moeglicheZuege = moegZuege

            # Für Dame
            elif self.isDame():
                moegZuege = zuege.zugzwangDame(
                    y, x, player, feld, None, None, 0, None)
                if moegZuege != []:
                    self.moeglicheZuege = moegZuege

        elif self.isComputer() and not player:

            # Für normale Steine
            if not self.isDame():
                moegZuege = zuege.zugzwang(feld, player, y, x, None, None, 0)
                if moegZuege != []:
                    self.moeglicheZuege = moegZuege

            # Für Dame
            elif self.isDame():
                moegZuege = zuege.zugzwangDame(
                    y, x, player, feld, None, None, 0, None)
                if moegZuege != []:
                    self.moeglicheZuege = moegZuege
