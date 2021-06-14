import tkinter as tk
import random as rd


class MainWindow(object):
    def __init__(self, title="BINGO", size="600x600"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.mainParent = tk.Frame(self.root, width=600, height=600, bg="red")
        self.mainParent.pack(fill="both", expand=True)
        self.mainParent.pack_propagate(0)
        self.frames = {}

    def setFrames(self, frames=None):
        assert isinstance(frames, dict)
        self.frames = frames

    def switchToFrame(self, frameName: str, data=None):
        self.clearMainParent()
        self.frames[frameName].visible()
        if data:
            self.frames[frameName].update(data)

    def clearMainParent(self):
        for widget in self.mainParent.winfo_children():
            widget.pack_forget()

    def show(self):
        frameIter = self.frames.keys()
        it = iter(frameIter)
        firstFrame = next(it)
        self.switchToFrame(firstFrame)
        self.root.mainloop()


class Page(object):
    def __init__(self, parent, **params):
        self.parent = parent
        self.frame = tk.Frame(parent, **params)

    def update(self, data):
        # this function is called when transition to
        # this page is made. Previous page can supply some
        # data to update this page
        raise NotImplementedError

    def visible(self):
        self.frame.pack(fill="both", expand=True)
        self.frame.pack_propagate(0)


class HomePage(Page):
    def __init__(self, mainWindow: MainWindow):
        self.mainWindow = mainWindow
        Page.__init__(
            self, mainWindow.mainParent, width=600, height=600, bg="#00ff00"
        )
        self.configure()

    def configure(self):
        self.frame.rowconfigure(4)
        self.frame.columnconfigure(3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        # title frame
        titleFrame = tk.Frame(self.frame, bg="green")
        titleFrame.grid(row=1, column=1, sticky="ew")
        titleLabel = tk.Label(
            titleFrame, text="BINGO", bg="green", font=("Fira Code", 25)
        )
        titleLabel.pack()

        # buttons
        buttonFrame = tk.Frame(self.frame, bg="red")
        buttonFrame.grid(row=2, column=1, sticky="ew")
        btnCfg = {"width": 50}

        # create server
        createServerButton = tk.Button(
            buttonFrame,
            text="Host",
            command=lambda: self.mainWindow.switchToFrame("bingo"),
            **btnCfg
        )
        createServerButton.pack()

        # connect to server
        connectServerButton = tk.Button(
            buttonFrame,
            text="Connect",
            command=lambda: self.mainWindow.switchToFrame("host"),
            **btnCfg
        )
        connectServerButton.pack()

        # exit button
        exitButton = tk.Button(
            buttonFrame, text="Exit", command=self.mainWindow.root.destroy, **btnCfg
        )
        exitButton.pack()
        titleFrame.grid_propagate(0)


class HostPage(Page):
    def __init__(self, mainWindow: MainWindow):
        self.mainWindow = mainWindow
        Page.__init__(
            self, mainWindow.mainParent, width=600, height=600, bg="#00ff00"
        )
        self.configure()

    def configure(self):
        self.frame.rowconfigure(4)
        self.frame.columnconfigure(3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        # title frame
        titleFrame = tk.Frame(self.frame, bg="green")
        titleFrame.grid(row=1, column=1, sticky="ew")
        titleLabel = tk.Label(
            titleFrame, text="Connect to server", bg="green", font=("Fira Code", 16)
        )
        titleLabel.pack()

        # buttons
        interactiveFrame = tk.Frame(self.frame, bg="red")
        interactiveFrame.grid(row=2, column=1, sticky="ew")
        btnCfg = {"width": 50}
        labelCfg = {"width": 54, "height": 2}
        textCfg = {"width": 37, "height": 1, "font": ("Fira Code", 12)}

        # label
        serverLabel = tk.Label(
            interactiveFrame, text="Enter Server IP Address", **labelCfg
        )
        serverLabel.pack()

        # server IP entry
        serverIpEntry = tk.Text(interactiveFrame, **textCfg)
        serverIpEntry.pack()

        # connect to server
        connectServerButton = tk.Button(interactiveFrame, text="Connect", **btnCfg)
        connectServerButton.pack()

        # back button
        backButton = tk.Button(
            interactiveFrame,
            text="Back",
            command=lambda: self.mainWindow.switchToFrame("home"),
            **btnCfg
        )
        backButton.pack()
        titleFrame.grid_propagate(0)


class BingoPage(Page):
    def __init__(self, mainWindow: MainWindow, bingoBoard=None):
        self.mainWindow = mainWindow
        Page.__init__(
            self, mainWindow.mainParent, width=600, height=600, bg="#00ff00"
        )
        if bingoBoard is None:
            self.bingoBoard = self.generateRandomBoard()
        else:
            self.bingoBoard = bingoBoard
        self.bingoBtn = []
        self.configure()

    def generateRandomBoard(self):
        bb = []
        i = 1
        for _ in range(5):
            bb += [[x for x in range(i, i + 5)]]
            i += 5
        return self.randomizeMatrix(bb)

    def randomizeMatrix(self, board):
        for _ in range(25):
            x1, y1 = rd.randint(0, 4), rd.randint(0, 4)
            x2, y2 = rd.randint(0, 4), rd.randint(0, 4)
            temp = board[x1][y1]
            board[x1][y1] = board[x2][y2]
            board[x2][y2] = temp
        return board

    def configure(self):
        self.frame.rowconfigure(4)
        self.frame.columnconfigure(3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        # bingo frame
        bingoFrame = tk.Frame(self.frame, bg="green")
        bingoFrame.grid(row=1, column=1, columnspan=3, sticky="we")

        titleLabel = tk.Label(
            bingoFrame, text="Select your board", bg="green", font=("Fira Code", 16)
        )
        titleLabel.pack()
        # create bingo
        self.bingoBtn = []
        bingoBtnCfg = {"height": 2, "width": 2, "font": ("Fira Code", 12)}
        for x in range(5):
            rowFrame = tk.Frame(bingoFrame)
            for y in range(5):
                btn = tk.Button(
                    rowFrame, text=str(self.bingoBoard[x][y]), **bingoBtnCfg
                )
                btn.pack(side=tk.LEFT)
                self.bingoBtn += [btn]
            rowFrame.pack()

        print(self.bingoBoard)

        # buttons
        buttonFrame = tk.Frame(self.frame, bg="red")
        buttonFrame.grid(row=2, column=1, sticky="ew")
        btnCfg = {"width": 50}

        # randomize button
        createServerButton = tk.Button(
            buttonFrame, text="Randomize", command=self.randomizeBoard, **btnCfg
        )
        createServerButton.pack()

        # host server button
        hostServerButton = tk.Button(
            buttonFrame,
            text="Host",
            command=lambda: self.mainWindow.switchToFrame("game", self.bingoBoard),
            **btnCfg
        )
        hostServerButton.pack()

        # back button
        backButton = tk.Button(
            buttonFrame,
            text="Back",
            command=lambda: self.mainWindow.switchToFrame("home"),
            **btnCfg
        )
        backButton.pack()
        bingoFrame.grid_propagate(0)

    def randomizeBoard(self):
        self.bingoBoard = self.randomizeMatrix(self.bingoBoard)
        self.updateBingoBoard()

    def updateBingoBoard(self):
        i = 0
        for x in range(5):
            for y in range(5):
                self.bingoBtn[i]["text"] = self.bingoBoard[x][y]
                i += 1


class BingoGamePage(BingoPage):
    def __init__(self, mainWindow: MainWindow, bingoBoard=None):
        BingoPage.__init__(self, mainWindow, bingoBoard)

    # override
    def update(self, data):
        self.bingoBoard = data
        self.updateBingoBoard()

    # override
    def configure(self):
        self.frame.rowconfigure(4)
        self.frame.columnconfigure(3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        # bingo frame
        bingoFrame = tk.Frame(self.frame, bg="green")
        bingoFrame.grid(row=1, column=1, columnspan=3, sticky="we")

        messageLabel = tk.Label(
            bingoFrame, text="Your Turn", bg="green", font=("Fira Code", 16)
        )
        messageLabel.pack()
        # create bingo
        self.bingoBtn = []
        bingoBtnCfg = {"height": 2, "width": 2, "font": ("Fira Code", 12)}
        for x in range(5):
            rowFrame = tk.Frame(bingoFrame)
            for y in range(5):
                btn = tk.Button(
                    rowFrame, text=str(self.bingoBoard[x][y]), **bingoBtnCfg
                )
                btn.pack(side=tk.LEFT)
                self.bingoBtn += [btn]
            rowFrame.pack()

        print(self.bingoBoard)

        # buttons
        buttonFrame = tk.Frame(self.frame, bg="red")
        buttonFrame.grid(row=2, column=1, sticky="ew")
        bingoTallybtnCfg = {"width": 4, "height": 3, "font": ("Fira Code", 14)}

        # BINGO buttons
        bingo = "BINGO"
        self.bingoTallyButtons = []
        bingoTallyFrame = tk.Frame(buttonFrame)
        for i in range(5):
            btn = tk.Button(bingoTallyFrame, text=bingo[i], **bingoTallybtnCfg)
            self.bingoTallyButtons += [btn]
            btn.pack(side=tk.LEFT)
        bingoTallyFrame.pack()
        # back button
        btnCfg = {"width": 50}
        quitButton = tk.Button(
            buttonFrame,
            text="Leave",
            command=lambda: self.mainWindow.switchToFrame("home"),
            **btnCfg
        )
        quitButton.pack()
        bingoFrame.grid_propagate(0)


if __name__ == "__main__":
    window = MainWindow("BINGO")
    pages = {
        "home": HomePage(window),
        "host": HostPage(window),
        "bingo": BingoPage(window),
        "game": BingoGamePage(window),
    }
    window.setFrames(pages)
    window.show()
