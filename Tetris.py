"""Tetris Game"""
import pygame
import random
import numpy as np

SPACE = "  "


class Piece:
    """Piece Class"""
    def __init__(self, table, row, col):
        # blocks
        self.blockI = [
                       np.array([["ı", "ı", "ı", "ı"],
                                ["  ", "  ", "  ", "  "]]),
                       np.array([["ı", "  "],
                                 ["ı", "  "],
                                 ["ı", "  "],
                                 ["ı", "  "]])]

        self.blockO = [np.array([["o", "o"],
                                ["o", "o"]])]

        self.blockT = [
                        np.array([["t", "t", "t"],
                                  ["  ", "t", "  "]]),

                       np.array([["  ", "t"],
                                 ["t", "t"],
                                 ["  ", "t"]]),

                       np.array([["  ", "t", "  "],
                                 ["t", "t", "t"]]),

                       np.array([["t", "  "],
                                 ["t", "t"],
                                 ["t", "  "]])]

        self.blockS = [
                        np.array([["  ", "s", "s"],
                                  ["s", "s", "  "]]),

                        np.array([["s", "  "],
                                  ["s", "s"],
                                  ["  ", "s"]])
        ]

        self.blockZ = [
                        np.array([["z", "z", "  "],
                                  ["  ", "z", "z"]]),

                        np.array([["  ", "z"],
                                  ["z", "z"],
                                  ["z", "  "]])
        ]

        self.blockL = [
                        np.array([["l", "  ", "  "],
                                  ["l", "l", "l"]]),

                        np.array([["l", "l"],
                                  ["l", "  "],
                                  ["l", "  "]]),

                        np.array([["l", "l", "l"],
                                  ["  ", "  ", "l"]]),

                        np.array([["  ", "l"],
                                  ["  ", "l"],
                                  ["l", "l"]])
        ]


        self.blockJ = [
                        np.array([["  ", "  ", "j"],
                                  ["j", "j", "j"]]),

                        np.array([["j", "  "],
                                  ["j", "  "],
                                  ["j", "j"]]),

                        np.array([["j", "j", "j"],
                                  ["j", "  ", "  "]]),

                        np.array([["j", "j"],
                                  ["  ", "j"],
                                  ["  ", "j"]])
        ]

        self.ColorDict = {"ı": (49, 199, 239), "o": (247, 211, 8), "t": (173, 77, 156), "s": (66, 182, 66), "z": (239, 32, 41),
                          "j": (90, 101, 173), "l": (239, 121, 33), "  ": (10, 10, 10)}
        # block list
        self.blocks = ["ı", "o", "t", "s", "z", "j", "l"]

        self.BlockList = [self.blockI, self.blockO, self.blockT, self.blockS, self.blockZ, self.blockJ, self.blockL]
        self.table = table

        # row and col
        self.row = row
        self.col = col

        # color
        self.color = "  "

        # block
        self.bList = random.choice(self.BlockList)
        self.block = self.bList[0]

        self.pos = []
        self.move = True

        # turn
        self.turn = 0

    def addToTable(self):
        """add to table"""
        # select a block and start column
        self.bList = random.choice(self.BlockList)
        self.block = self.bList[0]
        startCol = self.col//2 - int(self.block.shape[1]) // 2

        self.turn = 0
        for rowIndex, row in enumerate(self.block):
            for colIndex, col in enumerate(row):
                # add to table
                if self.block[rowIndex, colIndex] != "  ":
                    self.table[rowIndex, colIndex + startCol] = self.block[rowIndex, colIndex]
                    self.pos.append([rowIndex, colIndex+startCol])

        return self.table

    def goDown(self):
        """go down"""
        newPos = []
        copy = self.table.copy()
        for pos in self.pos[::-1]:
            try:
                row, col = pos
                # check if under is empty
                if self.table[row + 1, col] == SPACE and self.move is True:
                    # switch and go down
                    self.table[row + 1, col] = self.table[row, col]
                    self.color = self.table[row, col]
                    self.table[row, col] = SPACE
                    newPos.append([row + 1, col])
                else:
                    self.move = False
                    self.table = copy

                if row == self.row-1:
                    self.move = False
                    self.table = copy

            except IndexError: pass

        self.pos = newPos[::-1]
        return self.table

    def moveLeft(self):
        """move piece"""
        log = self.table.copy()
        newPos = []
        row, col = [], []
        # create row, col
        for position in self.pos:
            row.append(position[0])
            col.append(position[1])
        for r, c in zip(row, col):
            if self.table[r, c-1] == SPACE and c != 0:
                # go left
                newPos.append([r, c-1])
                self.table[r, c-1] = self.table[r, c]
                self.table[r, c] = SPACE
            else:
                # change table
                newPos = self.pos
                self.table = log
                break
        self.pos = newPos
        return self.table

    def moveRight(self):
        """move piece"""
        run = True
        # check cols
        for _, col in self.pos:
            if col == self.col-1:
                run = False

        if run is True:
            log = self.table.copy()
            newPos = []
            row, col = [], []
            # create row, col
            for position in self.pos:
                row.append(position[0])
                col.append(position[1])
            col.reverse()
            row.reverse()

            for r, c in zip(row, col):
                if self.table[r, c + 1] == SPACE:
                    # go left
                    newPos.append([r, c + 1])
                    self.table[r, c + 1] = self.table[r, c]
                    self.table[r, c] = SPACE
                else:
                    # change table
                    newPos = self.pos
                    self.table = log
                    break

            newPos.reverse()
            self.pos = newPos

        return self.table

    def turnPiece(self):
        """turn piece"""
        log = self.table.copy()
        pos = self.pos.copy()
        block = self.block.copy()

        self.turn += 1
        try:
            self.block = self.bList[self.turn]
        except:
            self.turn = 0
            self.block = self.bList[self.turn]


        startPos = self.pos[0]

        # make them empty
        for row, col in self.pos:
            self.table[row, col] = SPACE

        r, c = startPos
        newPos = []
        try:
            for row in range(self.block.shape[0]):
                for col in range(self.block.shape[1]):
                    # check
                    if self.block[row, col] != SPACE:
                        if self.table[row + r, col + c]:
                            # replace
                            self.table[row + r, col + c] = self.block[row, col]
                            newPos.append([row + r, col + c])
                        else:
                            # go back
                            newPos = pos
                            self.block = block
                            self.table = log
                            break
            print(self.table)
            print(newPos)
        except IndexError:
            newPos = pos
            self.block = block
            self.table = log

        self.pos = newPos
        return self.table


