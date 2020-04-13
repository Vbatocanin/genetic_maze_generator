from MazeHierarchy import *


def main():
    f = open('log.txt', "r")
    contents = f.read()
    f.close()

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
        print(mat_row)
        if mat_row != []:
            matrix.append(mat_row)

    print(matrix)

    maze = Maze(matrix)

    print(str(maze))

if __name__ == "__main__":
    main()