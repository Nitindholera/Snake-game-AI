from mlp import neural_network
from game import snake

class genetic_algo(object):
    def __init__(self, size):
        self.pop = [[neural_network(), 0] for i in range(size)]
        self.snake = snake((255,0,0),(10,10))
    
    def compute_fitness(self):
        for i, nn in enumerate(self.pop):
            self.snake.play(1, nn[0])
            self.pop[i][1] = (self.snake.fitness_fun())
        self.pop.sort()

def main():
    g = genetic_algo(50)
    g.compute_fitness() 
main()
            