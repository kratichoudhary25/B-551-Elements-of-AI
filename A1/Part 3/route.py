#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Balajee Devesha Srinivasan basrini
#          Smit Borasaniya sborasan
#          Krati Choudhary
#
# !/usr/bin/env python3

import sys
from heapq import *
from math import *

#----------------------------------------------------Parsing Data------------------------------------------------------#
def ParseDataset(CityDataset,RoadDataset):
    # Parsing the given data into Gps dictionary and a nested dictionary of starting city to ending city as a pair with
    # their parameters as keys
    CityDict = dict()
    HighwayDict = dict()
    # for loop to read CityFile
    with open(CityDataset,"r") as CityFile:
        for lines in CityFile:
            #splitting lat long and city
            City,Lat,Long = lines.strip().split(' ')
            # updating it to its CityDict
            CityDict.update({City: [radians(float(Lat)),radians(float(Long))]})
    # for loop to read RoadFile
    with open(RoadDataset,"r") as RoadFile:
        for lines in RoadFile.readlines():
            # splitting StartingCity,EndingCity,dist,spd,hwname
            StartingCity,EndingCity,dist,spd,hwname = lines.strip().split(' ')
            # updating it to its HighwayDict
            HighwayDict.update({(StartingCity,EndingCity) : {"Length":dist,"Spdlmt":spd,"Highway":hwname}})
            HighwayDict.update({(EndingCity,StartingCity) : {"Length":dist,"Spdlmt":spd,"Highway":hwname}})         
    return CityDict,HighwayDict

#----------------------------------------------------Heuristics------------------------------------------------------#

# Haversine formula for calculating distance between 2 points is taken from
# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

def hvsin_dist(StartingPoint,EndingCity,GpsDict):
    # Cheking if the StartingPoint is part of the provided GPS data mostly to check if we started from a city instead of jucntions
    try:
        Slat,Slon = GpsDict[StartingPoint][0],GpsDict[StartingPoint][1]
        Elat,Elon = GpsDict[EndingCity][0],GpsDict[EndingCity][1]
        lon_diff = Elon - Slon 
        lat_diff = Elat - Slat
        # calculating the sine to check the condition
        a = sin(lat_diff/2)**2 + cos(Slat) * cos(Elat) * sin(lon_diff/2)**2
        c = 2 * asin(sqrt(abs(a)))
        return(3956 * c)
    except:
        print("Starting point not part of GPS data.")


def dist_h(StartingPoint,EndingCity,GpsDict,Prevh,Prevg):
    # Using the Haversine distance for heuristic for the distance
    # Cheking if the StartingPoint is part of the provided GPS data else use the older existing data to update heuristic
    if StartingPoint in GpsDict:return hvsin_dist(StartingPoint,EndingCity,GpsDict)
    else:return Prevh - Prevg
        
def time_h(StartingPoint,EndingCity,GpsDict,HighwayDict,TravelDist,TravelledDist):
    # Time heuristic for detrmining the best possible time if we travel at 70mph which is higher than the max allowable speed in highways
    # best speed is the maximum speed taken empirically
    bestSpd = 70
    if StartingPoint in GpsDict.keys(): return hvsin_dist(StartingPoint,EndingCity,GpsDict)/bestSpd  
    else : return (TravelDist-TravelledDist)/bestSpd
        
def delivery_h(TravelParams):
    # heuristic function to calculate the delivery time with given tanh condition
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

# Goal dump function to return all the necessary final state parameters if goal condition is reached
def GoalDump(TravelParams):

    Hrs= sum([float(TravelParams.segmentlen[i])/float(TravelParams.hwspdlmts[i]) for i in range(len(TravelParams.drivinginstr))])
    return {"total-segments" : len(TravelParams.drivinginstr),
    "total-miles" : sum(list(TravelParams.segmentlen)),
    "total-hours" : Hrs,
    "total-delivery-hours" : delivery_h(TravelParams),
    "route-taken" : TravelParams.drivinginstr}

#----------------------------------------------------TravelParam class------------------------------------------------------#

class TravelParams:
    def __init__(self,StartingCity,EndingCity,dist,Spdlmt,hwname):
        # Python class object for storing all the possible values required in a state to process output
        self.StartingCity = StartingCity
        self.EndingCity = EndingCity
        self.TravelledDist = float(dist)
        self.Spdlmt = float(Spdlmt)
        self.hwname = hwname
        # list storing road lengths of travelled highways
        self.segmentlen = list()
        # list storing speed limits of travelled highways
        self.hwspdlmts = list()
        # list storing Driving instruction for final route of travelled highways and locations
        self.drivinginstr = list()
        # New move appended as a path instruction
        self.curpath = (EndingCity,str(str(hwname) + " for " + str(dist) + " miles"))
        # A* Heuristic scores
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0 
    # property function for calculating the f score of state
    @property
    def update_f_score(self):
        self.f_score = self.g_score + self.h_score

#----------------------------------------------------Successors and goal checking---------------------------------------------#
        
def successors(CurLocation,HighwayDat,VisitedCities):
    # Successor function checks if the start end pair of highway data has our starting condition 
    # and also if the new travel city has been visited or not
    CheckStates = list()
    for StartEndpair in HighwayDat.keys():
        if CurLocation == StartEndpair[0] and StartEndpair[1] not in VisitedCities:
            # Creating a new instance of TravelParams for each possible start end pair possible with corresponding values
            CheckStates.append(TravelParams(StartEndpair[0],StartEndpair[1],HighwayDat[StartEndpair]["Length"],HighwayDat[StartEndpair]["Spdlmt"],HighwayDat[StartEndpair]["Highway"]))
    return CheckStates

