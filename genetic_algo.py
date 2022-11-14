from mlp import neural_network
from game import snake
import numpy as np

class genetic_algo(object):
    def __init__(self, size):
        self.size = size
        self.pop = [[0, neural_network()] for i in range(size)]
        self.snake = snake((255,0,0),(10,10))
        
    def compute_fitness(self, gen):
        for i, nn in enumerate(self.pop):
            print("gen" + str(gen) + " nn" + str(i))
            self.snake.play(1, nn[1])
            self.pop[i][0] = (self.snake.fitness_fun()[5])
        self.pop.sort(key=lambda x: x[0], reverse=True)

    def evoulation(self, gens = 20, top = 12):
        for j in range(1, gens+1):
            self.compute_fitness(j)
            max(self.pop, key=lambda x: x[0])[1].brain.save_weights('brains/gen'+str(j) + '.h5')
            print(max(self.pop, key=lambda x: x[0])[0])
            
            self.pop = self.pop[:top]
            while len(self.pop) != self.size:
                num1 = np.random.randint(low=0, high=top)
                num2 = np.random.randint(low=0, high=top)
                self.pop.append([0, self.crossover(self.pop[num1][1], self.pop[num2][1])])
            
            for i in range(self.size):
                self.pop[i][1] = self.mutate(p=self.pop[i][1])
        
    
    def mutate(self, prob = 0.05, p = neural_network()):
        w = np.array(p.brain.get_weights())
        for i in range(len(w)):
            if len(w[i].shape)==2:
                for j in range(w[i].shape[0]):
                    for k in range(w[i].shape[1]):
                        num = np.random.uniform()
                        if num<prob:
                            w[i][j][k] = np.random.uniform(low=-1, high=1)
            elif len(w[i].shape)==1:
                for j in range(w[i].shape[0]):
                    num = np.random.uniform()
                    if num<prob:
                        w[i][j] = np.random.uniform(low=-1, high=1)
        
        p.brain.set_weights(w)
        return p

    def crossover(self, p1 = neural_network(), p2 = neural_network()):
        w1 = np.array(p1.brain.get_weights())
        w2 = np.array(p2.brain.get_weights())
        child = neural_network()

        for i in range(len(w1)):
            # print(i, w1[i].shape, w1[i].shape[0])
            if len(w1[i].shape)==2:
                for j in range(w1[i].shape[0]):
                    for k in range(w1[i].shape[1]):
                        num = np.random.uniform()
                        if num<0.5:
                            w1[i][j][k] = w2[i][j][k]
            elif len(w1[i].shape)==1:
                for j in range(w1[i].shape[0]):
                    num = np.random.uniform()
                    if num<0.5:
                        w1[i][j] = w2[i][j]
        
        child.brain.set_weights(w1)

        return child

def main():
    # g = genetic_algo(20)
    # g.evoulation(20, 8)
    x = neural_network()
    x.brain.load_weights('brains/gen2.h5')
    s = snake((255,0,0),(10,10))
    s.play(brain=x)
main()
            