"""
Module for implementing Simulated Annealing algorithm 
"""
import random
import math
##import numpy as np
##from mpl_toolkits.mplot3d import Axes3D
##import matplotlib.pyplot as plt
##from matplotlib import cm



#Given Functions
def Sphere(x,y):
    return (x**2)+(y**2)
def Rosenbrock(x,y):
    return 100*((y-(x**2))**2)+(1-x)**2
def Griewank(x,y):
    return (((x**2) + (y**2))/4000)-math.cos(x)*math.cos(y/math.sqrt(2))+1


#Finding Neighbor
def Neighbor(func,x,y,limits,step):
    val=[(x+step,y),(x,y+step),(x+step,y+step),(x-step,y),(x,y-step),(x-step,y-step),(x+step,y-step),(x-step,y+step)]
    newVal=[]
    for i in val:
        if i[0]>=limits[0] and i[0]<=limits[1] and i[1]>=limits[2] and i[1]<=limits[3]:
            newVal.append(i)
    solutions=[]
    for i in range(len(newVal)):
        solutions.append(func(newVal[i][0],newVal[i][1]))
    index=random.randint(0,len(solutions)-1)
    return round(newVal[index][0],2),round(newVal[index][1],2)


#Annealing
def SimulatedAnnealing(func,limits,step=0.1,minMax="maxima"):
        
    temperature = 1000
    stopTemp = 0.0000000000001
    alpha = 0.9
    x=round(random.uniform(limits[0],limits[1]),2)
    y=round(random.uniform(limits[2],limits[3]),2)
    currentState=func(x,y)
    delta=0
    newState=0
    values=set()
    #Runs loop until the temperature drops
    while temperature > stopTemp:
        for i in range(10):
            x1,y1=Neighbor(func,x,y,limits,step) 
            newState=func(x1,y1)
            delta=newState-currentState
            values.add((x,y))
            #For maxima
            if minMax=="maxima":
                if delta > 0:
                    currentState = newState
                    x,y=x1,y1
                else:
                    p=random.uniform(0,1)
                    m=math.exp(delta/temperature)
                    if p<m:
                        currentState=newState
                        x,y=x1,y1
            #For minima
            else:
                if delta < 0:
                    currentState = newState
                    x,y=x1,y1
                else:
                    p=random.uniform(0,1)
                    m=math.exp(-delta/temperature)
                    if p<m:
                        currentState=newState
                        x,y=x1,y1
                
            temperature = temperature * alpha
    return (currentState,x,y)

limits=[-5,5,-5,5]
val=SimulatedAnnealing(Sphere,limits,0.1,"maxima")
print(val)
###to plot 3d figure
##fig = plt.figure()
##axes = fig.gca(projection='3d')
###np.arrange creates an nd-array
##X = np.arange(limits[0], limits[1])
##Y = np.arange(limits[2], limits[3])
##X, Y = np.meshgrid(X, Y)
##
##graph = axes.plot_surface(X, Y, Rosenbrock(X, Y),alpha=0.3,color='b')
##count=0
##for coordinate in val[3]:
##        axes.scatter(coordinate[0], coordinate[1], Rosenbrock(coordinate[0], coordinate[1]), s= 30, c='yellow')
##    
##plt.show()

'''
Referred to pseudocode of SimulatedAnnealing in lecture slides
For the 3d graph referred to the following link
https://matplotlib.org/examples/mplot3d/surface3d_demo.html
'''
