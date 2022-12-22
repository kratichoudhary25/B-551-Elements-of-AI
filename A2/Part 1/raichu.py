#
# raichu.py : Play the game of Raichu
#
# Code by: Krati Choudhary <krachoud>
#        : Prabhruti Choudhary <prabchau>
#        : Sai Tanishq Nannapaneni <snannap>
#
# Based on skeleton code by D. Crandall, Oct 2021


import time
import copy
import sys

# Converting the string board to 2d matrix board 
def board_matrix(stringBoard,size):
    board=[[None]*size for i in range(size)]
    k=0
    for i in range(size):
        for j in range(size):
            board[i][j]=stringBoard[k]
            k+=1
    return board

# -------------------- Move validity checker ---------------------------
def move_valid(r,c,N):
    if 0 <= r < N and 0 <= c < N:
        return True
    else:
        return False

# -------------------------- White pichu moves --------------------------

# ------------------------ Cases for white pichu moving to left diagonal -----------------------
def w_pichu_left_diag(pos,r,c,N,succ_pichu):
    
    if c > 0 and c <= N and r<=N-1:

    # --------------------- If the left diagonal position is empty ---------------------------
        if pos[r+1][c-1]==".":

            # ----------------- If we reach at raichu promotion condition -----------------------
            if r == N-1:
                state = copy.deepcopy(pos)
                state[r + 1][c-1] = '@'
                state[r][c] = '.'
                succ_pichu.append(state)

            # ----------------- If we are at a middle place -----------------------------
            else: 
                state = copy.deepcopy(pos)
                state[r+1][c-1] = 'w'
                state[r][c] = '.'
                succ_pichu.append(state)
              
        # ---------------------- If opponent found ---------------------    
        if  pos[r+1][c-1]=="b" and (r<=N-2 and c>=2) and pos[r+2][c-2]==".": 

            # -------------------- If opponent is at the left diagonal and after jumping we reach raichu condition ---------------------------
            if r==N-2:
                state = copy.deepcopy(pos)
                state[r+2][c-2] = '@'
                state[r][c] = '.'
                state[r+1][c-1] = '.'
                succ_pichu.append(state)

            # ------------------- If opponent is at left diagonal but somewhere in the middle -------------------------    
            else:
                state = copy.deepcopy(pos)
                state[r+2][c-2] = 'w'
                state[r][c] = '.'
                state[r+1][c-1] = '.'
                succ_pichu.append(state)

# ------------------------ Cases for white pichu moving to right diagonal -----------------------
def w_pichu_right_diag(pos, r, c, N, succ_pichu):

    if move_valid(r,c,N) and pos[r+1][c+1]==".":
        if r == N-1: 
            state = copy.deepcopy(pos)
            state[r + 1][c+1] = '@'
            state[r][c] = '.'
            succ_pichu.append(state)
    
        else: 
            state = copy.deepcopy(pos)
            state[r+1][c+1] = 'w'
            state[r][c] = '.'
            succ_pichu.append(state)
                        
        if c >= 0 and c <= N-2 and r<=N-1:
            # ---------------- If immediate next diagonal position is empty ---------------------
            if pos[r+1][c+1]==".": 
                # ----------------------- If pichu has reached to the position where it changes to raichu ----------------------
                if r == N-1: 
                    state = copy.deepcopy(pos)
                    state[r + 1][c+1] = '@'
                    state[r][c] = '.'
                    succ_pichu.append(state)

                else: 
                # -------------------------- If pichu is at some other position we just move it -------------------------    
                    state = copy.deepcopy(pos)
                    state[r+1][c+1] = 'w'
                    state[r][c] = '.'
                    succ_pichu.append(state)
                            # --------------------- If there is an opponent --------------------------------  
                if  pos[r+1][c+1]=="b" and (r<=N-2 and c<=N-2) and pos[r+2][c+2]=="." :  
                    # ----------------------- After jumping over opponent we reach raichu condition ---------------------------
                    if r==N-2:
                        state = copy.deepcopy(pos)
                        state[r+2][c+2] = '@'
                        state[r][c] = '.'
                        state[r+1][c+1] = '.' 
                        succ_pichu.append(state)
                    # ---------------------- Just jumping over opponent --------------------------------    
                    else: 
                        state = copy.deepcopy(pos)
                        state[r+2][c+2] = 'w'
                        state[r][c] = '.'
                        state[r+1][c+1] = '.'
                        succ_pichu.append(state)
