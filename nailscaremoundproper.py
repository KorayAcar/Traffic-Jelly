import math as m
import random as r
r.seed(0)

def roadsim2d(opts):
    # function inputs are processed here for greater clarity
    
    # no. time steps simulated
    if opts.get("duration")==None:
        opts.update({"duration":30})
    duration=opts["duration"]
    
    # no. lanes on the road
    if opts.get("lanes")==None:
        opts.update({"lanes":4})
    lanes=opts["lanes"]
    
    # length of road
    if opts.get("length")==None:
        opts.update({"length":100})
    length=opts["length"]
    
    # initial state of road, empty by default
    if opts.get("initial")==None:
        opts.update({"initial":[[] for i in range(lanes)]})
    road=opts["initial"]
    
    # maximum speed allowed
    if opts.get("maxspeed")==None:
        opts.update({"maxspeed":10})
    maxspeed=opts["maxspeed"]
    
    # brake chance, 20% by default
    if opts.get("brake")==None:
        opts.update({"brake":0.2})
    p=opts["brake"]
    
    # amount of cars to enter road from the start over time, cannot exceed 1 per lane per time step
    if opts.get("involume")==None or opts.get("involume")>1:
        opts.update({"involume":1})
    ivol=opts["involume"]
    
    # max speed of entering cars
    if opts.get("inmaxspeed")==None or opts.get("inmaxspeed")>opts.get("maxspeed"):
        opts.update({"inmaxspeed":opts.get("maxspeed")})
    imax=opts["inmaxspeed"]
    
    # min speed of entering cars
    if opts.get("inminspeed")==None or opts.get("inminspeed")<0:
        opts.update({"inminspeed":imax//2+1})
    imin=opts["inminspeed"]
    
    # starting value of unique IDs (license plates), make sure to have this exceed max ID for the initial condition, 0 by default
    if opts.get("uid")==None:
        opts.update({"uid":0})
    uid=opts["uid"]
    
    # allows cars to switch even if there is a car right in front of them, False by default
    if opts.get("sideswitch")==None:
        opts.update({"sideswitch":False})
    sideswitch=opts["sideswitch"]
    
    # allows cars to brake harder to avoid "collisions", nonexistent by default. greater the number, harder the brake
    if opts.get("breaking")==None:
        opts.update({"breaking":1})
    breaking=opts["breaking"]
    
    # time it takes for a car to make it to the end of the road will be measured from this ID number onwards, set to -1 to turn off, waits for the system to get consistent by default
    if opts.get("measurefrom")==None:
        opts.update({"measurefrom":(lanes*length)//maxspeed})
    measure=opts["measurefrom"]
    
    # initialize simulation
    roads=[[[] for i in range(lanes)] for i in range(duration)]
    roads.insert(0,road)
    measurements=[[]]
    
    i=1
    while i<=duration:
        # generate new cars
        for lane in road:
            prob=r.uniform(0,1)
            if prob+ivol>1 and (len(lane)<1 or lane[-1][1]>0):
                #cars travel along the road according to position, and are sorted by position RTL
                lane.append([uid,0,m.ceil(imin+prob*(imax-imin)),False,0])
                uid=uid+1
        # handle switching across all lanes, from the leftmost (topmost) lane
        for lane in range(len(road)):
            #initialize B,C,F. B=A-1,D=C-1,F=E-1
            B=-1
            C=0
            F=-1
            if lane>0 and len(road[lane-1])!=0:
                B=0
            if lane<lanes-1 and len(road[lane+1])!=0:
                F=0
            while(C<len(road[lane])):
                #switching logic
                while(C>-1 and C<len(road[lane]) and road[lane][C][3]):
                    C=C+1
                while(B<0 or (B>-1 and lane>0 and B<len(road[lane-1]) and road[lane-1][B][1]>=road[lane][C][1])):
                    B=B+1
                B=B-1
                while(F<0 or (F>-1 and lane<lanes-1 and F<len(road[lane+1]) and road[lane+1][F][1]>=road[lane][C][1])):
                    F=F+1
                F=F-1
                road[lane][C][3]=True
                if lane>0 and C>0 and road[lane][C][1]+road[lane][C][2]>=road[lane][C-1][1] and (sideswitch or road[lane][C-1][1]-road[lane][C][1]>1) and (B<0 or road[lane-1][B][1]-road[lane][C][1]>1):
                    road[lane-1].insert(B+1,road[lane].pop(C))
                elif lane<lanes-1 and C>0 and (sideswitch or road[lane][C-1][1]-road[lane][C][1]>1) and (sideswitch or road[lane][C-1][1]-road[lane][C][1]>1) and (F<0 or road[lane+1][F][1]-road[lane][C][1]>1):
                    road[lane+1].insert(F+1,road[lane].pop(C))
                else:
                    C=C+1
        # apply 1D model across all lanes
        for lane in range(len(road)):
            C=0
            while(C<len(road[lane])):
                if(C!=0):
                    speed=max(min(maxspeed,road[lane][C][2]+1,m.ceil((road[lane][C-1][1]-road[lane][C][1]-1)/breaking))-m.floor(r.uniform(p,p+1)),0)
                else:
                    speed=max(min(maxspeed,road[lane][C][2]+1)-m.floor(r.uniform(p,p+1)),0)
                if road[lane][C][1]+speed<=length:
                    roads[i][lane].append([road[lane][C][0],road[lane][C][1]+speed,speed,False,road[lane][C][4]+1])
                elif road[lane][C][0]>=measure and measure>=0:
                    measurements[0].append([road[lane][C][0],road[lane][C][4]])
                C=C+1
        road=roads[i]
        i=i+1
    return {"simulation":roads,"timetaken":measurements[0]}
roads=roadsim2d({"duration":200})
