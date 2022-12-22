#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Krati Choudhary krachoud
#
# Discussed approach with : Kalyani Malokar
# Based on skeleton code provided in CSCI B551, Fall 2022.
#
# References:
# https://www.udemy.com/course/data-science-and-machine-learning-with-python-hands-on/learn/lecture/15090158#overview
# https://www.udemy.com/course/complete-python-bootcamp/learn/lecture/9497634#overview
# https://www.udemy.com/course/complete-python-bootcamp/learn/lecture/9442732#overview


import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# This function just appends the direction of the pichu in a string
def move_made(m, curr_loc, move_string):
        if m[1] == curr_loc[1] - 1:
                move_string = move_string + "L"
        elif m[1] == curr_loc[1] + 1:
                move_string = move_string + "R" 
        elif m[0] == curr_loc[0] - 1:
                move_string = move_string + "U"
        elif m[0] == curr_loc[0] + 1:
                move_string = move_string + "D"
        return move_string



def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0] # Coordinate of pichu's start location
        fringe=[(pichu_loc,0,'')] # Stores the current location of pichu, the number of unique moves, and an empty string to store the directions
        #print(fringe)
        
        #Record the visited locations
        visited = []

        # While
        while fringe != 0:
                (curr_move, curr_dist, move_string)=fringe.pop(0)
                row = curr_move[0]
                col = curr_move[1]
                for mv in moves(house_map, row, col):
                        if mv in visited:
                                continue
                        if house_map[mv[0]][mv[1]]=="@":
                                final_ans = (curr_dist+1, move_made(mv, (row,col), move_string))
                                return final_ans #As soon as the pichu reaches the destination the function returns the distance and the direction the pichu took
                        else:
                                fringe.append((mv, curr_dist + 1, move_made(mv, (row,col), move_string)))
        return(-1,'')

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

