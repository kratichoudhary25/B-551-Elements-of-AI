#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Krati Choudhary, krachoud
# 
# Based on skeleton code in CSCI B551, Fall 2022.
#
# https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/


import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    succ=[]
    for row in range(0, len(house_map)):
        for col in range(0,len(house_map[0])):
            if house_map[row][col] == '.':
                new_house_map = add_pichu(house_map, row, col)
                if condition_check(new_house_map):
                    succ.append(new_house_map)
    
    return succ

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

def condition_check(house_map):
    # Iterated over the whole grid 
    for row in range(0, len(house_map)):
        for col in range(0,len(house_map[0])):

            if house_map[row][col] == "p":  
               
               #checking row 
                row_temp = ""
                for i in range(col+1,len(house_map[0])):
                    row_temp += house_map[row][i]

                    if house_map[row][i] == "p":
                        if ("X" in row_temp[:]) or ("@" in row_temp[:]):
                            break
                        else:
                            return False
                
                #checking columns
                col_temp = ""  
                for i in range(row+1,len(house_map)):
                    col_temp += house_map[i][col]
                    
                    if house_map[i][col] == "p":
                        if ("X" in col_temp[:]) or ("@" in col_temp[:]):
                            break
                        else:
                            return False

                # checking lower half of the positive diagonal
                        
                pos_down = ""
                row_down = row
                col_down = col
                while (row_down + 1 in range(len(house_map)-1)) and (col_down-1 in range(len(house_map[0]))):
                    row_down += 1
                    col_down -= 1
                    pos_down += house_map[row_down][col_down]
                    if house_map[row_down][col_down] == "p":
                        if "X" in pos_down[:] or ("@" in pos_down[:]) :
                            break
                        else:
                            return False

                #checking upper half of positive diagonal
                pos_up = ""
                row_up = row
                col_up = col
                while (row_up-1 in range(0,len(house_map))) and (col_up+1 in range(0,len(house_map[0]))):
                    row_up -= 1
                    col_up += 1
                    pos_up += house_map[row_up][col_up]
                    if house_map[row_up][col_up] == "p":
                        if ("X" in pos_up[:]) or ("@" in pos_up[:]) :
                            break
                        else:
                            return False

               # checking lower half of the negative diagonal
                
                neg_down=""
                row_down=row
                col_down=col
                while (row_down+1 in range(len(house_map)-1)) and (col_down+1 in range(len(house_map[0]))):
                    row_down += 1
                    col_down += 1
                    neg_down += house_map[row_down][col_down]
                    if house_map[row_down][col_down]=="p":
                        if ("X" in neg_down[:]) or ("@" in neg_down[:]):
                            break
                        else:
                            return False
                        
                # checking upper half of the negative diagonal
                
                neg_up = ""
                row_up = row
                col_up = col
                while (row_up - 1 in range(len(house_map))) and (col_up-1 in range(len(house_map[0]))):
                    row_up -= 1
                    col_up -= 1
                    neg_up += house_map[row_up][col_up]
                    if house_map[row_up][col_up]=="p":
                        if ("X" in neg_up[:]) or ("@" in neg_up[:]):
                            break
                        else:
                            return False
                
                
                
    # it will return true if all the conditions have been met that is no "p" is able to see each other
    return True

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            fringe.append(new_house_map)
    return ("",False)
    '''
    while len(fringe) > 0:
        for new_house_map in successors(fringe.pop()):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            fringe.append(new_house_map)
'''
# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


