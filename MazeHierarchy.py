import numpy as np
import GenAlg
import random

class Cell:
    def __init__(self):

        # Indicators if a wall exists in a certain direction
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.visited = False

class Maze:
    def __init__(self,matrix):

        self.maze = []
        self.cells = []
        self.rowNo = len(matrix)
        self.colNo = len(matrix[0])

        # Initialization of complete maze
        for i in range(0, self.rowNo):
            self.maze.append([])
            for j in range(0,self.colNo):
                self.maze[i].append(Cell())

        self.generateMaze(matrix)

    def getCell(self,i,j):
        return self.maze[i][j]

    def isVisited(self,i,j):
        return self.maze[i][j].visited

    def generateMaze(self,matrix):
        # Generation of maze entrance
        self.startY = random.randint(0,len(matrix)-1)
        self.startX = random.randint(0, len(matrix[0])-1)

        # Generation of maze exit
        self.finishY = random.randint(0, len(matrix) - 1)
        self.finishX = random.randint(0, len(matrix[0]) - 1)

        # Initialization of current position
        curX = self.startX
        curY = self.startY

        # Number of Cells not yet visited
        noNotVisited = len(matrix)*len(matrix[0])


        while(noNotVisited>0):

            contenders = []
            if (curX!=0):
                if (self.isVisited(curX-1,curY)):
                    contenders.append([curX-1,curY])
            if (curX!=self.colNo-1):
                if (self.isVisited(curX+1,curY)):
                    contenders.append([curX+1,curY])
            if (curY!=0):
                if (self.isVisited(curX,curY-1)):
                    contenders.append([curX,curY-1])
            if (curX!=self.rowNo-1):
                if (self.isVisited(curX,curY+1)):
                    contenders.append([curX,curY+1])

            bestContender = contenders[0]
            nextIsChosen = False
            while(not nextIsChosen):
                for contender in contenders:
                    if( matrix[ contender[0],contender[1] ] > matrix[ bestContender[0],bestContender[1] ] ):
                        bestContender = contender
                r = random.random()
                if(r < matrix[ bestContender[0],bestContender[1] ]):
                    nextIsChosen = True
                else:
                    contenders.remove(bestContender)
            # bestContender