# ----------------------------- Black pichu moves -------------------------
def b_pichu_right_diag(pos,r,c,N,succ_pichu):
    if c >= 0 and c <= N-1:
        # -------------------- Immediate diagonal empty ---------------------------

        if pos[r-1][c+1]==".": 
        
            # --------------------- Reached raichu condition -----------------------
            if r == 1: 
                state = copy.deepcopy(pos)
                state[r - 1][c+1] = '$'
                state[r][c] = '.'
                succ_pichu.append(state)
        
            # ----------------------- Did not reach raichu condition --------------------------
            else: 
                state = copy.deepcopy(pos)
                state[r-1][c+1] = 'b'
                state[r][c] = '.'
                succ_pichu.append(state)
            
        # --------------------- Opponent is at immediate diagonal ------------------------    
        if  pos[r-1][c+1]=="w" and (r>=2 and c<=N-2) and pos[r-2][c+2]=="." : 
            if r==2:
                state = copy.deepcopy(pos)
                state[r - 2][c+2] = '$'
                state[r][c] = '.'
                state[r-1][c+1] = '.'
                succ_pichu.append(state)
            else:
                state = copy.deepcopy(pos)
                state[r-2][c+2] = 'b'
                state[r-1][c+1] = '.'
                state[r][c] = '.'
                succ_pichu.append(state)    

def b_pichu_left_diag(pos,r,c,N,succ_pichu):
    # All the things  repeated as above for the cases of left diagonal
    if c > 0 and c <= N:
                            # if the immediate left diagonal is empty
        if pos[r-1][c-1]==".":
            if r == 1:  # If we are in second last
                state = copy.deepcopy(pos)
                state[r - 1][c-1] = '$'
                state[r][c] = '.'
                succ_pichu.append(state)
            else: # If we are in some middle r
                state = copy.deepcopy(pos)
                state[r-1][c-1] = 'b'
                state[r][c] = '.'
                succ_pichu.append(state)
                            # Case in which there is an opponent player at it's immediate left diagonal
        if  pos[r-1][c-1]=="w" and (r>=2 and c>=2) and pos[r-2][c-2] == '.' : 
            if r==2:
                state = copy.deepcopy(pos)
                state[r - 2][c-2] = '$'
                state[r][c] = '.'
                state[r-1][c-1] = '.'
                succ_pichu.append(state)
            else:
                state = copy.deepcopy(pos)
                state[r-2][c-2] = 'b'
                state[r][c] = '.'
                state[r-1][c-1] = '.'
                succ_pichu.append(state)

# ----------------- Successors of pichu -------------------------
def pichu(pos,player):
    succ_pichu = []
    N=len(pos)-1
    if player=="w": # if the current player is white 
        for r in range(N):
               for c in range(len(pos[0])):
                    if pos[r][c] == 'w':
                        w_pichu_right_diag(pos, r, c, N, succ_pichu)
                        w_pichu_left_diag(pos, r, c, N, succ_pichu)               
                        
    else: # covered all the cases of black pichu 
        for r in range(len(pos)):
            for c in range(len(pos[0])):
                    if pos[r][c] == 'b':
                        b_pichu_right_diag(pos, r, c, N, succ_pichu)
                        b_pichu_left_diag(pos, r, c, N, succ_pichu)       
                        
    return succ_pichu
                        

                        # when we are moving down
                        # cases when immediate step below us is empty 

def w_pikachu_down(pos,r,c,N,succ_pikachu):

        if r<=N-1: 
            if pos[r+1][c]=="." and r==N-1 : # when we are in last r
                state = copy.deepcopy(pos)
                state[r+1][c] = '@'
                state[r][c] = '.'
                succ_pikachu.append(state)
        elif pos[r+1][c]==".": # if we are in some middle r
                state = copy.deepcopy(pos)
                state[r+1][c] = 'W'
                state[r][c] = '.'
                succ_pikachu.append(state)
        
        # considering cases when 2 steps below us are empty and we jump 2 steps
        if r<=N-2:                                                             
            if pos[r+1][c]=="." and pos[r+2][c]=="."  : 
                if r==N-2: # if we are in 5th r and jumping 2 steps will reach last r thus become raichu
                    state = copy.deepcopy(pos)
                    state[r + 2][c] = '@'
                    state[r][c] = '.'
                    succ_pikachu.append(state)                                    
                else: # if we are in some middle r then just move 2 position forward
                    state = copy.deepcopy(pos)
                    state[r+2][c] = 'W'
                    state[r][c] = '.'
                    succ_pikachu.append(state)                                      
            
