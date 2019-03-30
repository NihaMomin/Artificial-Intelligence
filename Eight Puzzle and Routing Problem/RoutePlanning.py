#importing packages
import util
import search
import csv

#importing data from csvs
#the lists connections and heuristics are nested lists
with open('cities.csv', 'r') as f:
  reader = csv.reader(f)
  cities = list(reader)
with open('connections.csv', 'r') as f:
  reader = csv.reader(f)
  connections = list(reader)
with open('heuristics.csv', 'r') as f:
  reader = csv.reader(f)
  heuristics = list(reader)
cities=  [y for x in cities for y in x]

#RoutePlanning Class
class RoutePlanningProblem(search.SearchProblem):
    def __init__(self,start,goal,heuristics,connections):
        '''Creates a new RoutePlanningProblem which
                    stores search information.'''
        self.start = start
        self.goal = goal
        self.heuristics = heuristics
        self.connections = connections
        
    def __str__(self):
        return self.start
    
    def __hash__(self):
        return hash(str(self.start))
 
    def getStartState(self):
        return self.start

    def isGoalState(self,state):
        if state==self.goal:
            return True
        else:
            return False
        
    def getSuccessors(self,state):
            """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is the city that we can go to i.e.not having
          the value -1 as its connection
        """
            successor=[]
            index=[]
            stepCost=[]
            output=[]
            #finds indices and costs of the cities which have connections and then uses
            #those indices to access the cities from the lists 
            for i in range(1,len(connections)):
                if state==connections[i][0]:
                    for j in range(1,len(connections[i])):
                        if int(connections[i][j])!=-1 and int(connections[i][j])!=0:
                            index+=[int(j)]
                            stepCost+=[int(connections[i][j])]
            for i in index:
                successor.append(connections[0][i])
            for i in range(len(successor)):
                output.append((successor[i],successor,state,stepCost[i]))    
            return output

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves i.e. the cities that we can travel to
        """
        cost=0
        
        for i in range(len(actions)-1):
            first=connections[0].index(actions[i])
            second=connections[0].index(actions[i+1])
            cost+=int(connections[first][second])
        return cost

    def getHeuristic(self,state):
        successor=self.getSuccessors(state)[0][1]
        heuristicValue=[]
        stateIndex=heuristics[0].index(state)
        
        for i in range(len(successor)):
            first=heuristics[0].index(successor[i])
            heuristicValue.append(int(heuristics[stateIndex][first]))              
        return min(heuristicValue)


                
                
                
problem = RoutePlanningProblem("Khunjerab Pass","Islamabad",heuristics,connections)
path = search.aStarSearch(problem)
print("Initial State")
print(problem.getStartState())
print("Path",path)

