import numpy as np
import random
import MazeHierarchy
from tqdm import tqdm


class Chromosome:
    def __init__(self, matrix, fitness):
        self.matrix = matrix
        self.fitness = fitness

    def __str__(self):
        return str(self.matrix)

    def generate_maze(self):
        pass


class GeneticAlgorithm:
    def __init__(self, n):
        self.generation_size = 5000
        self.chromosome_size = n  # maze size (n x n)
        self.reproduction_size = 1000
        self.max_iterations = 1000
        self.mutation_rate = 0.1
        self.tournament_size = 10

        self.selection_type = 'tournament'

    def fitness_DFS(self, curr_cell, finish_cell):
        """ calculates fitness """

        road_len = 0
        turns = 0
        steps_to_solution = 0

        if curr_cell.x == finish_cell.x and curr_cell.y == finish_cell.y:
            return road_len, turns, steps_to_solution, True

        total_road_len = 0
        total_turns = 0
        total_steps_to_solution = 0
        final_solution_found = False

        for path in curr_cell.paths:
            if not path.visited:
                path.visited = True
                path.parent = curr_cell
                [road_len, turns, steps_to_solution, solution_found] = self.fitness_DFS(path, finish_cell)
                total_steps_to_solution = total_steps_to_solution + steps_to_solution
                total_turns = total_turns + turns

                if curr_cell.parent:
                    incoming_direction = MazeHierarchy.Maze.getDirection(curr_cell.parent, curr_cell)
                    outgoing_direction = MazeHierarchy.Maze.getDirection(curr_cell, path)
                    if incoming_direction != outgoing_direction:
                        if not MazeHierarchy.Maze.isDirectionOpposite(incoming_direction, outgoing_direction):
                            total_turns = total_turns + 1

                if solution_found:
                    total_road_len = road_len + 1
                    final_solution_found = True

        total_steps_to_solution = total_steps_to_solution + 1

        return total_road_len, total_turns, total_steps_to_solution, final_solution_found

    def calculate_fitness(self, genetic_code):
        maze = MazeHierarchy.Maze(genetic_code)

        # TODO
        # max off-road steps
        # max number of turns
        # max steps for algorithms to find solutions
        maze.startCell.parent = None
        [road_len, turns, steps_to_solution, _] = self.fitness_DFS(maze.startCell, maze.finishCell)

        off_road_steps = self.chromosome_size ** 2 - road_len

        fitness_value = off_road_steps + turns + steps_to_solution

        return fitness_value

    def initial_population(self):
        init_population = []

        for _ in range(self.generation_size):
            n = self.chromosome_size
            matrix = np.random.rand(n, n)
            init_population.append(Chromosome(matrix, self.calculate_fitness(matrix)))

        return init_population

    def selection(self, chromosomes):
        selected = []

        for _ in range(self.reproduction_size):
            if self.selection_type == 'tournament':
                selected.append(self.tournament_selection(chromosomes))
            elif self.selection_type == 'roulette':
                selected.append(self.roulette_selection(chromosomes))

        return selected

    def roulette_selection(self, chromosomes):
        total_fitness = sum([chromosome.fitness for chromosome in chromosomes])

        selected_value = random.randrange(0, total_fitness)

        current_sum = 0
        for i in range(self.generation_size):
            current_sum += chromosomes[i].fitness

            if current_sum > selected_value:
                return chromosomes[i]

    def tournament_selection(self, chromosomes):
        selected = random.sample(chromosomes, self.tournament_size)

        winner = max(selected, key=lambda x: x.fitness)

        return winner

    def mutate(self, genetic_code):
        random_value = random.random()

        if random_value < self.mutation_rate:
            random_i = random.randrange(self.chromosome_size)
            random_j = random.randrange(self.chromosome_size)

            genetic_code.matrix[random_i][random_j] = np.random.rand()

        return genetic_code

    def create_generation(self, chromosomes):
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

        child1.fitness = self.calculate_fitness(child1.matrix)
        child2.fitness = self.calculate_fitness(child2.matrix)

        return child1, child2

    def optimize(self):
        population = self.initial_population()
        global_best_chromosome = None

        for _ in tqdm(range(0, self.max_iterations)):
            selected = self.selection(population)

            population = self.create_generation(selected)

            global_best_chromosome = max(population, key=lambda x: x.fitness)

            # print(global_best_chromosome)

            if global_best_chromosome.fitness == self.chromosome_size:
                break

        return global_best_chromosome


def main():
    genetic_algorithm = GeneticAlgorithm(9)
    result = genetic_algorithm.optimize()

    print(result.matrix)
    maze = MazeHierarchy.Maze(result.matrix)
    print(maze)


if __name__ == "__main__":
    main()
