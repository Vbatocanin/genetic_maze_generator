import numpy as np

class Chromosome:
    def __init__(self, matrix, fitness):
        self.matrix = matrix
        self.fitness = fitness

    def __str__(self):
        return str(self.matrix)

    def generate_maze(self):
        pass

n = 5
child1 = Chromosome(np.zeros((n, n)), 0)
child2 = Chromosome(np.zeros((n, n)), 0)
parent1 = Chromosome(np.random.rand(n, n), 0)
parent2 = Chromosome(np.random.rand(n, n), 0)

for i in range(n):
    for j in range(n):
        if (i < n/2 and j < n/2) or (i > n/2 and j > n/2):
            child1.matrix[i,j] = parent1.matrix[i,j]
            child2.matrix[i,j] = parent2.matrix[i,j]
        else:
            child1.matrix[i,j] = parent2.matrix[i,j]
            child2.matrix[i,j] = parent1.matrix[i,j]

print(child1.matrix)