# now considering first step below us empty and another is full
        if pos[r+1][c]=="." and (pos[r+2][c] in ["b","B","w","W"] ) : 
            if pos[r+2][c]=="b" or pos[r+2][c]=="B":
                if r==N-3 and pos[r+3][c]==".": # if we are in 4th r
                    state = copy.deepcopy(pos)
                    state[r + 3][c] = '@' # reached last r so convert to Raichu
                    state[r][c] = '.'     # updating our original location
                    state[r+2][c] = '.'   # updating the opponents location
                    succ_pikachu.append(state)
            else:                             # if we are in some middle r 
                if r<N-3 and pos[r+3][c]==".":
                    state = copy.deepcopy(pos)
                    state[r+3][c] = 'W'
                    state[r+2][c] = '.'
                    state[r][c] = '.'
                    succ_pikachu.append(state)                    
        
    # now considering when first step below us is full and another is empty 
        if (pos[r+1][c] in ["b","B","w","W"]) and pos[r+2][c]=="." : 
            if pos[r+1][c]=="b" or pos[r+1][c]=="B":
                if r==N-2:
                    state = copy.deepcopy(pos)
                    state[r + 2][c] = '@' # reached last r so convert to Raichu
                    state[r][c] = '.'     # updating our original location
                    state[r+1][c] = '.'   # updating the opponents location
                    succ_pikachu.append(state)
                else:                             # if we are in some middle r 
                    state = copy.deepcopy(pos)
                    state[r + 2][c] = 'W' 
                    state[r][c] = '.'
                    state[r+1][c] = '.' 
                    succ_pikachu.append(state)
    
    # 2 steps are empty moving forward
        if r<=N-3 and (pos[r+1][c] in ["b","B","w","W"] ) and pos[r+2][c]=="." and pos[r+3][c]=="." : 
            if pos[r+1][c]=="b" or pos[r+1][c]=="B":
                if r==N-3:
                    state = copy.deepcopy(pos)
                    state[r + 3][c] = '@' # reached last r so convert to Raichu
                    state[r+1][c] = '.'   # updating the opponents location
                    state[r][c] = '.'     # updating our original location
                    succ_pikachu.append(state)
                else:                             # if we are in some middle ro
                    state = copy.deepcopy(pos)
                    state[r + 3][c] = 'W' 
                    state[r+1][c] = '.'
                    state[r][c] = '.'
                    succ_pikachu.append(state)   


def w_pikachu_left(pos,r,c,N,succ_pikachu):
    # All the cases when we are moving pikachu to left side
    # when moving 1 step to the left when its empty
    if c>=1 and pos[r][c-1]==".":
        state = copy.deepcopy(pos)
        state[r][c-1] = 'W'
        state[r][c] = '.'
        succ_pikachu.append(state)
            
    if c>=2:
        # when moving 2 step to the left when they are empty 
        if pos[r][c-1]=="." and pos[r][c-2]=="."  : 
            state = copy.deepcopy(pos)
            state[r][c-2] = 'W'
            state[r][c] = '.'
            succ_pikachu.append(state)
        
        # now considering first step in left empty and another is full
        if pos[r][c-1]=="." and (pos[r][c-2] in ["b","B","w","W"]) : 
            if c>=3 and pos[r][c-3]=="." and pos[r][c-1] in 'bB':
                    state[r][c-3] = 'W'
                    state[r][c-2] = '.'
                    state[r][c] = '.'
                    succ_pikachu.append(state)
                
        # now considering first step full and another is empty 
        if (pos[r][c-1] in ["b","B","w","W"]) and pos[r][c-2]=="." : 
            if pos[r][c-1]=="b" or pos[r][c-1]=="B":
                state = copy.deepcopy(pos)
                state[r][c-2] = 'W' 
                state[r][c] = '.'
                state[r][c-1] = '.' 
                succ_pikachu.append(state)
        
        # considering first step full and 2 steps are empty after that
        if c>=3 and (pos[r][c-1] in ["b","B","w","W"]) and pos[r][c-2]=="." and pos[r][c-3]=="." : 
            if pos[r][c-1]=="b" or pos[r][c-1]=="B":    
                state = copy.deepcopy(pos)
                state[r][c-3] = 'W' 
                state[r][c-1] = '.'
                state[r][c] = '.'
                succ_pikachu.append(state)

