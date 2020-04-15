import numpy as np
from MazeHierarchy import *


def fitness_A_star(curr_cell, finish_cell):
    """ Fully searches the maze to calculate several fitness-relataed values. """

    road_len = 0
    turns = 0
    steps_to_solution = 0

    # if we've reached the finish cell, nothing more to do
    if curr_cell.x == finish_cell.x and curr_cell.y == finish_cell.y:
        return road_len, turns, steps_to_solution, True

    total_road_len = 0
    total_turns = 0
    total_steps_to_solution = 0
    final_solution_found = False

    # for every unvisited neighbor
    sorted_neighbors = sorted(curr_cell.paths,
                              key=lambda cell: abs(cell.x - finish_cell.x) + abs(cell.y - finish_cell.y))

    for path in sorted_neighbors:
        if not path.visited:
            path.visited = True
            path.parent = curr_cell

            # recoursive call
            [road_len, turns, steps_to_solution, solution_found] = fitness_A_star(path, finish_cell)

            # adding all steps the algorithm had to take to get to a solution
            if not final_solution_found:
                total_steps_to_solution = total_steps_to_solution + steps_to_solution

            # adding all the turns in the explored maze so far
            total_turns = total_turns + turns

            # if the current cell has a parent, check for turns and add them
            if curr_cell.parent:
                incoming_direction = Maze.get_direction(curr_cell.parent, curr_cell)
                outgoing_direction = Maze.get_direction(curr_cell, path)
                if incoming_direction != outgoing_direction:
                    if not Maze.is_direction_opposite(incoming_direction, outgoing_direction):
                        total_turns = total_turns + 1

            # if the solution is found, this node is on the path to it, so add 1 to the path length
            if solution_found:
                total_road_len = road_len + 1
                final_solution_found = True

    # add a step for this node to the total number of steps it took to solve the maze
    total_steps_to_solution = total_steps_to_solution + 1

    return total_road_len, total_turns, total_steps_to_solution, final_solution_found


def calculate_fitness(genetic_code):
    """ Calculates the fitness of a given probability matrix. """

    n = len(genetic_code)

    maze = Maze(genetic_code)

    # maximizing off-road steps
    # maximizing number of turns
    # maximizing steps for algorithms to find solutions
    maze.start_cell.parent = None
    [road_len, turns, steps_to_solution, _] = fitness_A_star(maze.start_cell, maze.finish_cell)

    off_road_steps = n ** 2 - road_len

    fitness_value = 0.8 * off_road_steps + turns + steps_to_solution

    return fitness_value

def main():
    n = 8

    matrix = np.random.rand(n, n)

    fit = calculate_fitness(matrix)

    print("\n  Fitness: " + str(fit) + "\n\n")

    maze = Maze(matrix)
    print(maze)

if __name__ == "__main__":
    main()