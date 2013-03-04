from copy import copy
import izhikevich_neuron
from data_loader import read_training_files
import math

#Class for evaluation the fitness of a given phenotuype.

def one_max_fitness(population):
    goal_bits = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    print goal_bits
    for individual in population:
        fitness = 0
        for p,g in zip(individual.phenotype, goal_bits):
            if p==g:
                fitness += 1
        individual.set_fitness(fitness)

#Receives list of a population of blotto strategies, pits every commanders against
#each other, awards fitness points when winning war against another commander
def blotto_fitness(population):
    for p in population:
        p.reset_fitness()
    population_copy = copy(population)
    for commander in population:
        population_copy.remove(commander)
        for opposing_commander in population_copy:
            
            #Execute a WAR!
            points_commander = 0
            points_opponent = 0
            battle_nr = 0
            for i,j in zip(commander.phenotype, opposing_commander.phenotype):
                i = i*commander.get_strength()
                j = j*opposing_commander.get_strength()

                if i>j:
                    points_commander+=2
                    commander.re_deploy(battle_nr, i-j)
                    opposing_commander.decrement_strength()
                if i<j:
                    points_opponent+=2
                    opposing_commander.re_deploy(battle_nr, j-i)
                    commander.decrement_strength()
                battle_nr += 1
                
            #WAR done, increment fitness of winner based on points
            if points_commander>points_opponent:
                commander.increment_fitness(2)
            if points_commander<points_opponent:
                opposing_commander.increment_fitness(2)
            if points_commander==points_opponent:
                commander.increment_fitness(1)
                opposing_commander.increment_fitness(1)
            commander.reset()
            opposing_commander.reset()
            
#3 different fitness calculations: 
#Spike Time
#Spike Interval
#Waveform
trainingdata = read_training_files()
def izzy_spike_time(population):
    power = 2
    S_b = izhikevich_neuron.find_spikes(trainingdata, 0)
    
    for p in population:
        S_a = p.spikes
        
        N = min(len(S_a),len(S_b))
        if N == 0:
            p.set_fitness(0)
            continue
        
        sigma = 0
        for t_ai, t_bi in zip(S_a, S_b):
            sigma += abs(t_ai - t_bi)**power
        
        nv = sigma ** (power ** -1)
        dist = nv/N
        
        print "DISTANCE "+str(dist)
        p.set_distance( dist )
        fitness = (1.0/dist)*1000
        print "Fitness "+str(fitness)
        p.set_fitness( fitness )

def izzy_spike_interval(population):
    power = 4
    S_b = izhikevich_neuron.find_spikes(trainingdata, 0)
    for p in population:
        S_a = p.spikes
        
        N = min(len(S_a), len(S_b))
        
        if N <= 1:
            p.set_fitness(0)
            continue
        
        sigma = 0
        for i in range(1, N):
            sigma += abs((S_a[i] - S_a[i-1]) - (S_b[i] - S_b[i-1]))**power
        
        distance = sigma ** (power ** -1) / (N - 1)
        print "DISTANCE", distance
        fitness = (1 / distance) * 1000
        print "Fitness", fitness
        p.set_fitness(fitness)

def izzy_waveform(population):
    power = 2
    for p in population:
        st = p.spiketrain
        td = trainingdata
        
        tsum = 0
        for va,vb in zip(st, td):
            tsum += (va-vb)**power
        tsum = tsum**(power**-1)
        tsum /= 1001
        print "Distance", tsum
        print "Fitness", 1/tsum
        p.set_fitness( 1/tsum )