def is_goal(TravelParams,EndingCity):
    # Checking if the new states ending point is equal to the given ending point 
    return TravelParams.EndingCity == EndingCity

#-------------------------------------------------------- Core Loop ---------------------------------------------------------#
def get_route(StartingCity, EndingCity, CostFunct):
    # Parsing the input data into GPS data and Highway data
    GpsDat,HighwayDat = ParseDataset("city-gps.txt","road-segments.txt")
    
    # Start to end distance 
    TravelDist = hvsin_dist(StartingCity,EndingCity,GpsDat)
    # Initializing 2 lists for storing visited states and cities to prevent infinite looping and appending starting city into it
    HpQ = list()
    VisitedStates = list()

    VisitedCities = [StartingCity]
#-------------------------------------------------------- state inits ---------------------------------------------------------#    
    # Initializations for the g and h scores
    
    for InitState in successors(StartingCity,HighwayDat,VisitedCities):
        # print(InitState.StartingCity,InitState.EndingCity)
        
        TravelledDist = InitState.TravelledDist
        if CostFunct == "segments":
            # Simple 1 cost for segment travel heuristics with 1 incrementing g scores per state 
            InitState.g_score,InitState.h_score = 0,1
        elif CostFunct == "distance":
            # Initializing using max distance and subsequently penalizing for each long move as TravelledDist
            # and dist_h heuristic based on haversine distances of locations
            InitState.g_score,InitState.h_score = TravelledDist,dist_h(StartingCity,EndingCity,GpsDat,0,InitState.g_score)
        elif CostFunct == "time":
            # Initializing g with 0 and h with the time_h heuristic that calculates haversine distcances between points and
            # divides them with 70mph max speed for time heuristic
            InitState.g_score,InitState.h_score = 0,time_h(StartingCity,EndingCity,GpsDat,HighwayDat,TravelDist,TravelledDist)
        elif CostFunct == "delivery":
            # Initializing g and h = 0 and handling the later cases using the delivery_h heuristic that uses the provided 
            # probability as h function and g 
            InitState.g_score,InitState.h_score = 0,0
        
        # updating f scores
        # adding the currently travelled state i.e. ending city into Visitied cities
        InitState.update_f_score
        VisitedCities.append(InitState.EndingCity)
        # print(InitState.f_score)
        InitState.drivinginstr.append(InitState.curpath)
        InitState.hwspdlmts.append(InitState.Spdlmt)
        InitState.segmentlen.append(InitState.TravelledDist)
        
        # appending the initialized states and corresponding fscores into the queue before sorting based on priorities pf their f score
        HpQ.append(InitState)
        
    # Converting the list into prioritized queue by sorting using f_score
    HpQ.sort(key = lambda State:State.f_score)
#-------------------------------------------------------- succesive states  ---------------------------------------------------------#    
    while HpQ:
        # Popping the top priority state from the queue
        PrioState =HpQ.pop(0)
        # print(PrioState.StartingCity,PrioState.EndingCity)
        
        # Checking if goal state is reached 
        if is_goal(PrioState,EndingCity):
            #print("reached goal")
            return GoalDump(PrioState)
        
        # Executing successors fucntion and storing in the state list
        succ_states = successors(PrioState.EndingCity,HighwayDat,VisitedCities)
        # print(succ_states)
        VisitedCities.append(PrioState.EndingCity)
        
        for NextState in succ_states:
            
            # After aquiring the new successor states from priority q we now append the previous moves to the state to create a
            # Backtracking log for path instructions, speed limits and travel distances and typecasting them as float to avoing 
            # integer to string 
            NextState.drivinginstr.extend(PrioState.drivinginstr + [NextState.curpath])
            NextState.hwspdlmts.extend(PrioState.hwspdlmts + [NextState.Spdlmt])
            NextState.segmentlen.extend(PrioState.segmentlen + [NextState.TravelledDist])
            #print(NextState.drivinginstr,"|",NextState.hwspdlmts,"|",NextState.segmentlen)
            
            TravelledDist += NextState.TravelledDist
            
            #Updating the heuristics using the previous state values and updating the new values into a new state 
            if CostFunct == 'segments':
                NextState.g_score,NextState.h_score = (PrioState.g_score + 1),(PrioState.h_score + 1)
            elif CostFunct == 'distance':
                NextState.g_score,NextState.h_score = (PrioState.g_score + NextState.TravelledDist),dist_h(StartingCity,EndingCity,GpsDat,0,InitState.g_score)
            elif CostFunct == 'time':
                NextState.g_score, NextState.h_score = (PrioState.g_score + (NextState.TravelledDist) / NextState.Spdlmt),time_h(StartingCity,EndingCity,GpsDat,HighwayDat,TravelDist,TravelledDist)
            elif CostFunct == 'delivery':
                NextState.g_score,NextState.h_score = (PrioState.g_score + (NextState.TravelledDist) / NextState.Spdlmt),delivery_h(NextState)
            
            #again updating the f scores
            NextState.update_f_score
            #adding the travelled sucessor cities into the visited city list
            VisitedCities.append(NextState.EndingCity)
        #   print(VisitedCities)
        # Appending the the visited state into visited state list
        VisitedStates.append(PrioState)
        # print(VisitedStates)
        # looping through the succesors lists to add new states not present in visited states and queue into the priority queue
        for state in succ_states:
            if state in HpQ:
                continue
            elif state in VisitedStates:
                continue
            else :
                HpQ.append(state)
            # print(HpQ)
        # Recalculating priority based on f scores
        HpQ.sort(key = lambda x:x.f_score)
        

# Please don't modify anything below this line

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