class Main:
    """Main class of the game"""
    def __init__(self):
        pygame.init()
        # define row, col and sqSize
        self.col = 20
        self.row = 35
        self.sqSize = 20
        # define Width Height and scree
        self.WIDTH = self.col*self.sqSize
        self.HEIGHT = self.row*self.sqSize
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Tetris")
        # create table
        self.table = np.full((self.row, self.col), SPACE)
        # running, clock and FPS
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 35
        # colors
        self.ColorLine = (40, 40, 40)
        self.ColorDict = {"ı": (49, 199, 239), "o": (247, 211, 8), "t": (173, 77, 156), "s": (66, 182, 66), "z": (239, 32, 41),
                          "j": (90, 101, 173), "l": (239, 121, 33), "  ": (10, 10, 10)}
        # block list
        self.blocks = ["ı", "o", "t", "s", "z", "j", "l"]

        self.piece = None

        self.timer = pygame.USEREVENT
        pygame.time.set_timer(self.timer, 150)

    def addPiece(self):
        """add piece"""
        self.piece = Piece(self.table, self.row, self.col)
        self.table = self.piece.addToTable()

    def pieceChecks(self):
        """piece check"""
        for pos in self.piece.pos:
            if pos[0] == self.row-1:
                self.piece.move = False
        if self.piece.move is False:
            self.addPiece()
        self.checkRow()

    def checkRow(self):
        """check rows"""
        delete = False
        for row in range(self.row):
            count = 0
            for col in range(self.col):
                if self.table[row, col] != SPACE: count += 1

            if count == self.col:
                delete = row
                break

        if delete is not False:
            self.table[delete:] = SPACE
            for row in list(reversed(range(self.row))):
                for col in range(self.col):
                    try:
                        self.table[row + 1, col] = self.table[row, col]
                        self.table[row, col] = SPACE
                    except IndexError: pass

            newPos = []
            for pos in self.piece.pos:
                newPos.append([pos[0]+1, pos[1]])
            self.piece.pos = newPos


    def event(self):
        """event loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quit from the game
                self.running = False
            if event.type == self.timer:
                self.table = self.piece.goDown()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.table = self.piece.moveRight()
                if event.key == pygame.K_LEFT:
                    self.table = self.piece.moveLeft()
                if event.key == pygame.K_DOWN:
                    self.table = self.piece.goDown()
                if event.key == pygame.K_UP:
                    self.table = self.piece.turnPiece()

    def main(self):
        """main function"""
        self.addPiece()
        while self.running:
            # be sure about the FPS
            self.clock.tick(self.FPS)
            self.event()
            self.pieceChecks()
            self.draw()

    def drawLines(self):
        """drawing lines"""
        # row => y, col => x
        for row in range(self.row):
            for col in range(self.col):
                # draw horizontal and vertical lines
                pygame.draw.line(self.screen, self.ColorLine, (col*self.sqSize, 0), (col*self.sqSize, self.HEIGHT))
                pygame.draw.line(self.screen, self.ColorLine, (0, row*self.sqSize), (self.WIDTH, row*self.sqSize))

    def drawGrids(self):
        """draw grids"""
        # row => y, col => x
        for row in range(self.row):
            for col in range(self.col):
                x = col*self.sqSize
                y = row*self.sqSize
                string = self.table[row, col]
                rect = pygame.rect.Rect((x, y), (self.sqSize, self.sqSize))
                pygame.draw.rect(self.screen, self.ColorDict[string], rect)

    def draw(self):
        """draw screen"""
        self.screen.fill(self.ColorDict["  "])
        self.drawGrids()
        self.drawLines()
        pygame.display.flip()



if __name__ == '__main__':
    """Start Game"""
    Main().main()
pygame.quit()