def w_pikachu_right(pos,r,c,N,succ_pikachu):
    # All the cases when we are moving pikachu to right side
    # when moving 1 step to the right when its empty
    if c<=N-1 and pos[r][c+1]==".":
            state = copy.deepcopy(pos)
            state[r][c+1] = 'W'
            state[r][c] = '.'
            succ_pikachu.append(state)
            
    if c<=N-2:                                    
         # considering when moving 2 steps to the right when they are empty 
        if pos[r][c+1]=="." and pos[r][c+2]=="."  :                                     
            state = copy.deepcopy(pos)
            state[r][c+2] = 'W'
            state[r][c] = '.'
            succ_pikachu.append(state)
        
        # now considering first step in right empty and another is full and after that there is an empty step
        # so we will jump to the last empty step. We could have jumped to the first empty step but that case 
        # we have already covered above when we to check any immediate empty step towards right
        if pos[r][c+1]=="." and (pos[r][c+2] in ["b","B","w","W"]) : 
            if pos[r][c+2]=="b" or pos[r][c+2]=="B":
                if c<=N-3 and state[r][c+3]==".":
                    state = copy.deepcopy(pos)
                    state[r][c+3] = 'W'
                    state[r][c+2] = '.'
                    state[r][c] = '.'
                    succ_pikachu.append(state)
                
        # now considering  first step full and another is empty 
        if (pos[r][c+1] in ["b","B","w","W"]) and pos[r][c+2]=="." : 
            if pos[r][c+1]=="b" or pos[r][c+1]=="B":
                state = copy.deepcopy(pos)
                state[r][c+2] = 'W' 
                state[r][c] = '.'
                state[r][c+1] = '.' # jo place par opponent tha usko delete
                succ_pikachu.append(state)
        
        # considering first step full and 2 steps empty to the right
        if c<=N-3 and (pos[r][c+1] in ["b","B","w","W"]) and pos[r][c+2]=="." and pos[r][c+3]=="." : 
            if pos[r][c+1]=="b" or pos[r][c+1]=="B": 
                state = copy.deepcopy(pos)
                state[r][c+3] = 'W' 
                state[r][c+1] = '.'
                state[r][c] = '.'
                succ_pikachu.append(state)  

def b_pikachu_up(pos,r,c,N,succ_pikachu):       

    
                    # when moving up 
                    # consider to when 1 step is empty above
    if r>=1 and pos[r-1][c]==".":
        if r==N-1: # If we are in second r will get converted to Raichu
            state = copy.deepcopy(pos)
            state[r-1][c] = '$'
            state[r][c] = '.'
            succ_pikachu.append(state)
        else:       # We are in some middle r
            state = copy.deepcopy(pos)
            state[r-1][c] = 'B'
            state[r][c] = '.'
            succ_pikachu.append(state)
                                    
    if r>=2:
    # considering when two steps above are empty
        if pos[r-1][c]=="." and pos[r-2][c]=="."  : 
            if r==2: # if we are in 2nd r and jumping 2 steps
                state = copy.deepcopy(pos)
                state[r - 2][c] = '$'
                state[r][c] = '.'
                succ_pikachu.append(state)                                    
            else: # if we are in some middle r and we move 2 position forward
                state = copy.deepcopy(pos)
                state[r-2][c] = 'B'
                state[r][c] = '.'
                succ_pikachu.append(state)

    # now considering first step empty and another is full and then another step is empty 
    if pos[r-1][c]=="." and (pos[r-2][c] in ["w","W","b","B"]) : 
        if pos[r-2][c]=="w" or pos[r-2][c]=="W":                                
            if r>3 and state[r-3][c]==".":
                state = copy.deepcopy(pos)
                state[r-3][c] = 'B'
                state[r-2][c] = '.'
                state[r][c] = '.'
                succ_pikachu.append(state)
            
    # now considering  first step full and another is empty 
    if (pos[r-1][c] in ["w","W","b","B"]) and pos[r-2][c]=="." : 
        if pos[r-1][c]=="w" or pos[r-1][c]=="W":
            if r==2: # if we are in 2nd r 
                state = copy.deepcopy(pos)
                state[r - 2][c] = '$' # will reach last r therefore raichu
                state[r][c] = '.'
                state[r-1][c] = '.' 
                succ_pikachu.append(state)
            else: # if we are in some middle r
                state = copy.deepcopy(pos)
                state[r - 2][c] = 'B' 
                state[r][c] = '.'
                state[r-1][c] = '.' 
                succ_pikachu.append(state)

    # considering first step full and then 2 steps are empty
    if r>=3 and (pos[r-1][c] in ["w","W","b","B"]) and pos[r-2][c]=="." and pos[r-3][c]=="." : 
        if pos[r-1][c]=="w" or pos[r-1][c]=="W":
            if r==3: # if in 3rd r than will be converted to Raichu
                state = copy.deepcopy(pos)
                state[r - 3][c] = '$' 
                state[r-1][c] = '.'
                state[r][c] = '.'
                succ_pikachu.append(state)
            else: # We are in some middle r
                state = copy.deepcopy(pos)
                state[r - 3][c] = 'B' 
                state[r-1][c] = '.'
                state[r][c] = '.'
                succ_pikachu.append(state)

