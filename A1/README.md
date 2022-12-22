# basrini-sborasan-krachoud-a1
Elements of Artificial Intelligence Assignment 1 
## Report for Assignment 1

### Problem 1: Birds, heuristics, and A*

**Initial State** : Given input array of unsorted birds/numbers
**Goal State** : Sorted order of numbers/birds
**State Space** : Position of each bird after each step pf swapping
**Heuristic Function** : Manhattan distance of the misplaced or unsorted birds/numbers
**Successor Function** : This function returns all the successive moves to be made to reach the goal state.

**Approach:**
The question was plain and simple and the main part to compute wat to find out the manhatten distane and take/choose the one with the least cost to help us reach the goal state.
The heuristic function computed looks like:
```sh
def h(state):
    heur_distance = []
    # calculating the Heuristic value(manhatten dist)
    for _, __ in zip(state, [1,2,3,4,5]):
        # taking difference and finding the absolute minimum of it
        difference = __ - _
        absolute_difference = abs(difference)
        # appending all the difference in the heur_distance variable
        heur_distance.append(absolute_difference)
        # returning the sum of the heuristic distance
    return sum(heur_distance)
```
### Problem 2: The Puzzle 2022
**Initial State** : Given input board.
**Goal State** : Sorted order of numbers in the given board.
**State Space** : Position of each element of the board after each step.
**Edge Weight** : Equal weight of each edge = 1
**Heuristic Function** : Modified version of Manhattan distance with addition of current cost.
**Successor Function** : This function returns all the successive moves made to reach the goal state by rotating it in all the ways given to us(row left, row right, column up, column down, outer clockwise, outer anti-clockwise, inner clockwise and inner anti-clockwise)

**Approach :** 
The solve function begins the process by creating a priority queue for the fringe using the heapq module, initializing an empty fringe, and tracking visited board states by using a dictionary that is initially filled with the initial board state.

The initial board, the initial cost (indicating the number of moves and edge weights and initialized as 0), the current cost, the current path travelled, and the most recent move are the starting items that are then entered into the fringe. The algorithm first determines if the successor is possible by looping through all of the potential successors of the present state of the board (move row 1-5 L or R, move column 1-5 U or D, move outer or inner ring clockwise or counterclockwise).

**Difficulties faced :**
- The problem faced by us was that it took a lot of time and the algorithm did not converge at first with only Manhatten distance. Afterwards we added the current cost and it helped converge the algorithm.
- We were not able to produce an optimal heuristic and feel like we are missing somethings to make it optimum.
- We think adding the square of depth of the would increase the the cost with more depth and would thus make the output more optimium but that exceeds the time for it to be computed.
- We could have also tried the approach to take other distances like Euclidean distance but that would again give us suboptimal outputs.
```sh
    while fringe:
        # getting state, current_cost, current_path from the fringe appended by the successor function
        _, (state, current_cost, current_path) = heapq.heappop(fringe)
        for (next_state, move, manhattan_cost) in successors(state):
            # terminating condition here
            if is_goal(next_state):
                return current_path + [move]
            else:
                if next_state not in traversed.keys():
                    # we only append if next state is not in the visited states so that if we do encounter the same node we need not recompute all the nodes for the given node again
                    traversed[next_state] = True
                    heuristic_val = current_cost + 1 + manhattan_cost
                    heapq.heappush(fringe, (heuristic_val, (next_state, current_cost + 1, current_path + [move])))
```

#### **Questions:** 
**1. In this problem, what is the branching factor of the search tree?**
Ans. 5 rows right moved + 5 rows left moved + 5 columns moved up + 5 columns moved down + 2 outer ring movements (clockwise and anti-clockwise) + 2 inner ring movements (clockwise and anti-clockwise) = 24
Therefore, the branching factor for the search tree is 24.

**2. If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A*** **search? A rough answer is fine.**
Ans. If the solution is reached in 7 moves, it would explore approximately 24^7^ states before we found the solution.


### Problem 3: Road Trip!
**Input format** : Parse the provided City Gps and Highway routes dataset into as:-
 {City:[radians(lat),radians(long)]} 
 {(start_city,end_city):{"length":'highway length',"SpeedLimit":'highway Speed Limit',"Hw Name":'highway name'}}
