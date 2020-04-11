import numpy as np
import GenAlg
import random
from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NO_DIRECTION = 4


class Cell:
    def __init__(self, x, y):
        # Indicators if a wall exists in a certain direction
        self.x = x
        self.y = y
        self.parent = None
        self.paths = []

        self.visited = False

    def setVisited(self, val):
        self.visited = val


class Maze:
    def __init__(self, probMatrix):

        # Generation of maze exit and entrance
        self.nCols = len(probMatrix[0])
        self.nRows = len(probMatrix)

        [self.finishX, self.finishY] = self.generateEdge(self.nCols, self.nRows)
        [self.startX, self.startY] = self.generateEdge(self.nCols, self.nRows)

        while [self.finishX, self.finishY] == [self.startX, self.startY]:
            [self.startX, self.startY] = self.generateEdge(self.nCols, self.nRows)

        self.cellMaze = []
        self.cells = []
        self.rowNo = len(probMatrix)
        self.colNo = len(probMatrix[0])

        # Initialization of complete maze
        for i in range(0, self.rowNo):
            self.cellMaze.append([])
            for j in range(0, self.colNo):
                self.cellMaze[i].append(Cell(j, i))

        self.startCell = self.getCell(self.startX, self.startY)
        self.finishCell = self.getCell(self.finishX, self.finishY)
        self.generateMaze(probMatrix)

    def generateEdge(self, nCols, nRows):
        p = 0.5
        r = random.randint(0, 1)
        if r < p:
            r = random.randint(0, 1)
            if r < p:
                return [nCols - 1, random.randint(0, nRows - 1)]
            else:
                return [0, random.randint(0, nRows - 1)]
        else:
            r = random.randint(0, 1)
            if r < p:
                return [random.randint(0, nCols - 1), nRows - 1]
            else:
                return [random.randint(0, nCols - 1), 0]

    def __str__(self):

        stringMatrix = []
        for i in range(0, 2 * self.nRows + 1):
            stringMatrix.append([])
            for j in range(0, 2 * self.nCols + 1):
                if i % 2 == 0 or j % 2 == 0:
                    stringMatrix[i].append('@')
                else:
                    stringMatrix[i].append(' ')

        if self.startX == 0:
            stringMatrix[self.startY * 2 + 1][self.startX * 2] = ' '
        elif self.startY == 0:
            stringMatrix[self.startY * 2][self.startX * 2 + 1] = ' '
        if self.startX == self.nCols - 1:
            stringMatrix[self.startY * 2 + 1][self.startX * 2 + 2] = ' '
        elif self.startY == self.nRows - 1:
            stringMatrix[self.startY * 2 + 2][self.startX * 2 + 1] = ' '

        if self.finishX == 0:
            stringMatrix[self.finishY * 2 + 1][self.finishX * 2] = ' '
        elif self.finishY == 0:
            stringMatrix[self.finishY * 2][self.finishX * 2 + 1] = ' '
        if self.finishX == self.nCols - 1:
            stringMatrix[self.finishY * 2 + 1][self.finishX * 2 + 2] = ' '
        elif self.finishY == self.nRows - 1:
            stringMatrix[self.finishY * 2 + 2][self.finishX * 2 + 1] = ' '

        for row in self.cellMaze:
            for cell in row:
                curX = 2 * cell.x + 1
                curY = 2 * cell.y + 1

                for neighbor in cell.paths:
                    tmpDirection = self.getDirection(cell, neighbor)
                    if tmpDirection == Direction.UP:
                        stringMatrix[curY - 1][curX] = ' '
                    elif tmpDirection == Direction.LEFT:
                        stringMatrix[curY][curX - 1] = ' '

        finalString = ""
        for charList in stringMatrix:
            finalString += "".join(charList) + "\n"
        return finalString

    def getDirection(self, fromCell, toCell):
        diffx = toCell.x - fromCell.x
        diffy = toCell.y - fromCell.y

        if diffy == 0:
            if diffx == 1:
                return Direction.RIGHT
            if diffx == -1:
                return Direction.LEFT
        if diffx == 0:
            if diffy == 1:
                return Direction.DOWN
            if diffy == -1:
                return Direction.UP
        return Direction.NO_DIRECTION

    def getCell(self, x, y):
        return self.cellMaze[y][x]

    def isVisited(self, i, j):
        return self.cellMaze[j][i].visited

    def makePath(self, parentX, parentY, childX, childY):
        child = self.getCell(childX, childY)
        parent = self.getCell(parentX, parentY)
        child.parent = parent
        child.setVisited(True)
        parent.paths.append(child)
        child.paths.append(parent)

    def generateMaze(self, probMatrix):
        # Generation of maze entrance
        print("Maze dimensions:", self.nCols, "x", self.nRows)
        print("Starting from cell:", self.startCell.x, ",", self.startCell.y)
        # Initialization of current position
        self.startCell.setVisited(True)
        curCell = self.startCell

        # List of contenders that are not initially optimal but will be chosen after the fact
        # when the current cell is cornered
        globalContenders = []

        while True:

            localContenders = []

            if (curCell.x != 0) and not self.isVisited(curCell.x - 1, curCell.y):
                localContenders.append(self.getCell(curCell.x - 1, curCell.y))
                print("Making path from:", curCell.x, curCell.y, " To:", curCell.x - 1, curCell.y)
                self.makePath(curCell.x, curCell.y, curCell.x - 1, curCell.y)

            if (curCell.x != self.colNo - 1) and not self.isVisited(curCell.x + 1, curCell.y):
                localContenders.append(self.getCell(curCell.x + 1, curCell.y))
                print("Making path from:", curCell.x, curCell.y, " To:", curCell.x + 1, curCell.y)
                self.makePath(curCell.x, curCell.y, curCell.x + 1, curCell.y)

            if (curCell.y != 0) and not self.isVisited(curCell.x, curCell.y - 1):
                localContenders.append(self.getCell(curCell.x, curCell.y - 1))
                print("Making path from:", curCell.x, curCell.y, " To:", curCell.x, curCell.y - 1)
                self.makePath(curCell.x, curCell.y, curCell.x, curCell.y - 1)

            if (curCell.y != self.rowNo - 1) and not self.isVisited(curCell.x, curCell.y + 1):
                localContenders.append(self.getCell(curCell.x, curCell.y + 1))
                print("Making path from:", curCell.x, curCell.y, " To:", curCell.x, curCell.y + 1)
                self.makePath(curCell.x, curCell.y, curCell.x, curCell.y + 1)

            if localContenders == []:
                if globalContenders == []:
                    return
                localBestContender = globalContenders[0]
                for contender in globalContenders:
                    if probMatrix[contender.x][contender.y] > probMatrix[localBestContender.x][localBestContender.y]:
                        localBestContender = contender
                globalContenders.remove(localBestContender)
                nextIsChosen = True
            else:
                localBestContender = localContenders[0]
                nextIsChosen = False

            while not nextIsChosen:
                for contender in localContenders:
                    if probMatrix[localBestContender.x][localBestContender.y] < probMatrix[contender.x][contender.y]:
                        localBestContender = contender
                r = random.random()
                if r < probMatrix[localBestContender.x][localBestContender.y]:
                    nextIsChosen = True
                else:
                    try:
                        localContenders.remove(localBestContender)
                    except ValueError:
                        pass

            # Adds the unused Cells to the global list
            if localContenders:
                globalContenders.extend(localContenders)

            # Mark the chosen best contender as visited
            curCell = localBestContender
            curCell.setVisited(True)
            print("Cur x,y :", localBestContender.x, ",", localBestContender.y)


def main():
    probMatrixExample = [[0.4, 0.1, 0.2], [0.6, 0.2, 0.26], [0.42, 0.31, 0.52]]
    mazeExample = Maze(probMatrixExample)
    print(mazeExample)
    print("Done")


if __name__ == "__main__":
    main()
