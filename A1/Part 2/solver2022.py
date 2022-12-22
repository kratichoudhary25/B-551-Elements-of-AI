#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: Balajee Devesha Srinivasan basrini
#          Smit Borasaniya sborasan
#          Krati Choudhary krachoud
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
# reference from https://docs.python.org/3/library/heapq.html
import heapq

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# ------------ Getting row and col value --------------
def indexed(index):
    return (int(index/5), index % 5)

# ------------ Row Rotation ----------------
# helper function for row rotation towards right
def rowR(r):
    return r[-1:] + r[0:-1]
# helper function for row rotation towards left
def rowL(r):
    return r[1:] + r[0:1]

# ----------- Row Successors -----------------
# row successor function to give successors towards right
def rowR_succ(board, r):
    rotr = rowR(board[r*5:(r*5)+5])
    # print(rotr)
    # print((tuple(board[0:r*5] + rotr + board[(r*5)+5:])))
    return (tuple(board[0:r*5] + rotr + board[(r*5)+5:]))
# row successor function to give successors towards left
def rowL_succ(board, r):
    rotr = rowL(board[r*5:(r*5)+5])
    # print(rotr)
    # print((tuple(board[0:r*5] + rotr + board[(r*5)+5:])))
    return (tuple(board[0:r*5] + rotr + board[(r*5)+5:]))

# ----------- Column Rotation ----------------
# helper function for column rotation upwards
def colUp(c):
    return c[1:] + c[0:1]
# helper function for column rotation  downwards
def colDown(c):
    return c[-1:] + c[0:-1]

# ------------ Column Successors ---------------
# column successor function to give successors upwards
def colUp_succ(board, c):
    rotc = colUp(board[c:c+21:5])
    # print(rotc)
    # print((tuple(board[0:c] + tuple([rotc[0]])) + board[c+1:c+5] + tuple([rotc[1]]) + board[c+6:c+10] + tuple([rotc[2]]) + board[c+11:c+15] + tuple([rotc[3]]) + board[c+16:c+20] + tuple([rotc[4]]) + board[c+21:]))
    return (tuple(board[0:c] + tuple([rotc[0]])) + board[c+1:c+5] + tuple([rotc[1]]) + board[c+6:c+10] + tuple([rotc[2]]) + board[c+11:c+15] + tuple([rotc[3]]) + board[c+16:c+20] + tuple([rotc[4]]) + board[c+21:])
# column successor function to give successors downwards
def colDown_succ(board,col):
    rotc = colDown(board[col:col + 21:5])
    # print(rotc)
    # print((tuple(board[0:col] + tuple([rotc[0]])) + board[col + 1:col + 5] + tuple([rotc[1]]) + board[col + 6:col + 10] + tuple([rotc[2]]) + board[col + 11:col + 15] + tuple([rotc[3]]) + board[col + 16:col + 20] + tuple([rotc[4]]) + board[col + 21:]))
    return (tuple(board[0:col] + tuple([rotc[0]])) + board[col + 1:col + 5] + tuple([rotc[1]]) + board[col + 6:col + 10] + tuple([rotc[2]]) + board[col + 11:col + 15] + tuple([rotc[3]]) + board[col + 16:col + 20] + tuple([rotc[4]]) + board[col + 21:])


# ------------- Outer Elements Rotation --------------
# outer clockwise rotation
def OC(board):
    # print((tuple([board[5]]) + tuple(board[0:4]) + tuple([board[10]]) + tuple(board[6:9]) + tuple([board[4]]) + tuple([board[15]]) + tuple(board[11:14]) + tuple([board[9]]) + tuple([board[20]]) + tuple(board[16:19]) + tuple([board[14]]) + tuple([board[21]]) + tuple(board[22:25]) + tuple([board[19]])))
    return (tuple([board[5]]) + tuple(board[0:4]) + tuple([board[10]]) + tuple(board[6:9]) + tuple([board[4]]) + tuple([board[15]]) + tuple(board[11:14]) + tuple([board[9]]) + tuple([board[20]]) + tuple(board[16:19]) + tuple([board[14]]) + tuple([board[21]]) + tuple(board[22:25]) + tuple([board[19]]))
# outer anti-clockwise rotation
def OCC(board):
    # print((tuple([board[1]]) + tuple(board[2:5]) + tuple([board[9]]) + tuple([board[0]]) + tuple(board[6:9]) + tuple([board[14]]) + tuple([board[5]]) + tuple(board[11:14]) + tuple([board[19]]) + tuple([board[10]]) + tuple(board[16:19]) + tuple([board[24]]) + tuple([board[15]]) + tuple(board[20:23]) + tuple([board[23]])))
    return (tuple([board[1]]) + tuple(board[2:5]) + tuple([board[9]]) + tuple([board[0]]) + tuple(board[6:9]) + tuple([board[14]]) + tuple([board[5]]) + tuple(board[11:14]) + tuple([board[19]]) + tuple([board[10]]) + tuple(board[16:19]) + tuple([board[24]]) + tuple([board[15]]) + tuple(board[20:23]) + tuple([board[23]]))


