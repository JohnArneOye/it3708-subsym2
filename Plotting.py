import matplotlib.pyplot as plt
import numpy as np
import math

class Plotting:
    ea = None
    
    def __init__(self, ea):
        self.ea = ea
        # [[ max_fitness, avg_fitness, std_deviation ]]
        self.generation = []
        self.max_fitness = []
        self.avg_fitness = []
        self.std_deviation = []
        
    def plot(self):
        
        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.generation, self.max_fitness, self.generation, self.avg_fitness)
        plt.ylabel("Max and average fitness")
        
        plt.subplot(212)
        plt.plot(self.generation, self.std_deviation)
        plt.ylabel("Standard deviation")
        plt.show()
    
    def update(self):
        self.generation.append(self.ea.generation)
        self.max_fitness.append(self.ea.best_individual.fitness)
        self.avg_fitness.append(self.ea.avg_fitness)
        self.std_deviation.append(self.ea.std_deviation)

class Blotting:
    
    def __init__(self, ea):
        self.ea = ea
        self.generation = []
        self.max_fitness = []
        self.avg_fitness = []
        self.std_deviation = []
        self.avg_entropy = []
        
        
    def plot(self):
        plt.figure(1)
        plt.subplot(311)
        plt.plot(self.generation, self.max_fitness, self.generation, self.avg_fitness)
        plt.ylabel("Max and average fitness")
        
        plt.subplot(312)
        plt.plot(self.generation, self.std_deviation)
        plt.ylabel("Standard deviation")
        
        plt.subplot(313)
        plt.plot(self.generation, self.avg_entropy)
        plt.ylabel("Average entropy")
        plt.show()
    
    def update(self):
        self.generation.append(self.ea.generation)
        self.max_fitness.append(self.ea.best_individual.fitness)
        self.avg_fitness.append(self.ea.average_fitness)
        self.std_deviation.append(self.ea.std_deviation)
        entropy = []
        for individual in self.ea.population:
            individual_entropy = 0
            for i in individual.phenotype:
                if not i==0:
                    individual_entropy += ( i*math.log(i,2) )
            entropy.append( -individual_entropy)
        self.avg_entropy.append(sum(entropy)/len(entropy))

class NeuroPlot:
    
    def __init__(self, ea):
        pass
    
    def update(self):
        pass
    
    def plot(self):
        pass
    
    #Take in a izzy neuron and plot the spike train and the spikes and stuff
    def plot_neuron(self):
        pass