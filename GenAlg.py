import numpy as np
import random
import MazeHierarchy
from tqdm import tqdm


class Chromosome:
    """ A class used to store chromosomes used in genetic algorithm. """

    def __init__(self, matrix, fitness):
        self.matrix = matrix
        self.fitness = fitness

    def __str__(self):
        return str(self.matrix)


class GeneticAlgorithm:
    def __init__(self, n):
        self.generation_size = 5000
        self.chromosome_size = n  # maze size (n x n)
        self.reproduction_size = 1000
        self.max_iterations = 1000
        self.mutation_rate = 0.1
        self.tournament_size = 10
        self.log = open("log.txt", "a+")
        self.log.truncate(0)
        self.log.close()

        self.selection_type = 'tournament'

    def fitness_DFS(self, curr_cell, finish_cell):
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
        for path in curr_cell.paths:
            if not path.visited:
                path.visited = True
                path.parent = curr_cell

                # recoursive call
                [road_len, turns, steps_to_solution, solution_found] = self.fitness_DFS(path, finish_cell)

                # adding all steps the algorithm had to take to get to a solution
                if not final_solution_found:
                    total_steps_to_solution = total_steps_to_solution + steps_to_solution

                # adding all the turns in the explored maze so far
                total_turns = total_turns + turns

                # if the current cell has a parent, check for turns and add them
                if curr_cell.parent:
                    incoming_direction = MazeHierarchy.Maze.getDirection(curr_cell.parent, curr_cell)
                    outgoing_direction = MazeHierarchy.Maze.getDirection(curr_cell, path)
                    if incoming_direction != outgoing_direction:
                        if not MazeHierarchy.Maze.isDirectionOpposite(incoming_direction, outgoing_direction):
                            total_turns = total_turns + 1

                # if the solution is found, this node is on the path to it, so add 1 to the path length
                if solution_found:
                    total_road_len = road_len + 1
                    final_solution_found = True

        # add a step for this node to the total number of steps it took to solve the maze
        total_steps_to_solution = total_steps_to_solution + 1

        return total_road_len, total_turns, total_steps_to_solution, final_solution_found

    def calculate_fitness(self, genetic_code):
        """ Calculates the fitness of a given probability matrix. """

        maze = MazeHierarchy.Maze(genetic_code)

        # maximizing off-road steps
        # maximizing number of turns
        # maximizing steps for algorithms to find solutions
        maze.startCell.parent = None
        [road_len, turns, steps_to_solution, _] = self.fitness_DFS(maze.startCell, maze.finishCell)

        off_road_steps = self.chromosome_size ** 2 - road_len

        fitness_value = 0.8*off_road_steps + turns + steps_to_solution

        return fitness_value

    def initial_population(self):
        """ Initializes a random population of Chromosomes. """

        init_population = []

        for _ in range(self.generation_size):
            n = self.chromosome_size
            matrix = np.random.rand(n, n)
            init_population.append(Chromosome(matrix, self.calculate_fitness(matrix)))

        return init_population

    def selection(self, chromosomes):
        """ Selects a reproduction_size number of high-fitness Chromosomes. """

        selected = []

        # picking selection type based on a predefined variable
        for _ in range(self.reproduction_size):
            if self.selection_type == 'tournament':
                selected.append(self.tournament_selection(chromosomes))
            elif self.selection_type == 'roulette':
                selected.append(self.roulette_selection(chromosomes))

        return selected

    def roulette_selection(self, chromosomes):
        """ Selects a Chromosome with a probability proportionate to its fitness. """

        total_fitness = sum([chromosome.fitness for chromosome in chromosomes])

        selected_value = random.randrange(0, total_fitness)

        current_sum = 0
        for i in range(self.generation_size):
            current_sum += chromosomes[i].fitness

            if current_sum > selected_value:
                return chromosomes[i]

    def tournament_selection(self, chromosomes):
        """ Selects the best Chromosome from a random sample. """

        selected = random.sample(chromosomes, self.tournament_size)

        winner = max(selected, key=lambda x: x.fitness)

        return winner

    def mutate(self, genetic_code):
        """" Changes one probability in a chromosome. """

        random_value = random.random()

        if random_value < self.mutation_rate:
            random_i1 = random.randrange(self.chromosome_size)
            random_j1 = random.randrange(self.chromosome_size)

            random_i2 = random.randrange(self.chromosome_size)
            random_j2 = random.randrange(self.chromosome_size)

            if random_i1 > random_i2:
                random_i1, random_i2 = random_i2, random_i1

            if random_j1 > random_j2:
                random_j1, random_j2 = random_j2, random_j1

            for i in range(random_i1, random_i2):
                for j in range(random_j1, random_j2):
                    genetic_code.matrix[i][j] = np.random.rand()

        return genetic_code

    def create_generation(self, chromosomes):
        """ Advances the evolution by one generaiton. """

        generation = []
        generation_size = 0

        while generation_size < self.generation_size:
            [parent1, parent2] = random.sample(chromosomes, 2)

            child1, child2 = self.crossover(parent1, parent2)

            child1 = self.mutate(child1)
            child2 = self.mutate(child2)

            child1.fitness = self.calculate_fitness(child1.matrix)
            child2.fitness = self.calculate_fitness(child2.matrix)

            generation.append(child1)
            generation.append(child2)

            generation_size += 2

        return generation

    def crossover(self, parent1, parent2):
        """ Crosses over two probability matrices by separating them into quadrants
        and switching two of the submatrices. """

        n = self.chromosome_size
        child1 = Chromosome(np.zeros((n, n)), 0)
        child2 = Chromosome(np.zeros((n, n)), 0)

        for i in range(n):
            for j in range(n):
                if (i < n / 2 and j < n / 2) or (i > n / 2 and j > n / 2):
                    child1.matrix[i, j] = parent1.matrix[i, j]
                    child2.matrix[i, j] = parent2.matrix[i, j]
                else:
                    child1.matrix[i, j] = parent2.matrix[i, j]
                    child2.matrix[i, j] = parent1.matrix[i, j]

        # child1.fitness = self.calculate_fitness(child1.matrix)
        # child2.fitness = self.calculate_fitness(child2.matrix)

        return child1, child2

    def optimize(self):
        """ Runs the genetic algorithm. """

        population = self.initial_population()
        global_best_chromosome = None

        for _ in tqdm(range(0, self.max_iterations)):
            self.log = open("log.txt", "a+")

            selected = self.selection(population)

            population = self.create_generation(selected)

            global_best_chromosome = max(population, key=lambda x: x.fitness)

            self.log.write(str(global_best_chromosome.matrix)+'\n\n')

            if global_best_chromosome.fitness == self.chromosome_size:
                break

            self.log.close()

        return global_best_chromosome


def main():
    genetic_algorithm = GeneticAlgorithm(8)
    result = genetic_algorithm.optimize()

    print(result.matrix)
    maze = MazeHierarchy.Maze(result.matrix)
    print(maze)


if __name__ == "__main__":
    main()
