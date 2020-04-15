import numpy as np
import GenAlg
import random
from enum import Enum
from random import shuffle


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NO_DIRECTION = 4


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
        self.n_cols = len(probMatrix[0])
        self.n_rows = len(probMatrix)

        # Generation of start and exit node
        # [self.exitX, self.exitY] = self.generateEdge(self.nCols, self.nRows)
        [self.exit_x, self.exit_y] = [self.n_cols - 1, 0]
        # [self.startX, self.startY] = self.generateEdge(self.nCols, self.nRows)
        [self.start_x, self.start_y] = [0, self.n_rows - 1]

        # Re-generate start in case start and finish nodes are one and the same
        while [self.exit_x, self.exit_y] == [self.start_x, self.start_y]:
            [self.start_x, self.start_y] = self.generate_edge(self.n_cols, self.n_rows)

        # cellMaze is a list of lists which contains Cell objects in the same order as the prob matrix
        self.cell_maze = []

        # Initialization of complete maze
        for i in range(0, self.n_rows):
            self.cell_maze.append([])
            for j in range(0, self.n_cols):
                self.cell_maze[i].append(Cell(j, i))

        self.start_cell = self.get_cell(self.start_x, self.start_y)
        self.finish_cell = self.get_cell(self.exit_x, self.exit_y)
        self.generate_maze(probMatrix)

        for row in self.cell_maze:
            for cell in row:
                cell.setVisited(False)
                shuffle(cell.paths)

    # Generates the coordiantes for an edge Cell, which is only used for the start and finish cells
    def generate_edge(self, n_cols, n_rows):
        # Chance of it being on the left-right or the up-down edges
        p = 0.5
        r = random.randint(0, 1)
        if r < p:
            # Same princible, just for left or right
            r = random.randint(0, 1)
            if r < p:
                return [n_cols - 1, random.randint(0, n_rows - 1)]
            else:
                return [0, random.randint(0, n_rows - 1)]
        else:
            # Same princible, just for up or down
            r = random.randint(0, 1)
            if r < p:
                return [random.randint(0, n_cols - 1), n_rows - 1]
            else:
                return [random.randint(0, n_cols - 1), 0]

    def __str__(self):

        # █ indicate a wall
        # Blank spaces indicate free space

        # List of lists which contain characters, the coordinates correspond to the original maze
        # but with padding, which means (stringMatrixX, stringMatrixY) -> (mazeX * 2 + 1, mazeY * 2 + 1)
        string_matrix = []
        for i in range(0, 2 * self.n_rows + 1):
            string_matrix.append([])
            for j in range(0, 2 * self.n_cols + 1):
                if i % 2 == 0 or j % 2 == 0:
                    string_matrix[i].append('█')
                else:
                    string_matrix[i].append(' ')

        # Adding a blank space as an entrance to the maze
        if self.start_x == 0:
            string_matrix[self.start_y * 2 + 1][self.start_x * 2] = ' '
        elif self.start_y == 0:
            string_matrix[self.start_y * 2][self.start_x * 2 + 1] = ' '
        elif self.start_x == self.n_cols - 1:
            string_matrix[self.start_y * 2 + 1][self.start_x * 2 + 2] = ' '
        elif self.start_y == self.n_rows - 1:
            string_matrix[self.start_y * 2 + 2][self.start_x * 2 + 1] = ' '

        # Adding a blank space as an exit from the maze
        if self.exit_x == 0:
            string_matrix[self.exit_y * 2 + 1][self.exit_x * 2] = ' '
        elif self.exit_y == 0:
            string_matrix[self.exit_y * 2][self.exit_x * 2 + 1] = ' '
        elif self.exit_x == self.n_cols - 1:
            string_matrix[self.exit_y * 2 + 1][self.exit_x * 2 + 2] = ' '
        elif self.exit_y == self.n_rows - 1:
            string_matrix[self.exit_y * 2 + 2][self.exit_x * 2 + 1] = ' '

        # Drawing the actual hallways from Cell to Cell
        for row in self.cell_maze:
            for cell in row:
                curX = 2 * cell.x + 1
                curY = 2 * cell.y + 1

                for neighbor in cell.paths:
                    tmp_direction = self.get_direction(cell, neighbor)
                    if tmp_direction == Direction.UP:
                        string_matrix[curY - 1][curX] = ' '
                    elif tmp_direction == Direction.LEFT:
                        string_matrix[curY][curX - 1] = ' '

        # Final string generatrion
        final_string = ""
        for char_list in string_matrix:
            final_string += "  " + "".join(char_list) + "\n"
        return final_string

    # A function that return the direction in which you need to go
    # in order to go from fromCell to toCell
    @staticmethod
    def get_direction(from_cell, to_cell):
        diffx = to_cell.x - from_cell.x
        diffy = to_cell.y - from_cell.y

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
    def is_direction_opposite(dir1, dir2):
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

    def get_cell(self, x, y):
        return self.cell_maze[y][x]

    def is_visited(self, i, j):
        return self.cell_maze[j][i].visited


    # Makes a path from parentCell to childCell according
    # to their coordinates
    def make_path(self, parent_x, parent_y, child_x, child_y):
        child = self.get_cell(child_x, child_y)
        parent = self.get_cell(parent_x, parent_y)
        child.parent = parent
        child.setVisited(True)
        parent.paths.append(child)
        child.paths.append(parent)

    def generate_maze(self, prob_matrix):
        # Generation of maze entrance
        # print("Maze dimensions:", self.nCols, "x", self.nRows)
        # print("Starting from cell:", self.startCell.x, ",", self.startCell.y)
        # Initialization of current position
        self.start_cell.setVisited(True)
        cur_cell = self.start_cell

        # List of contenders that are not initially optimal but will be chosen after the fact
        # when the current cell is cornered
        global_contenders = []

        # This while loop adds potetial contenders which are adjacent to the current Cell
        while True:
            did_global_search = False
            local_contenders = []

            if (cur_cell.x != 0) and not self.is_visited(cur_cell.x - 1, cur_cell.y):
                tmp_cell = self.get_cell(cur_cell.x - 1, cur_cell.y)
                local_contenders.append(tmp_cell)
                # print("Making path from:", cur_cell.x, cur_cell.y, " To:", cur_cell.x - 1, cur_cell.y)
                self.set_parent(cur_cell.x, cur_cell.y, cur_cell.x - 1, cur_cell.y)


            if (cur_cell.x != self.n_cols - 1) and not self.is_visited(cur_cell.x + 1, cur_cell.y):
                tmp_cell = self.get_cell(cur_cell.x + 1, cur_cell.y)
                local_contenders.append(tmp_cell)
                # print("Making path from:", cur_cell.x, cur_cell.y, " To:", cur_cell.x + 1, cur_cell.y)
                self.set_parent(cur_cell.x, cur_cell.y, cur_cell.x + 1, cur_cell.y)

            if (cur_cell.y != 0) and not self.is_visited(cur_cell.x, cur_cell.y - 1):
                tmp_cell = self.get_cell(cur_cell.x, cur_cell.y - 1)
                local_contenders.append(tmp_cell)
                # print("Making path from:", cur_cell.x, cur_cell.y, " To:", cur_cell.x, cur_cell.y - 1)
                self.set_parent(cur_cell.x, cur_cell.y, cur_cell.x, cur_cell.y - 1)

            if (cur_cell.y != self.n_rows - 1) and not self.is_visited(cur_cell.x, cur_cell.y + 1):
                tmp_cell = self.get_cell(cur_cell.x, cur_cell.y + 1)
                local_contenders.append(tmp_cell)
                # print("Making path from:", cur_cell.x, cur_cell.y, " To:", cur_cell.x, cur_cell.y + 1)
                self.set_parent(cur_cell.x, cur_cell.y, cur_cell.x, cur_cell.y + 1)

            # In case there weren't any new Cells, return, because the maze is done
            if not local_contenders:
                did_global_search = True
                if not global_contenders:
                    return
                # If there are still Cells left, but which aren't adjacent,
                # fetch the one with the best probability attribute

                localBestContender = max(global_contenders, key=lambda con: prob_matrix[con.y][con.x])
                global_contenders.remove(localBestContender)
                # The next Cell to visit is already chosed
                next_is_chosen = True
            else:
                # In Case there are new adjacent Cells, find the best one with the given probability parameter
                localBestContender = local_contenders[0]
                next_is_chosen = False

            # Take the current Cell with the probability from the probMatrix
            # If it misses on the first Cell, picks the next best cell according to prob parameter
            while not next_is_chosen:
                if len(local_contenders) == 1:
                    localBestContender = local_contenders[0]
                    next_is_chosen = True
                    break
                localBestContender = max(local_contenders, key=lambda con: prob_matrix[con.y][con.x])
                r = random.random()
                if r < prob_matrix[localBestContender.y][localBestContender.x]:
                    next_is_chosen = True
                    local_contenders.remove(localBestContender)
                else:
                    try:
                        global_contenders.append(localBestContender)
                        local_contenders.remove(localBestContender)
                    except ValueError:
                        pass

            # Adds the unused Cells to the global list, which accumulates all the not-currently-adjacent Cells
            if local_contenders:
                global_contenders.extend(local_contenders)
            if did_global_search:
                cur_cell = localBestContender.parent

            # Mark the chosen best contender as visited
            self.make_path(cur_cell.x, cur_cell.y, localBestContender.x, localBestContender.y)
            cur_cell = localBestContender
            cur_cell.setVisited(True)
            # print("Cur x,y :", localBestContender.x, ",", localBestContender.y)

    def set_parent(self, parent_x, parent_y, child_x, child_y):
        child = self.get_cell(child_x, child_y)
        parent = self.get_cell(parent_x, parent_y)
        child.parent = parent



def main():
    prob_matrix_example = [[0.4, 0.1, 0.2], [0.6, 0.2, 0.26], [0.42, 0.31, 0.52]]
    maze_example = Maze(prob_matrix_example)
    print(maze_example)
    print("Done")


if __name__ == "__main__":
    main()
