
from zuege import moeglicheZuege


class Feld:

    moeglicheZuege = []
    dZügePlayer = [[-1,1],[-1,-1]]
    dZügeComputer = [[1,-1],[1,1]]

    def __init__(self):
        self.white = False
        self.black = False
        self.player = False
        self.computer = False
        self.dame = False
        self.clicked = False
        self.Nachbar = False

    #Methoden zur Abfrage des Status
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

    def isNachbar(self):
        return self.Nachbar

    #Methoden zum setzen eines Status
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

    def makeNachbar(self,bool):
        self.Nachbar = bool

    #Mögliche Züge berechnen
    def getZüge(self):
        return self.moeglicheZuege

    def zügeBerechnen(self, feld, player, y, x):

        self.moeglicheZuege = []

        if self.isPlayer() and player:
            #Für normale Steine
            if not self.isDame():
                #Alle Möglichkeiten durchgehen
                for j,i in self.dZügePlayer:
                    j2 = j*2
                    i2 = i*2
                    #Auf Existenz prüfen
                    if not (y+j < 0 or x+i < 0 or x+i > 7):
                        #Auf leere des nächsten Feldes prüfen
                        if not feld[y+j][x+i].isPlayer() and not feld[y+j][x+i].isComputer():
                            self.moeglicheZuege.append((feld[y+j][x+i],None))
                    #Auf Gegner prüfen und leere des dahinter liegenden Feldes
                    if not(y+j2 < 0 or x+i2 < 0 or x+i2 > 7):
                        if feld[y+j][x+i].isComputer() and not feld[y+j2][x+i2].isPlayer() and not feld[y+j2][x+i2].isComputer():
                            self.moeglicheZuege.append((feld[y+j2][x+i2],feld[y+j][x+i]))

            elif self.isDame():
                pass

        elif self.isComputer() and not player:
            #Für normale Steine
            if not self.isDame():
                #Alle Möglichkeiten durchgehen
                for j,i in self.dZügeComputer:
                    j2 = j*2
                    i2 = i*2
                    #Auf Existenz prüfen
                    if not(y+j > 7 or x+i < 0 or x+i > 7):
                        #Auf leere des nächsten Feldes prüfen
                        if not feld[y+j][x+i].isPlayer() and not feld[y+j][x+i].isComputer():
                            self.moeglicheZuege.append((feld[y+j][x+i],None))
                    #Auf Gegner prüfen und leere des dahinter liegenden Feldes
                    if not(y+j2 > 7 or x+i2 < 0 or x+i2 > 7):
                        if feld[y+j][x+i].isPlayer() and not feld[y+j2][x+i2].isPlayer() and not feld[y+j2][x+i2].isComputer():
                            self.moeglicheZuege.append((feld[y+j2][x+i2],feld[y+j][x+i]))
            elif self.isDame():
                pass
    