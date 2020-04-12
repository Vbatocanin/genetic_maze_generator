import numpy as np
import random
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

            child1_code, child2_code = self.crossover(parent1, parent2)

            child1_code = self.mutate(child1_code)
            child2_code = self.mutate(child2_code)

            child1 = child1_code
            child1.fitness = self.calculate_fitness(child1_code)
            child2 = child2_code
            child2.fitness = self.calculate_fitness(child2_code)

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
                if (i < n/2 and j < n/2) or (i > n/2 and j > n/2):
                    child1.matrix[i, j] = parent1.matrix[i, j]
                    child2.matrix[i, j] = parent2.matrix[i, j]
                else:
                    child1.matrix[i, j] = parent2.matrix[i, j]
                    child2.matrix[i, j] = parent1.matrix[i, j]
        
        child1.fitness = self.calculate_fitness(child1.matrix)
        child2.fitness = self.calculate_fitness(child2.matrix)

        return (child1, child2)

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


def main():
    genetic_algorithm = GeneticAlgorithm(5)
    result = genetic_algorithm.optimize()
    print('Result: {}'.format(result))


if __name__ == "__main__":
    main()
