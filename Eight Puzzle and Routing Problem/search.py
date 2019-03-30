# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
       
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """

        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """

        util.raiseNotDefined()
        
    def getHeuristic(self,state):
        """
         state: the current state of agent

         THis function returns the heuristic of current state of the agent which will be the 
         estimated distance from goal.
        """
        util.raiseNotDefined()


def aStarSearch(problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #creating frontier
    frontier=util.PriorityQueue()
    #initial state
    initialState=problem.getStartState() 
    f=problem.getHeuristic(initialState)
    frontier.push(initialState,f)
    #Dictionaries to maintain path and cost
    previousNode={}
    previousNode[initialState]=None
    previousCost={}
    visited = set()
    flag=False
    nodes=[]
    previousCost[initialState]=0
    #loop runs till the frontier isn't empty
    while frontier.isEmpty()==False:
    #pops lowest priority element here priority is sum of cost and heuristics
        current=frontier.pop()
        if (not current in visited):
            visited.add(current)
        #breaks loop when goal state found
            if problem.isGoalState(current):
                flag=True
                break
        #finding the goal state
            successor=problem.getSuccessors(current)
 
            for i in successor:
        #i[3] is the stepCost that the successor function returns along with successors
                newCost=previousCost[current]+i[3]
                if i[0] not in previousCost or newCost<previousCost[i[0]]:
                    previousCost[i[0]]=newCost
                    priority=newCost+problem.getHeuristic(i[0])
                    frontier.push(i[0],priority)
                    #stores the previous node
                    previousNode[i[0]]=current

    #to get the path
    #Since the dictionary previousNode keeps track of the node from which we
    #came to the current node. Hence, back tracking would give us the entire path            
    if flag:
        while True:
            nodes=[current]+nodes
            temp=current
            current=previousNode[current]
            del previousNode[temp]
            #breaks the loop when the dictionary exhausts
            if not current:
                break  
                    
    return nodes

'''Reference: https://www.redblobgames.com/pathfinding/a-star/implementation.html
A* algorithm was understood from the mentioned link and then implemented. Reference has been
provided to avoid plagarism because the above code has been inspired from the mentioned link.
'''
