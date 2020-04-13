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
    def opposite_direction(self):
        pass


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # TODO: Potentially remove parent because it's not used atm
        self.parent = None

        # Works exactly like a graph adjacency list
        self.paths = []

        # Used in DFS, indicates if DFS has been called in this Cell
        self.visited = False

    def setVisited(self, val):
        self.visited = val


class Maze:
    def __init__(self, probMatrix):

        # Maze dimensions, in case a non-square maze is given as input
        self.nCols = len(probMatrix[0])
        self.nRows = len(probMatrix)

        # Generation of start and exit node
        # [self.exitX, self.exitY] = self.generateEdge(self.nCols, self.nRows)
        [self.exitX, self.exitY] = [self.nCols - 1, 0]
        # [self.startX, self.startY] = self.generateEdge(self.nCols, self.nRows)
        [self.startX, self.startY] = [0, self.nRows - 1]

        # Re-generate start in case start and finish nodes are one and the same
        while [self.exitX, self.exitY] == [self.startX, self.startY]:
            [self.startX, self.startY] = self.generateEdge(self.nCols, self.nRows)

        # cellMaze is a list of lists which contains Cell objects in the same order as the prob matrix
        self.cellMaze = []

        # Initialization of complete maze
        for i in range(0, self.nRows):
            self.cellMaze.append([])
            for j in range(0, self.nCols):
                self.cellMaze[i].append(Cell(j, i))

        self.startCell = self.getCell(self.startX, self.startY)
        self.finishCell = self.getCell(self.exitX, self.exitY)
        self.generateMaze(probMatrix)

        for row in self.cellMaze:
            for cell in row:
                cell.setVisited(False)

    # Generates the coordiantes for an edge Cell, which is only used for the start and finish cells
    def generateEdge(self, nCols, nRows):
        # Chance of it being on the left-right or the up-down edges
        p = 0.5
        r = random.randint(0, 1)
        if r < p:
            # Same princible, just for left or right
            r = random.randint(0, 1)
            if r < p:
                return [nCols - 1, random.randint(0, nRows - 1)]
            else:
                return [0, random.randint(0, nRows - 1)]
        else:
            # Same princible, just for up or down
            r = random.randint(0, 1)
            if r < p:
                return [random.randint(0, nCols - 1), nRows - 1]
            else:
                return [random.randint(0, nCols - 1), 0]


    def __str__(self):

        # @ indicate a wall
        # Blank spaces indicate free space

        # List of lists which contain charaters, the coordinates correspond to the original maze
        # but with padding, which means (stringMatrixX, stringMatrixY) -> (mazeX * 2 + 1, mazeY * 2 + 1)
        stringMatrix = []
        for i in range(0, 2 * self.nRows + 1):
            stringMatrix.append([])
            for j in range(0, 2 * self.nCols + 1):
                if i % 2 == 0 or j % 2 == 0:
                    stringMatrix[i].append('@')
                else:
                    stringMatrix[i].append(' ')

        # Adding a blank space as an entrance to the maze
        if self.startX == 0:
            stringMatrix[self.startY * 2 + 1][self.startX * 2] = ' '
        elif self.startY == 0:
            stringMatrix[self.startY * 2][self.startX * 2 + 1] = ' '
        elif self.startX == self.nCols - 1:
            stringMatrix[self.startY * 2 + 1][self.startX * 2 + 2] = ' '
        elif self.startY == self.nRows - 1:
            stringMatrix[self.startY * 2 + 2][self.startX * 2 + 1] = ' '

        # Adding a blank space as an exit from the maze
        if self.exitX == 0:
            stringMatrix[self.exitY * 2 + 1][self.exitX * 2] = ' '
        elif self.exitY == 0:
            stringMatrix[self.exitY * 2][self.exitX * 2 + 1] = ' '
        elif self.exitX == self.nCols - 1:
            stringMatrix[self.exitY * 2 + 1][self.exitX * 2 + 2] = ' '
        elif self.exitY == self.nRows - 1:
            stringMatrix[self.exitY * 2 + 2][self.exitX * 2 + 1] = ' '

        # Drawing the actual hallways from Cell to Cell
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

        # Final string generatrion
        finalString = ""
        for charList in stringMatrix:
            finalString += "".join(charList) + "\n"
        return finalString

    # A function that return the direction in which you need to go
    # in order to go from fromCell to toCell
    @staticmethod
    def getDirection(fromCell, toCell):
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

    @staticmethod
    def isDirectionOpposite(dir1, dir2):
        if dir1 == Direction.UP and dir2 == Direction.DOWN:
            return True
        elif dir1 == Direction.DOWN and dir2 == Direction.UP:
            return True
        elif dir1 == Direction.LEFT and dir2 == Direction.RIGHT:
            return True
        elif dir1 == Direction.RIGHT and dir2 == Direction.LEFT:
            return True
        else:
            return False

    def getCell(self, x, y):
        return self.cellMaze[y][x]

    def isVisited(self, i, j):
        return self.cellMaze[j][i].visited

    # Makes a path from parentCell to childCell according
    # to their coordinates
    def makePath(self, parentX, parentY, childX, childY):
        child = self.getCell(childX, childY)
        parent = self.getCell(parentX, parentY)
        child.parent = parent
        child.setVisited(True)
        parent.paths.append(child)
        child.paths.append(parent)

    def generateMaze(self, probMatrix):
        # Generation of maze entrance
        # print("Maze dimensions:", self.nCols, "x", self.nRows)
        # print("Starting from cell:", self.startCell.x, ",", self.startCell.y)
        # Initialization of current position
        self.startCell.setVisited(True)
        curCell = self.startCell

        # List of contenders that are not initially optimal but will be chosen after the fact
        # when the current cell is cornered
        globalContenders = []

        # This while loop adds potetial contenders which are adjacent to the current Cell
        while True:

            localContenders = []

            if (curCell.x != 0) and not self.isVisited(curCell.x - 1, curCell.y):
                tmpCell = self.getCell(curCell.x - 1, curCell.y)
                localContenders.append(tmpCell)
                # print("Making path from:", curCell.x, curCell.y, " To:", curCell.x - 1, curCell.y)
                self.setParent(curCell.x, curCell.y, curCell.x - 1, curCell.y)

            if (curCell.x != self.nCols - 1) and not self.isVisited(curCell.x + 1, curCell.y):
                tmpCell = self.getCell(curCell.x + 1, curCell.y)
                localContenders.append(tmpCell)
                # print("Making path from:", curCell.x, curCell.y, " To:", curCell.x + 1, curCell.y)
                self.setParent(curCell.x, curCell.y, curCell.x + 1, curCell.y)

            if (curCell.y != 0) and not self.isVisited(curCell.x, curCell.y - 1):
                tmpCell = self.getCell(curCell.x, curCell.y - 1)
                localContenders.append(tmpCell)
                # print("Making path from:", curCell.x, curCell.y, " To:", curCell.x, curCell.y - 1)
                self.setParent(curCell.x, curCell.y, curCell.x, curCell.y - 1)

            if (curCell.y != self.nRows - 1) and not self.isVisited(curCell.x, curCell.y + 1):
                tmpCell = self.getCell(curCell.x, curCell.y + 1)
                localContenders.append(tmpCell)
                # print("Making path from:", curCell.x, curCell.y, " To:", curCell.x, curCell.y + 1)
                self.setParent(curCell.x, curCell.y, curCell.x, curCell.y + 1)

            # In case there weren't any new Cells, return, because the maze is done
            if not localContenders:
                if not globalContenders:
                    return
                # If there are still Cells left, but which aren't adjacent,
                # fetch the one with the best probability attribute

                localBestContender = max(globalContenders, key=lambda con: probMatrix[con.y][con.x])
                globalContenders.remove(localBestContender)
                # The next Cell to visit is already chosed
                nextIsChosen = True
            else:
                # In Case there are new adjacent Cells, find the best one with the given probability parameter
                localBestContender = localContenders[0]
                nextIsChosen = False

            # Take the current Cell with the probability from the probMatrix
            # If it misses on the first Cell, picks the next best cell according to prob parameter
            while not nextIsChosen:
                if len(localContenders) == 1:
                    localBestContender = localContenders[0]
                    nextIsChosen = True
                    break
                localBestContender = max(localContenders, key=lambda con: probMatrix[con.y][con.x])
                r = random.random()
                if r < probMatrix[localBestContender.y][localBestContender.x]:
                    nextIsChosen = True
                else:
                    try:
                        localContenders.remove(localBestContender)
                    except ValueError:
                        pass

            # Adds the unused Cells to the global list, which accumulates all the not-currently-adjacent Cells
            if localContenders:
                globalContenders.extend(localContenders)
                curCell = localBestContender.parent

            # Mark the chosen best contender as visited

            self.makePath(curCell.x,curCell.y,localBestContender.x,localBestContender.y)
            curCell = localBestContender
            curCell.setVisited(True)
            # print("Cur x,y :", localBestContender.x, ",", localBestContender.y)

    def setParent(self, parentX, parentY, childX, childY):
        child = self.getCell(childX, childY)
        parent = self.getCell(parentX, parentY)
        child.parent = parent



def main():
    probMatrixExample = [[0.4, 0.1, 0.2], [0.6, 0.2, 0.26], [0.42, 0.31, 0.52]]
    mazeExample = Maze(probMatrixExample)
    print(mazeExample)
    print("Done")


if __name__ == "__main__":
    main()
