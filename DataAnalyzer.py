import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from MazeHierarchy import *
from DisplayRandomMaze import *
from DisplayResult import *

def plot_linear_regression():
    df = pd.read_csv("anketa.csv")

    X_list = df['fitness']
    y = df['grade']

    removed_outliers = y.between(y.quantile(.15), y.quantile(.85))

    X = []
    for num in X_list:
        X.append([num])

    reg = linear_model.LinearRegression()
    reg.fit(X, y)

    Y = reg.predict(X)

    plt.figure(figsize=(6, 4))
    plt.scatter(X, y, label='Data')
    plt.plot(X, Y, 'r')

    plt.ylim(1, 3)

    plt.xlabel('Prilagođenost')
    plt.ylabel('Prosečna ocena')

    #plt.show()

    plt.savefig('linreg.png')

def average_fitness(matrix):
    sum = 0
    num = 100
    for _ in range(num):
        maze = Maze(matrix)
        sum = sum + calculate_fitness(matrix)

    return float(sum) / num

def main():

    # f = open('logs/log2.txt', 'r')
    # contents = f.read()
    # f.close()
    #
    # matrix = parse_log(contents)
    #
    # print(average_fitness(matrix))

    plot_linear_regression()


if __name__ == "__main__":
    main()