**Seach Space** : All the node segments present in our dataset.
**Initial State** : Given Starting city, Destination and cost function. Initialize a state to store all the corresponding travel parameters with initial city.
**Goal State** : Reaching the destination location and returning tyhe optimal travel path and parameters based on the given cost function.
**State Space** : All the node segments present in our dataset.
**Heuristic Functions** : 
- For segments: We are using a simple add 1 heuristing for both h and g scores.
- For distance: We for g score we are continually adding the the path distances and for heuristic we are using haversine distances and travel distance
- For time: the g score is increment highway distance/ speed limit and the heuristic uses haversine distances/ speed limit
- For delivery: the g score is increment highway distance/ speed limit and the heuristic does similar computation to time heuristic but also accounts for the probability of dropping the package if speed lim >= 50

**Successor Function** : The successor function takes in the current city, highway data and visited city list and appends all the new paths possible for a given current city and next city pair present in the dataset and not already visited

**Approach :** 
The approach to the solving process is mostly generic as in we take the init state in the form of starting city and run it through the successor funnction as above to generate all the next possible cities to visit and update the initial g, h and f scores accordingly.
Next, we use a priority sorting to get the highes priority node based on f score then we use that state to re run through its successors in a loop until we reach the destination city. At each step we continually add the moves taken in appropriate list to use as goal dump.
Once, IsGoal is triggerred we use the GoalDump function to return all the necessary parameters fr evaluation/display.

**Difficulties faced :**
- We faced difficulties in deciding the best data structure and storage format for the dataset itself as each different approach has a different necessity for parsing. In the end, we have used dictionary as the primary format and list for [lat,long] and nested dictionary to store the highway dataset
- next we had to decide the parameters in Travel state and how to trace back the path. We finally agreed on using a list inside the state and append the new moves and finally directly return
- we faced a lot of trouble with the type of priority queue as well as heapq doesnt handle state comparisons so we had to use regular list with sort function.
```sh
# hvsin_dist : it appropriates physical spherical distance betrween two given points/locations with given latitude and longitude info
def hvsin_dist(StartingPoint,EndingCity,GpsDict):
    Slat,Slon = GpsDict[StartingPoint][0],GpsDict[StartingPoint][1]
    Elat,Elon = GpsDict[EndingCity][0],GpsDict[EndingCity][1]
    lon_diff = Elon - Slon 
    lat_diff = Elat - Slat
    # calculating the sine to check the condition
    a = sin(lat_diff/2)**2 + cos(Slat) * cos(Elat) * sin(lon_diff/2)**2
    c = 2 * asin(sqrt(abs(a)))
    return(3956 * c)

# dist_h : calculates the distance between two given locations using the hvsin_dist function
def dist_h(StartingPoint,EndingCity,GpsDict,Prevh,Prevg):
    if StartingPoint in GpsDict:return hvsin_dist(StartingPoint,EndingCity,GpsDict)
    else:return Prevh - Prevg
    
# time_h : calculates the time given between two locations using hvsin_dist distance function divided by optimal speed which we have considered as 70 mph
def time_h(StartingPoint,EndingCity,GpsDict,HighwayDict,TravelDist,TravelledDist):
    bestSpd = 70
    if StartingPoint in GpsDict.keys(): return hvsin_dist(StartingPoint,EndingCity,GpsDict)/bestSpd  
    else : return (TravelDist-TravelledDist)/bestSpd
 
# delivery_h : it expands upon the given probability of package delivery time using the provided probability function if the speed limit is exceeded beyond 50 mph.
def delivery_h(TravelParams):
    delhrs = 0
    tt = 0
    for i in range(len(TravelParams.drivinginstr)):
        dropprob = 0
        if float(TravelParams.hwspdlmts[i]) >=50:
            dropprob = tanh(TravelParams.segmentlen[i]/1000)
            tr = TravelParams.segmentlen[i]/TravelParams.hwspdlmts[i]
            tt = sum(list(TravelParams.segmentlen[x]/TravelParams.hwspdlmts[x] for x in range(i)))
            delhrs +=  tr + 2 * dropprob * ( tr + tt )
        else:
            delhrs+= TravelParams.segmentlen[i]/TravelParams.hwspdlmts[i]
    return delhrs

# GoalDump : it returns the output in the necessary format
def GoalDump(TravelParams):
    Hrs= sum([float(TravelParams.segmentlen[i])/float(TravelParams.hwspdlmts[i]) for i in range(len(TravelParams.drivinginstr))])
    return {"total-segments" : len(TravelParams.drivinginstr),
    "total-miles" : sum(list(TravelParams.segmentlen)),
    "total-hours" : Hrs,
    "total-delivery-hours" : delivery_h(TravelParams),
    "route-taken" : TravelParams.drivinginstr}
```