def b_pikachu_left(pos,r,c,N,succ_pikachu):
    # now doing all the things when moving left side
    # when first step towards left is empty            
    if c>=1 and pos[r][c-1]==".":
            state = copy.deepcopy(pos)
            state[r][c-1] = 'B'
            state[r][c] = '.'
            succ_pikachu.append(state)
                
    if c>=2:
        # considering when left 2 steps are empty and we jump 2 steps left 
        if pos[r][c-1]=="." and pos[r][c-2]=="."  : 
            state = copy.deepcopy(pos)
            state[r][c-2] = 'B'
            state[r][c] = '.'
            succ_pikachu.append(state)
        
        # now considering first step in left empty and another is full and there is another empty step after that
        if pos[r][c-1]=="." and (pos[r][c-2] in ["w","W","b","B"]) : 
            if pos[r][c-2]=="w" or pos[r][c-2]=="W":
                if c>=3 and state[r][c-3]==".": # we will jump to last empty step
                    state = copy.deepcopy(pos)
                    state[r][c-3] = 'B'
                    state[r][c-2] = '.'
                    state[r][c] = '.'
                    succ_pikachu.append(state)
            
        # now considering first step full and another is empty 
        if (pos[r][c-1] in ["w","W","b","B"]) and pos[r][c-2]=="." : 
            if pos[r][c-1]=="w" or pos[r][c-1]=="W":                                    
                state = copy.deepcopy(pos)
                state[r][c-2] = 'B' 
                state[r][c] = '.'
                state[r][c-1] = '.' 
                succ_pikachu.append(state)
        
        # considering first step full and then 2 steps empty and jumped on last empty slot 
        if c>=3 and (pos[r][c-1] in ["w","W","b","B"]) and pos[r][c-2]=="." and pos[r][c-3]=="." : 
            if pos[r][c-1]=="w" or pos[r][c-1]=="W":
                state = copy.deepcopy(pos)
                state[r][c-3] = 'B' 
                state[r][c-1] = '.'
                state[r][c] = '.'
                succ_pikachu.append(state)

def b_pikachu_right(pos,r,c,N,succ_pikachu):
    # cases in which we are moving right
    # one step is empty  
    if c<=N-1 and pos[r][c+1]==".":
            state = copy.deepcopy(pos)
            state[r][c+1] = 'B'
            state[r][c] = '.'
            succ_pikachu.append(state)
        
    if c<=N-2:
         # considering when 2 steps are empty on the right and we jump 2 steps right 
        if pos[r][c+1]=="." and pos[r][c+2]=="."  :                                     
            state = copy.deepcopy(pos)
            state[r][c+2] = 'B'
            state[r][c] = '.'
            succ_pikachu.append(state)
        
        # now considering first step in right empty and another is full and another empty step after that
        if pos[r][c+1]=="." and (pos[r][c+2] in ["w","W","b","B"]) : 
            if pos[r][c+2]=="w" or pos[r][c+2]=="W":
                if c<=N-3 and state[r][c+3]==".":
                    state = copy.deepcopy(pos)
                    state[r][c+3] = 'B'
                    state[r][c+2] = '.'
                    state[r][c] = '.'
                    succ_pikachu.append(state)
        
        # now considering first step full and another is empty 
        if (pos[r][c+1] in ["w","W","b","B"]) and pos[r][c+2]=="." : 
            if pos[r][c+1]=="w" or pos[r][c+1]=="W":
                state = copy.deepcopy(pos)
                state[r][c+2] = 'B' 
                state[r][c] = '.'
                state[r][c+1] = '.' 
                succ_pikachu.append(state)
        
        # considering first step full and then 2 steps are empty
        if c<=N-3 and (pos[r][c+1] in ["w","W","b","B"]) and pos[r][c+2]=="." and pos[r][c+3]=="." : 
            if pos[r][c+1]=="w" or pos[r][c+1]=="W":
                state = copy.deepcopy(pos)
                state[r][c+3] = 'B' 
                state[r][c+1] = '.'
                state[r][c] = '.'
                succ_pikachu.append(state)   
                # Generating all the successors of pikachu

def pikachu(pos,player):
    succ_pikachu=[]

    N=len(pos)-1
    if player=="w": # if the current player is white 
        for r in range(N):
               for c in range(len(pos[0])):
                    if pos[r][c] == 'W': 
                        w_pikachu_down(pos,r,c,N,succ_pikachu)
                        w_pikachu_left(pos,r,c,N,succ_pikachu)
                        w_pikachu_right(pos,r,c,N,succ_pikachu)

    else: #covered all the cases of black pikachu
         if player=="b": # all the moves if the current player is Black 
            for r in range(len(pos)):
               for c in range(len(pos[0])):
                    if pos[r][c] == 'B': 
                        b_pikachu_up(pos,r,c,N,succ_pikachu)
                        b_pikachu_left(pos,r,c,N,succ_pikachu)
                        b_pikachu_right(pos,r,c,N,succ_pikachu)   
                        


    return succ_pikachu                            

