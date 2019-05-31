import matplotlib.pyplot as plt
import numpy as np
import random

def InitFirstPopulation(Queens, Solutions):
    Population = np.zeros([Solutions, Queens + 1])
    
    for j in range(0, Solutions):        
        for i in range(0, Queens):            
            value = random.randint(1, Queens)
            while(1 == 1):
                if value in Population[j] :
                    value = random.randint(1, Queens)
                else:
                    Population[j, i] = value
                    break

    return Population    

def CostFunctionAll(Solutions):   
    for i in range(0 , len(Solutions)):       
        Solutions[i, 8] = CostFunction(Solutions[i])
        
    B = np.array(Solutions)
    return np.array(sorted(B, key=lambda x :x[-1]))

def CostFunction(Chromosome):
    Threats = 0
    Queens = len(Chromosome) - 1
        
    for i in range(0 , Queens):                
        value = Chromosome[i]
        for j in range(i + 1, Queens):
            #line Threats
            if(value == Chromosome[j] and j != i):
                Threats = Threats + 1               
            
            #Cross Threats
            if(abs(j - i) + value == Chromosome[j]):                
                Threats = Threats + 1               
            
            #Cross Threats
            if(abs(abs(j - i) - value) == Chromosome[j]):                
                Threats = Threats + 1               
    return Threats

def CrossOver(Population, NewPopulation):
    p1 = Population[random.randint(0, 99),:8]
    p2 = Population[random.randint(0, 99),:8]    
    
    ch1 = np.zeros(8)
    ch2 = np.zeros(8)
       
    ch1[0] = p1[0]
    ch1[1] = p1[1]
    ch1[2] = p1[2]
    ch1[3] = p1[3]
    for i in range(4, 8):        
        for j in range(0, 8):
            val = p2[j]
            if val not in ch1:
                ch1[i] = val        
       
    ch1 = np.append(ch1, [0])
    ch1[8] = CostFunction(ch1)
    
    ch2[7] = p1[7]
    ch2[6] = p1[6]
    ch2[5] = p1[5]
    ch2[4] = p1[4]
    for i in range(0, 4):
        for j in range(0 , 8):
            val = p1[j]
            if val not in ch2:
                ch2[i] = val    
    
    ch2 = np.append(ch2, [0])
    ch2[8] = CostFunction(ch2)
    
    for i in range(0, len(NewPopulation)):            
        if(NewPopulation[i] is None):
            NewPopulation[i] = ch1
            break
        
    for j in range(0, len(NewPopulation)):    
        if(NewPopulation[j] is None):
            NewPopulation[j] = ch2
            break
    
    return NewPopulation

def Mutation(Population, NewPopulation):
    
    p1 = Population[random.randint(0, 99)]
    
    point1 = random.randint(0, 3)
    point2 = random.randint(4, 7)

    ch1 = p1
    v1 = ch1[point1] 
    v2 = ch1[point2] 
    ch1[point1] = v2
    ch1[point2] = v1
    
    ch1[8] = CostFunction(ch1)
    
    for i in range(0, len(NewPopulation)):    
        if(NewPopulation[i] is None):
            NewPopulation[i] = ch1
            break
    
    return NewPopulation 

Queens = 8
NumberOfSolutions = 100
Solutions = InitFirstPopulation(Queens, NumberOfSolutions)
Solutions = CostFunctionAll(Solutions)    
CrossOverNumber = 40
MutationNumber = 30
NewPopulationNumber = 110
Epochs = 100
BestSolutions = [None] * Epochs
AVGSolutions = [None] * Epochs
AllSolutions = [None] * Epochs
AllSolutions[0] = Solutions
BestSolutions[0] = Solutions[0,8]
AVGSolutions[0] = np.average(Solutions[:,8])

for i in range(1, Epochs):    
    LatestPopulation = AllSolutions[i-1]
    NewPopulation = [None] * NewPopulationNumber

    #CrossOver
    for j in range(0 , CrossOverNumber):        
        NewPopulation = CrossOver(LatestPopulation, NewPopulation)             
        
    #Mutation
    for j in range(0 , MutationNumber):        
        NewPopulation = Mutation(LatestPopulation, NewPopulation)
            
    Temp = np.array(sorted(NewPopulation, key=lambda x :x[-1]))
    
    NewGeneration = Temp[:100,:]    
    AllSolutions[i] = NewGeneration
    BestSolutions[i] = NewGeneration[0,8]
    AVGSolutions[i] = np.average(NewGeneration[:,8])
    if(BestSolutions[i] == 0):
        print('Solution : ' + str(NewGeneration[0]))
        print('Generation : ' + str(i))
        break

plt.plot(BestSolutions)
plt.title('Best Cost In Each Generation')
plt.show()

plt.plot(AVGSolutions)
plt.title('Average Cost In Each Generation')
plt.show()
