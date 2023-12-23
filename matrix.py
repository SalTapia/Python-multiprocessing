#!/usr/bin/env python
from random import randint
#import os
import multiprocessing
from  time import process_time
import sys
import math

# row = col = sample_size
row = 2
col = 2

Row = multiprocessing.Value('i',row)
Col = multiprocessing.Value('i',col)

a = [multiprocessing.Array('i',[0]*row)]*col
b  = [multiprocessing.Array('i',[0]*row)]*col
result = [multiprocessing.Array('i',[0]*row)]*col

lock = multiprocessing.Lock()

def printmatrix(c,m):
    print("\n")
    if m == 1:
        print("MATRIX A") 
    else:
        print("MATRIX B")
    
    for i in range(row):
        for j in range(col):
             print("",c[i][j],end="") 
        print('\n')   

def computematrix():
    lock.acquire()
    for i in range(Row.value):
        for j in range(Col.value):
            result[i][j] = 0
            for k in range(Col.value):
                result[i][j]+= (a[i][k]) * (b[k][j]) 
    lock.release()	
    exit(0)

def printresults():
    print("\n")    
    print("RESULTS")     
    for i in range(row):
        for j in range(col):
            print("",result[i][j],end="")
        print("\n")

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
    runs = (int)(sys.argv[1])

    if(runs < 3):
        print("ERROR: Argument must be 3 or greater to compute standard deviation\n")
        exit()
    sum_processtime = 0
    processtime = []

for _ in range(runs):

    for i in range(row):
        for j in range(col):
            a[i][j] = randint(0,10)
            b[i][j] = randint(0,10)  
    m = 1     
    printmatrix(a,m)
    m = 2
    printmatrix(b,m)
    
    start = process_time()
    processes = []
    for _ in range(4):
        t = multiprocessing.Process(target=computematrix)
        t.start()
        processes.append(t)

    for process in processes:
        process.join()

    end = process_time()

   #output to file
   # print(i,end="")
   # print(",",end-start)

    sum_processtime+= (end-start)
    processtime.append((end-start))
    printresults()
    
avgtime = (sum_processtime / runs)

print("Average process time for ", runs ," runs ","%.8f seconds." % avgtime)
computeStandardDiviation(processtime,runs)