# ---------------------

# Generating all the successors of raichu


def w_raichu_below(pos,r,c,N,succ_raichu):
    opp=0
    row_value=0
    col_value=0
    # all the states for rs that are below the current position
    for i in range(r+1,len(pos)):
        # if we find same piece than just break 
        if pos[i][c] in ['w', 'W', '@'] :
            break
        # if we find opponent piece save its r and c and continue
        # if we have already found the opponent piece and another opponent comes then break as in a single
        # time it can kill only 1 opponent
        if pos[i][c] in ['b','B','$']:
            if opp==0:
                opp=1  
                row_value=i
                col_value=c
                continue
            else: break
        # if found an empty location get 1 state and if found this empty location after finding the opponent
        # piece than delete the opponent piece 
        if pos[i][c]==".":
            state = copy.deepcopy(pos)
            state[i][c] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        # done the same thing as above but for rs that are above the current piece positon 
def w_raichu_above(pos,r,c,N,succ_raichu):
    opp=0
    row_value=0
    col_value=0
    for i in range(r-1,-1,-1):
        if pos[i][c] in ['w', 'W', '@']:
            break
        if pos[i][c] in ['b','B','$']:  
            if opp==0:
                opp=1  
                row_value=i
                col_value=c
                continue
            else: break
        if pos[i][c]==".":
            state = copy.deepcopy(pos)
            state[i][c] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        #cumns right of current position
def w_raichu_right(pos,r,c,N,succ_raichu):
    opp=0
    row_value=0
    col_value=0
    for i in range(c+1,len(pos[0])):
        if pos[r][i] in ['w', 'W', '@']:
            break
        if pos[r][i] in ['b','B','$']:  
            if opp==0:
                opp=1  
                row_value=r
                col_value=i
                continue
            else: break
        if pos[r][i]==".":
            state = copy.deepcopy(pos)
            state[r][i] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        # cumns left of current position
def w_raichu_left(pos,r,c,N,succ_raichu):
    opp=0
    row_value=0
    col_value=0   
    for i in range(c-1,-1,-1):
        if pos[r][i] in ['w', 'W', '@']:
            break
        if pos[r][i] in ['b','B','$'] :  
            if opp==0:
                opp=1  
                row_value=r
                col_value=i
                continue
            else: 
                break
        if pos[r][i]==".":
            state = copy.deepcopy(pos)
            state[r][i] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        # Checking positive half diagonal
def w_raichu_pos_diag(pos,r,c,N,succ_raichu):
    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val-1 in range(0,len(pos))) and (col_up_val+1 in range(0,len(pos[0]))):
        row_up_val-=1
        col_up_val+=1
        if pos[row_up_val][col_up_val] in ['w', 'W', '@'] :
            break
        if pos[row_up_val][col_up_val] in ['b','B','$']:  
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                                
                        # Lower half negetive diagonal
    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val+1 in range(0,len(pos))) and (col_up_val-1 in range(0,len(pos[0]))):
        row_up_val+=1
        col_up_val-=1
        if pos[row_up_val][col_up_val] in ['w', 'W', '@']:
            break
        if pos[row_up_val][col_up_val] in ['b','B','$']:  
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        # Upper half negetive diagonal
def w_raichu_neg_diag(pos,r,c,N,succ_raichu):
    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val-1 in range(0,len(pos))) and (col_up_val-1 in range(0,len(pos[0]))):
        row_up_val-=1
        col_up_val-=1
        if pos[row_up_val][col_up_val] in ['w', 'W', '@']:
            break
        if pos[row_up_val][col_up_val] in ['b','B','$']: 
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                                
                        # Lower half negetive diagonal traversal

    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val+1 in range(0,len(pos))) and (col_up_val+1 in range(0,len(pos[0]))):
        row_up_val+=1
        col_up_val+=1
        if pos[row_up_val][col_up_val] in ['w', 'W', '@']:
            break
        if pos[row_up_val][col_up_val] in ['b','B','$']:  
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '@'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
    
    # All ways for black player
def b_raichu_below(pos,r,c,N,succ_raichu):
    opp=0
    row_value=0
    col_value=0
    # for rs that are below the current position
    for i in range(r+1,len(pos)):
        if pos[i][c] in ['b','B','$']:
            break
        if pos[i][c] in ['w', 'W', '@']:
            if opp==0:
                opp=1  
                row_value=i
                col_value=c
                continue
            else: break
        if pos[i][c]==".":
            state = copy.deepcopy(pos)
            state[i][c] = '$'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        # RS above the position
