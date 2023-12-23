from random import randint
import os
import multiprocessing
import time
import sys
import math

pi = multiprocessing.Array('d',range(1))
n = multiprocessing.Value('i',10000) #n value

def estimatePI():
    RAND_MAX = 3276
    count = 0
    for i in range(n.value):
        
        x =  randint(0,RAND_MAX) / RAND_MAX 
        y =  randint(0,RAND_MAX) / RAND_MAX 
        z = x * x + y * y
        
        if z <= 1:
            count+=1
    
    pi[0] =  count / n.value * 4

def printResults():
    print("Approximate PI =",pi[0])

def computeStandardDiviation(processtime,runs):
    sum = 0
    mean = 0
    variant = 0.0 

    for i in range(runs):
        sum+= processtime[i]

    mean = sum/runs
    sum = 0
    for i in range(runs):
        for j in range(1):
            sum+= (((abs(processtime[i]-mean))) * (abs((processtime[i]-mean))))
            
    variant = (sum/(runs-1))
    
    print("Standard Deviation: %.8f" % math.sqrt(variant))
    print("Standard Error: %.8f" % (math.sqrt(variant)/math.sqrt(runs)))

if __name__ == "__main__":
    runs  = (int)(sys.argv[1])

    processes = []
    sum_processtime = 0
    processtime = []
    
    for i in range(runs):
        
        start = time.time()
        #100 processes
        for _ in range(1):
            t = multiprocessing.Process(target=estimatePI)
            t.start()
            processes.append(t)
        
        for process in processes:
            process.join()

        end = time.time()
        
        sum_processtime+= (end-start)
        processtime.append((end-start))

avgtime = (sum_processtime / runs)
print("Average process time for", runs ,"runs:","%.8f seconds." % avgtime)
computeStandardDiviation(processtime,runs)
printResults()