# -------------- Inner Elements Rotation ----------------
# inner clockwise rotation
def IC(board):
    # print((tuple(board[0:6]) + tuple([board[11]]) + tuple(board[6:8]) + tuple(board[9:11]) + tuple([board[16]]) + tuple([board[12]]) + tuple([board[8]]) + tuple(board[14:16]) + tuple(board[17:19]) + tuple([board[13]]) + tuple(board[19:])))
    return (tuple(board[0:6]) + tuple([board[11]]) + tuple(board[6:8]) + tuple(board[9:11]) + tuple([board[16]]) + tuple([board[12]]) + tuple([board[8]]) + tuple(board[14:16]) + tuple(board[17:19]) + tuple([board[13]]) + tuple(board[19:]))
# inner anti-clockwise rotation
def ICC(board):
    # print((tuple(board[0:6]) + tuple(board[7:9]) + tuple([board[13]]) + tuple(board[9:11]) + tuple([board[6]]) + tuple([board[12]]) + tuple([board[18]]) + tuple(board[14:16]) + tuple([board[11]]) + tuple(board[16:18]) + tuple(board[19:])))
    return (tuple(board[0:6]) + tuple(board[7:9]) + tuple([board[13]]) + tuple(board[9:11]) + tuple([board[6]]) + tuple([board[12]]) + tuple([board[18]]) + tuple(board[14:16]) + tuple([board[11]]) + tuple(board[16:18]) + tuple(board[19:]))


# -------------- Heuristic Function -----------------
def manhatt(board):
    # initializing a dictionary of touples to find manhatten distance with the successor fringe
    finalPos = {1: (0,0), 2: (0,1), 3: (0,2), 4: (0,3), 5: (0,4), 6: (1,0), 7:(1,1), 8:(1,2), 9:(1,3), 10:(1,4), 11:(2,0), 12:(2,1), 13:(2,2), 14:(2,3), 15:(2,4), 16:(3,0), 17:(3,1), 18:(3,2), 19:(3,3), 20:(3,4), 21:(4,0), 22:(4,1), 23:(4,2), 24:(4,3), 25:(4,4)}
    # initializing hueristic = 0
    heuristic = 0

    fin = -1
    for index, val in enumerate(board):
        row, col = indexed(index)
        # print(row, col)
        # final pos of Row
        finR = finalPos[val][0]
        # final pos of Column
        finC = finalPos[val][1]
        # print(finR, finC)
        # absolute values of rows and columns
        a= abs(row-finR)+abs(col-finC)
        b= 5-abs(row-finR)+abs(col-finC)
        c= abs(row-finR)+5-abs(col-finC)
        d=5-abs(row-finR)+5-abs(col-finC)
        ## print(a,b,c,d)
        fin=min(a,b,c,d)
        heuristic+=fin
        # print(fin,heuristic)
    return heuristic//5


# ---------------- Storing Steps ---------------
# successor function to find the next successor states with the given rotations
def successors(board):
 
    succ = []
    # first checking all rotations and then appending to successor list
    succ.append([(OC(board)), 'Oc', manhatt(OC(board))])
    succ.append([(OCC(board)), 'Occ', manhatt(OCC(board))])
    succ.append([(IC(board)), 'Ic', manhatt(IC(board))])
    succ.append([(ICC(board)), 'Icc', manhatt(ICC(board))])
    # print(succ)
    # then checking and computing the column and row rotations and finding out their manhatten distance parallelly.
    for ele in range(1,6):
        succ.append(
            [(rowL_succ(board, ele-1)), 'L' + str(ele), manhatt(rowL_succ(board, ele-1))])
        succ.append(
            [(rowR_succ(board, ele-1)), 'R' + str(ele), manhatt(rowR_succ(board, ele-1))])
        succ.append(
            [(colUp_succ(board, ele-1)), 'U' + str(ele), manhatt(colUp_succ(board, ele-1))])
        succ.append(
            [(colDown_succ(board, ele-1)), 'D' + str(ele), manhatt(colDown_succ(board, ele-1))])
    # print(succ)
    # returning all the computed successors
    return succ

# ---------------- Goal State Comparison ------------------
# checking if goal state is achieved and if it is then returning the path taken till the goal is reached.
def is_goal(board):
    # print("inside goal state fn")
    dest = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    return dest == list(board)

# --------------- Finding the path -------------------
def solve(initial_board):
    
    traversed = {tuple(initial_board):True}
    fringe = []
    current_path = []
    current_cost = 0

    heapq.heappush(fringe, (manhatt(initial_board), (initial_board, current_cost, current_path)))

    while fringe:
        # getting state, current_cost, current_path from the fringe appended by the successor function
        _, (state, current_cost, current_path) = heapq.heappop(fringe)
        # print(state, current_cost, current_path)
        for (next_state, move, manhattan_cost) in successors(state):
            # terminating condition here
            if is_goal(next_state):
                return current_path + [move]
            else:
                # we only append if next state is not in the visited states so that if we do encounter the same node we need not recompute all the nodes for the given node again
                if next_state not in traversed.keys():

                    # print(f"next_state : {next_state}")
                    traversed[next_state] = True

                    heuristic_val = current_cost + 1 + manhattan_cost
                    # print(f"heuristic_val : {heuristic_val}")
                    heapq.heappush(fringe, (heuristic_val, (next_state, current_cost + 1, current_path + [move])))

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