def b_raichu_above(pos,r,c,N,succ_raichu):
    opp=0
    row_value=0
    col_value=0
    for i in range(r-1,-1,-1):
        if pos[i][c] in ['b','B','$']:
            break
        if pos[i][c] in ['w', 'W', '@']:  
            if opp==0:
                opp=1  
                row_value=i
                col_value=c
                continue
            else: break
        if pos[i][c]==".":
            state = copy.deepcopy(pos)
            state[i][c] = '$'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        # Current positions after cumns
def b_raichu_cols(pos,r,c,N,succ_raichu):
    opp=0
    row_value=0
    col_value=0
    for i in range(c+1,len(pos[0])):
        if pos[r][i] in ['b','B','$']:
            break
        if pos[r][i] in ['w', 'W', '@']:  
            if opp==0:
                opp=1  
                row_value=r
                col_value=i
                continue
            else: break
        if pos[r][i]==".":
            state = copy.deepcopy(pos)
            state[r][i] = '$'
            state[r][i] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
    
    # Current position for cumns     
    opp=0
    row_value=0
    col_value=0   
    for i in range(c-1,-1,-1):
        if pos[r][i] in ['b','B','$'] :
            break
        if pos[r][i] in ['w', 'W', '@']:  
            if opp==0:
                opp=1  
                row_value=r
                col_value=i
                continue
            else: break
        if pos[r][i]==".":
            state = copy.deepcopy(pos)
            state[r][i] = '$'
            state[r][i] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                        
                        # Positive half of the upper diagonal states
def b_raichu_pos_diag(pos,r,c,N,succ_raichu):
    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val-1 in range(0,len(pos))) and (col_up_val+1 in range(0,len(pos[0]))):
        row_up_val-=1
        col_up_val+=1
        if pos[row_up_val][col_up_val] in ['b','B','$'] :
            break
        if pos[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '$'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
            
    # For states lower half diagonal
    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val+1 in range(0,len(pos))) and (col_up_val-1 in range(0,len(pos[0]))):
        row_up_val+=1
        col_up_val-=1
        if pos[row_up_val][col_up_val] in ['b','B','$'] :
            break
        if pos[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '$'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)

    # Upper half negetive diagonal traversal
    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val-1 in range(0,len(pos))) and (col_up_val-1 in range(0,len(pos[0]))):
        row_up_val-=1
        col_up_val-=1
        if pos[row_up_val][col_up_val] in ['b','B','$']:
            break
        if pos[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '$'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)
                                
                        # Lower half diagonal traversal
