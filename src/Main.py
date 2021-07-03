from NetworkAPI import Network
import BingoGame
import random
from collections import namedtuple

Menus = namedtuple("MenuType", ["Main", "Randomize", "Host", "Connect", "Exit"])
MenuType = Menus(0, 1, 2, 3, 4)
Chances = namedtuple("ChanceType", ["Your", "Opponent"])
ChanceType = Chances(0, 1)


class GameDriver(object):
    def __init__(self):
        self.bingoBoard = BingoGame.Bingo(5)

    def showMenu(self, menuType=MenuType.Main):
        if menuType == MenuType.Main:
            print("1. Randomize Matrix")
            print("2. Host Game")
            print("3. Connect to Game Server")
            print("4. Exit")
        elif menuType == MenuType.Host:
            print("Starting Server...")

    def inputIP(self):
        message = "Enter IP Address and port: "
        inp = input(message)
        ip, port = Network.validateAddress(inp)
        while port == 0:
            inp = input(message)
            ip, port = Network.validateAddress(inp)
        return ip, int(port)

    def inputInt(self, lmin=0, lmax=100):
        isValid = False
        inp = None
        while not isValid:
            inp = input(f"Enter a digit between {lmin} and {lmax}: ")
            if not inp.isdigit():
                continue
            if int(inp) < lmin and int(inp) > lmax:
                continue
            isValid = True
        return int(inp)

    def beginGame(self, connection: Network, chance=ChanceType.Your):
        gameOver = False
        while not gameOver:
            # show everytime
            self.bingoBoard.show()
            if chance == ChanceType.Your:
                num = self.inputInt(1, 25)
                if self.bingoBoard.isMarked(num):
                    print(f"{num} already marked.")
                    continue
                self.bingoBoard.mark(num)
                # eval board and send -1 if game is over (we won)
                gameOver = self.bingoBoard.evaluateBoard() == 5
                if gameOver:
                    connection.send(str(-1))  # indicates game is over
                else:
                    connection.send(str(num))
                    chance = ChanceType.Opponent
            else:
                print("Waiting for opponent...")
                num = connection.receive()
                if int(num) == -1:
                    break
                self.bingoBoard.mark(int(num))
                gameOver = self.bingoBoard.evaluateBoard() == 5
                chance = ChanceType.Your

        # game ended, but who won
        if chance == ChanceType.Your:
            print("You won")
            connection.send("-1")
        else:
            print("Opponent Won")
        connection.cleanup()

    def negotiateChance(self, connection, role) -> ChanceType:
        """
        Server generates a random number to select chance
        and sends it to client.
        Client waits for server to see change value
        """
        chance = None
        other = {0: 1, 1: 0}
        if role == "server":
            chance = random.randint(0, 1)
            connection.send(str(other[chance]))
        elif role == "client":
            chance = int(connection.receive())
        return ChanceType[chance]

    def run(self):
        print("Welcome to the BINGO")
        self.bingoBoard.show()
        self.showMenu()
        connection = None
        userInput = self.inputInt(1, 4)
        while userInput == MenuType.Randomize:
            self.bingoBoard.randomizeBoard()
            self.bingoBoard.show()
            self.showMenu()
            userInput = self.inputInt(1, 4)
        if userInput == MenuType.Host:
            self.showMenu(MenuType.Host)
            connection = Network()
            clSocket = connection.startServer()
            if clSocket is not None:
                chance = self.negotiateChance(connection, "server")
                self.beginGame(connection, chance)
        elif userInput == MenuType.Connect:
            ipAddress, port = self.inputIP()
            connection = Network(ipAddress, int(port))
            if connection.connectServer():
                chance = self.negotiateChance(connection, "client")
                self.beginGame(connection, chance)


if __name__ == "__main__":
    GameDriver().run()
