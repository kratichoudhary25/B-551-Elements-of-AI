#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: Smit Borasaniya sborasan
#          Balajee Devesha Srinivasan basrini
#          Krati Choudhary krachoud
#
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys
N=5

#####
# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):

    # print(f"successor : {[ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]}")

    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# given a state, return an estimate of the number of steps to a goal from that state
# refereence for heuristic calculation of manhatten distance : https://iq.opengenus.org/manhattan-distance/
def h(state):
    # print(f"state inside h:{state}")
    # print(sum(val1-val2) for val1, val2 in zip(state,[1,2,3,4,5]))
    heur_distance = []
    
    # calculating the Heuristic value(manhatten dist)
    for _, __ in zip(state, [1,2,3,4,5]):

        difference = __ - _
        absolute_difference = abs(difference)
        # if len(absolute_difference) == absolute_difference.count(absolute_difference.set()):
        #     return 0
        heur_distance.append(absolute_difference)
    return sum(heur_distance)

#########
#
# THE ALGORITHM:
#
# This is a generic solver using BFS. 
#
def solve(initial_state):
    fringe = []
    # taking dummy cost to converge it if we find a cost less than it.
    cost = 100

    # visited_move=[]
    # counter = 0
    fringe += [(initial_state, []),]
    while len(fringe) > 0:
        (state, path) = fringe.pop(0)

        # visited_move.append(state)
        # print(f"(state, path) : {(state, path)}")
        
        if is_goal(state):
            # endw = time.time() - start
            # print(endw)
            return path+[state,]

        for s in successors(state):
            heur_dist = h(s)

            # print(heur_dist)
            # print(f"s : {s}")

            if heur_dist <= cost:

                cost = heur_dist
                fringe.append((s, path+[state,]))
        
        # print(f"fringe : {fringe}")
        # counter += 1
        # if counter == 20:
        #     break

    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))
    
    
    