def b_raichu_neg_diag(pos,r,c,N,succ_raichu):
    row_up_val=r
    col_up_val=c
    opp=0
    row_value=0
    col_value=0   
    while (row_up_val+1 in range(0,len(pos))) and (col_up_val+1 in range(0,len(pos[0]))):
        row_up_val+=1
        col_up_val+=1
        if pos[row_up_val][col_up_val] in ['b','B','$']:
            break
        if pos[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opp==0:
                opp=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if pos[row_up_val][col_up_val]==".":
            state = copy.deepcopy(pos)
            state[row_up_val][col_up_val] = '$'
            state[r][c] = '.'
            if opp==1:
                state[row_value][col_value]="."
            succ_raichu.append(state)   
def raichu(pos,player):
    succ_raichu=[]
    if player=="w": # if the current player is white 
        for r in range(len(pos)):
               for c in range(len(pos[0])):
                    if pos[r][c] == '@': 
                       w_raichu_below(pos,r,c,N,succ_raichu) 
                       w_raichu_above(pos,r,c,N,succ_raichu)
                       w_raichu_right(pos,r,c,N,succ_raichu)
                       w_raichu_left(pos,r,c,N,succ_raichu)
                       w_raichu_pos_diag(pos,r,c,N,succ_raichu)
                       w_raichu_neg_diag(pos,r,c,N,succ_raichu)

    if player=="b": 
        for r in range(len(pos)):
               for c in range(len(pos[0])):
                    if pos[r][c] == '$': 
                        b_raichu_below(pos,r,c,N,succ_raichu)
                        b_raichu_above(pos,r,c,N,succ_raichu)
                        b_raichu_cols(pos,r,c,N,succ_raichu)
                        b_raichu_pos_diag(pos,r,c,N,succ_raichu)
                        b_raichu_neg_diag(pos,r,c,N,succ_raichu)

    return succ_raichu

# ---------------- Making an overall list of all successors and evaluation function values ----------------
def succ_eval_list(pos, player):
    successors = [] 
    if player == 'w':
        pichu_steps = pichu(pos,'w')
        pikachu_steps = pikachu(pos,'w')
        raichu_steps = raichu(pos,'w')
        for i in pichu_steps:
            successors.append([eval_func(i,'w', N), i])
        for i in pikachu_steps:
            successors.append([eval_func(i,'w', N), i])
        for i in raichu_steps:
            successors.append([eval_func(i,'w', N), i])

    else:
        pichu_steps = pichu(pos,'b')
        pikachu_steps = pikachu(pos,'b')
        raichu_steps = raichu(pos,'b')
        for i in pichu_steps:
            successors.append([eval_func(i,'b', N), i])
        for i in pikachu_steps:
            successors.append([eval_func(i,'b', N), i])
        for i in raichu_steps:
            successors.append([eval_func(i,'b', N), i])
        
    return sorted(successors, reverse= True)

# Reference: https://www.youtube.com/watch?v=mYbrH1Cl3nw

def eval_func(pos,player,N):
    
    b_pichu,B_pikachu,R_black,w_pichu,W_pikachu,R_white=0,0,0,0,0,0

    for x in pos:
        #pichu counts
        b_pichu += x.count('b')
        w_pichu += x.count('w')

        #pikachu counts
        B_pikachu += x.count('B')
        W_pikachu += x.count('W')

        #raichu counts
        R_black += x.count('$')
        R_white += x.count('@')
    
    num_moves = (N-1)*(N-1)*(N-1)
    
    if player=='w':    

        evaluated_value = num_moves * (R_white - R_black) + 9 * (W_pikachu - B_pikachu)+ 2 * (w_pichu - b_pichu)

        evaluated_value+=0.1*((all_moves(pos,'w')-all_moves(pos,'b')))
        return evaluated_value
    else:
        evaluated_value = num_moves * (R_black - R_white)+ 9 * (B_pikachu - W_pikachu)+ 2 * (b_pichu - w_pichu)
        evaluated_value+=0.1*((all_moves(pos,'b')-all_moves(pos,'w'))) 
        return evaluated_value
    
#--------------- Return the number of pichus and pikachus currently left ----------------------

def all_moves(pos,player):
    # Since there are very few raichus we can skip them
    return len(pichu(pos,player)) + len(pikachu(pos,player))

# converting the board back to string
def board_to_string(board, N):
    s = ''
    for i in range(0, len(board)):
        for j in board[i][0:N]:
            s += j
    return s

# -------------------- Checking if there is a winner -----------------------
def final_state(board):
    stringBoard=board_to_string(board,N)
    black_pieces = ["b", "B", "$"]
    white_pieces = ["w", "W", "@"]
    if any(piece in black_pieces for piece in stringBoard) == False or any(piece in white_pieces for piece in stringBoard) == False:
        return True
    elif any(piece in black_pieces[:1] for piece in stringBoard) == False or any(piece in white_pieces[:1] for piece in stringBoard) == False:
        return True
    return False
    

# Reference: Artificial Intelligence: A Modern Approach (Pearson Series in Artifical Intelligence) 
# Theoretical Reference: https://www.idtech.com/blog/minimax-algorithm-in-chess-checkers-tic-tac-toe
def max_value(board, player,depth):
    N = len(board) 
    if final_state(board) or depth > 5:
        return eval_func(board, player, N)
    for state in succ_eval_list(board, player):
        depth += 1
        val = max(eval_func(state[1], player, N), min_value(state[1], player, depth))
        return val

def min_value(board, player, depth):
    N = len(board)
    
    if player == 'b':
        player = 'w' 
    else:
        player = 'b'

    if final_state(board) == True or depth > 5:
        return eval_func(board, player,N)

    for state in succ_eval_list(board, player):
        depth += 1
        val = min(eval_func(state[1], player,N), max_value(state[1], player, depth))
        return val

def minimax_algo(board, player):
  succ = succ_eval_list(board, player)
  #print(succ)
  max_val = - sys.maxsize
  max_action = None
  for state in succ:
   # print("val: ", val)
    if player == 'b':
        val = max_value(state[1],player, 0 )
    else:
        val = min_value(state[1], player, 0)
        
    if val > max_val:
      max_val = val
      max_action = state[1]
  return max_action
 
# ------------------------- Finding the best move using the minimax algorithm -----------------------    
def find_best_move(board, N, player, timelimit):
    board_mat = board_matrix(board,N)
    minimax_ans = minimax_algo(board_mat, player)
    return [board_to_string(minimax_ans,N)]

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
