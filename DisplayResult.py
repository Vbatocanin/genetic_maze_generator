from MazeHierarchy import *
from DisplayRandomMaze import *

def parse_log(contents):
    last_matrix = contents.split('\n\n')[-2]

    rows = last_matrix.split(']')
    matrix = []

    for row in rows:
        row = "".join(filter(lambda char: char != "]", row))
        row = "".join(filter(lambda char: char != "[", row))
        row = "".join(filter(lambda char: char != "\n", row))
        row = row.split(' ')
        row = [element for element in row if element]
        mat_row = [float(num) for num in row]
        if mat_row != []:
            matrix.append(mat_row)

    return matrix

def main():
    f = open('logs/log2.txt', "r")
    contents = f.read()
    f.close()

    matrix = parse_log(contents)

    fit = calculate_fitness(matrix)

    print("\n  Fitness: " + str(fit))

    #for row in matrix:
    #    print(row)

    print("\n\n")

    maze = Maze(matrix)

    print(str(maze))

if __name__ == "__main__":
    main()