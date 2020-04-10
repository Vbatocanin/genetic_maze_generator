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
    def __init__(self, x, y, prob):
        # Indicators if a wall exists in a certain direction
        self.x = x
        self.y = y
        self.parent = None
        self.paths = []

        self.visited = False

    def setVisited(self,val):
        self.visited = val


class Maze:
    def __init__(self, probMatrix):

        # Generation of maze exit and entrance
        finishX = random.randint(0, len(probMatrix[0]) - 1)
        finishY = random.randint(0, len(probMatrix) - 1)

        startX = random.randint(0, len(probMatrix[0]) - 1)
        startY = random.randint(0, len(probMatrix) - 1)

        self.cellMaze = []
        self.cells = []
        self.rowNo = len(probMatrix)
        self.colNo = len(probMatrix[0])

        # Initialization of complete maze
        for i in range(0, self.rowNo):
            self.cellMaze.append([])
            for j in range(0, self.colNo):
                self.cellMaze[i].append(Cell(i, j, probMatrix[i][j]))

        self.startCell = self.getCell(startX, startY)
        self.finishCell = self.getCell(finishX, finishY)
        self.generateMaze(probMatrix)

    def getCell(self, x, y):
        return self.cellMaze[x][y]

    def isVisited(self, i, j):
        return self.cellMaze[i][j].visited

    def makePath(self, parentX, parentY, childX, childY):
        child = self.getCell(childX, childY)
        parent = self.getCell(parentX, parentY)
        child.parent = parent
        child.setVisited(True)
        parent.paths.append(child)


    def generateMaze(self, probMatrix):
        # Generation of maze entrance
        print(len(probMatrix) - 1)
        print(len(probMatrix[0]) - 1)

        # Initialization of current position
        curCell = self.startCell

        # Number of Cells not yet visited
        noNotVisited = len(probMatrix) * len(probMatrix[0])

        # List of contenders that are not initially optimal but will be chosen after the fact
        # when the current cell is cornered
        globalContenders = []

        while noNotVisited > 0:

            localContenders = []

            if (curCell.x != 0) and not self.isVisited(curCell.x - 1, curCell.y):
                localContenders.append(self.getCell(curCell.x - 1, curCell.y))
                self.makePath(curCell.x, curCell.y, curCell.x - 1, curCell.y)

            if (curCell.x != self.colNo - 1) and not self.isVisited(curCell.x + 1, curCell.y):
                localContenders.append(self.getCell(curCell.x + 1, curCell.y))
                self.makePath(curCell.x, curCell.y, curCell.x + 1, curCell.y)

            if (curCell.y != 0) and not self.isVisited(curCell.x, curCell.y - 1):
                localContenders.append(self.getCell(curCell.x, curCell.y - 1))
                self.makePath(curCell.x, curCell.y, curCell.x, curCell.y - 1)

            if (curCell.y != self.rowNo - 1) and not self.isVisited(curCell.x, curCell.y + 1):
                localContenders.append(self.getCell(curCell.x, curCell.y + 1))
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
                    #print(contender.x, contender.y, "vs", localBestContender.x, localBestContender.y)
                    #print("----------------------")
                    if (probMatrix[localBestContender.x][localBestContender.y] < probMatrix[contender.x][contender.y]):
                        localBestContender = contender
                r = random.random()
                if (r < probMatrix[localBestContender.x][localBestContender.y]):
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
            print("Cur x,y :",localBestContender.x,",",localBestContender.y)



def main():
    probMatrixExample = [[0.4, 0.1, 0.2], [0.6, 0.2, 0.26], [0.42, 0.31, 0.52]]
    mazeExample = Maze(probMatrixExample)


if __name__ == "__main__":
    main()
