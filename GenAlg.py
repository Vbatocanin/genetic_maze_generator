import numpy as np
import MazeHierarchy

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

    def calculate_fitness(self, genetic_code):
        fitness_value = 0

        # TODO
        # off-road steps
        # number of turns
        # steps for algorithms to find solutions

        return fitness_value

    def initial_population(self):
        init_population = []

        for _ in self.generation_size:
            matrix = np.random.rand(n, n)
            init_population.append(Chromosome(matrix, self.calculate_fitness(matrix)))

        return init_population

    def selection(self, chromosomes):
        selected = []

        # TODO

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
        pass

    def create_generation(self, chromosomes):
        generation = []
        generation_size = 0

        while generation_size < self.generation_size:
            [parent1, parent2] = random.sample(chromosomes, 2)

            child1_code, child2_code = self.crossover(parent1, parent2)

            child1_code = self.mutate(child1_code)
            child2_code = self.mutate(child2_code)

            child1 = Chromosome(child1_code, self.calculate_fitness(child1_code))
            child2 = Chromosome(child2_code, self.calculate_fitness(child2_code))

            generation.append(child1)
            generation.append(child2)

            generation_size += 2

        return generation

    def crossover(self, parent1, parent2):
        pass
        # return (child1, child2)

    def optimize(self):
        population = self.initial_population()

        for i in range(0, self.max_iterations):
            selected = self.selection(population)

            population = self.create_generation(selected)

            global_best_chromosome = max(population, key=lambda x: x.fitness)

            # print(global_best_chromosome)

            if global_best_chromosome.fitness == self.chromosome_size:
                break

        return global_best_chromosome