from copy import copy
import izhikevich_neuron
import data_loader

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
def izzy_spike_time(population):
    trainingdata = data_loader.read_training_files(2)
    power = 2
    S_b = izhikevich_neuron.find_spikes(trainingdata, 0)

    for p in population:
        S_a = p.spikes
        sigma = 0
        dist = 0.0
        for t_ai, t_bi in zip(S_a, S_b):
            sigma += abs(t_ai - t_bi)**power
        nv = sigma**(1/power)
        if min(len(S_a),len(S_b)) == 0:
            nv += abs(len(S_a) - len(S_b))*1000
            dist = nv
        else:
            nv += abs(len(S_a) - len(S_b))*1000/min(len(S_a),len(S_b))
            dist = ( (1/min(len(S_a),len(S_b)))*nv )+1
        print S_a
        print S_b
        print "DISTANCE "+str(dist)
        fitness = 1/dist/dist
        print "Fitness "+str(fitness)
        p.set_fitness( fitness )

def izzy_spike_interval(self):
    pass

def izzy_waveform(self):
    pass