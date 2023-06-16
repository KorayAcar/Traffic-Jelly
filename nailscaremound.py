import math as m
import numpy as np
import random as r
def roadgen1d(length,cars):
    # empty cell = -1
    # cell with car >= 0, number represents speed
    road=np.full(length,-1)
    for i in r.sample(range(length),cars):
        road[i]=0
    return road
def roadsim1d(road,duration,mspeed=5,p=0,breaking=1,loop=True):
    length=len(road)
    roads=np.full((duration+1,length),-1)
    roads[0]=road
    speed=0
    for i in range(duration):
        # A: empty cell before next car
        A=0
        while roads[i,A]<0:
            A+=1
            if A==length:
                return roads
        A+=length-1
        # B: cell with current car
        B=length-1
        while B>=0:
            if(roads[i,B]<0):
                B-=1
                continue
            # apply all 3 rules at once
            speed=max(min(mspeed,roads[i,B]+1,m.ceil((A-B)/breaking))-m.floor(r.uniform(p,p+1)),0)
            # move the car, if car goes off the right it only appears on the left if loop
            if(loop or B+speed<length):
                roads[i+1,(B+speed)%length]=speed
            B-=1
            A=B
    return roads









roads=roadsim1d(roadgen1d(100,15),100,10,0.2,2,False)






