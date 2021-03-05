# %%
import numpy as np, pandas as pd
import bisect
import re
from collections import deque
import threading

# %%
"""
 Latitude/Longitude tree creation:
 currently, we are building Tree for India whose coordinates are lat=(8,37), long =(68,97)
 We create a tree whose lat/long are in (7,39) and (66,99) respectively. This was done to handle overflow/underflow
 while tackling moving users
"""
def CreateGPSTree(gps, contact_dist):
    if gps == 'lat':
        start_degree = 7
        end_degree   = 39
    elif gps == 'long':
        start_degree = 66
        end_degree   = 99
    else:
        raise ValueError("Only allowed options are: 'lat' and 'long' ")
    minute = 60
    seconds= 60
    partition = int(30/contact_dist)
    tree = dict()
    for i in range(start_degree,end_degree):
        tree[i] = dict()
        for j in range(0,minute):
            tree[i][j] = dict()
            for k in range(0,seconds):
                tree[i][j][k]=dict()
                for l in range(0,partition):
                    tree[i][j][k][l] = []
    return tree

# %%
"""
 Map lat/long in the tree
"""
def MapGPS(tree, data, contact_dist):  
    partition = int(30/contact_dist)
    interval = np.linspace(1/partition,1,partition)
    #yo=''
    for idx in range(0, len(data)):
        degree, minute, second = data.iloc[idx]
        second_int = int(second)
        second_frac = second - second_int
        #yo=degree
        dec_ind = bisect.bisect_left(interval, second_frac)
#         #print(degree, minute, second_int, dec_ind)
        tree[str(degree)][str(minute)][str(second_int)][str(dec_ind)].append([idx,[degree,minute,second]])
    ##print(tree[str(yo)])
       

# %%
"""
 Map lat/long in the tree using parallel implemention
"""
def MapGPSInParallel(i_d, tree, contact_dist):  
    partition = int(30/contact_dist)
    interval = np.linspace(1/partition,1,partition)
    idx, data = i_d
    degree, minute, second = data
    second_int = int(second)
    second_frac = second - second_int
    dec_ind = bisect.bisect_left(interval, second_frac)
#     tree[str(degree)][str(minute)][str(second_int)][str(dec_ind)].append(idx)
    l = tree[str(degree)][str(minute)][str(second_int)][str(dec_ind)]
    l.append(idx)
    tree[str(degree)][str(minute)][str(second_int)][str(dec_ind)] = l

# %%

def inters(a,b):

	return None
from math import radians, cos, sin, asin, sqrt 
def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r)*1000 
      
      
def dist(x,y):
	if distance(dms2dd((x[0],x[1],x[2])),dms2dd((y[0],y[1],y[2])),0,0)<=5:
		return True
	

	
def findp(a,b):
	yo=[]
	for i in range(0,len(a)):
		for j in range(0,len(b)):
			if dist(a[i][1],b[j][1]):
				yo.append(sorted([a[i][0],b[j][0]]))
	return yo
def inters(a,b):
	a=set(tuple(row) for row in a)
	b=set(tuple(row) for row in b)
	return  set(a).intersection(set(b))


def hotspot(tree,tree1,t,a,data):
   
    start_degree = 7
    end_degree   = 39
    start_degree1 = 66
    end_degree1   = 99
    x=[]
    for i in a:
        x.append(i[0],i[1])
    minute = 60
    seconds= 60
    partition = int(30/5)
    possible=[]
    for i in range(start_degree,end_degree):
        for j in range(0,minute):
            for k in range(0,seconds):
                for l in range(0,partition):
                    if len(tree[i][j][k][l])>t and tree[i][j][k][l][0] in x:
                        possible.append([i,j,k,l])
    possible1=[]
    for i in range(start_degree,end_degree):
        for j in range(0,minute):
            for k in range(0,seconds):
                for l in range(0,partition):
                    if len(tree[i][j][k][l])>t and tree[i][j][k][l][0] in x:
                        possible.append([i,j,k,l])
    
    return possible

def hotspotpeople(lat,long,latt,longt):


    avgdist= 5    #5 min around 9km
    minute = 60
    contact_dist=5
    partition = int(30/contact_dist)
    people =[]
    interval = np.linspace(1/partition,1,partition)
    degree, minute, second = lat[0],lat[1],lat[2]
    second_int = int(second)
    second_frac = second - second_int

    dec_ind = bisect.bisect_left(interval, second_frac)
    i,j,k,l=degree, minute, second_int,dec_ind
    target_coord = (i,j,k,l)
    startdeg,startmin = submin(target_coord, avgdist)
    enddeg,endmin   = addmin(target_coord, avgdist)
    
    for a in range(startdeg, enddeg+1):
        x=0
        y=60
        if a==startdeg:
            x=startmin
        if a==enddeg:
            y=endmin
        for b in range(x,y):
            for c in range(0,60):
                for d in range(partition):
                    if len(latt[str(a)][str(b)][str(c)][str(d)])>0 :
                        people.append(latt[str(a)][str(b)][str(c)][str(d)][0][0])
    
    degree, minute, second = long[0],long[1],long[2]
    second_int = int(second)
    second_frac = second - second_int
    #print('----------------------------')
    dec_ind = bisect.bisect_left(interval, second_frac)
    i,j,k,l=degree, minute, second_int,dec_ind
    target_coord = (i,j,k,l)
    startdeg,startmin = submin(target_coord, avgdist)
    enddeg,endmin   = addmin(target_coord, avgdist)
    
    for a in range(startdeg, enddeg+1):
        x=0
        y=60
        if a==startdeg:
            x=startmin
        if a==enddeg:
            y=endmin
        for b in range(x,y):
            for c in range(0,60):
                for d in range(partition):
                    if len(longt[str(a)][str(b)][str(c)][str(d)])>0 :
                        people.append(longt[str(a)][str(b)][str(c)][str(d)][0][0])
                     
    return people  

def realhotspotpeople(lat,long,data,data1,x):
    people=[]
    lengthofcity=10000#->Consider 10km by 10km CITY AREA
    for idx in x:
        degree, minute, second = data.iloc[idx]
        a=dms2dd((degree, minute, second))
        degree, minute, second = data1.iloc[idx]
        a1=dms2dd((degree, minute, second))
        if distance(dms2dd(lat),a,dms2dd(long),a1)<lengthofcity:
            people.append(idx)    
        
    return people

    
def deftomap(x,data, data1,covid19pos,Suspected):
    #map=gmapapi()
    for i in x:
        lat=data[i]
        long=data1[i]
        color='blue'#ith is NORMAL(COVID -ive)
        a,b=covid19pos[i],Suspected[i]
        if b==1:
            color='orange'#ith is SUSPECTED
        if a==1:
            color='red'#ith is COVID +ive
        #map.maptograph(lat,long,i,color)
        #WHICH CAN BE DONE AFTER BUYING GOOGLE MAP SUBSCRIPTION TO ACCESS MAP AND API CAN BE CALLED THEN
    #return map.plot()
    
"""
Static case: when the user make contact at one location
Function to find intersection over two sets of coordinatess 
"""
def IntersectGPSTree(tree_before, tree_after,  gps, contact_dist):
    if gps == 'lat':
        start_degree = 7
        end_degree   = 39
    elif gps == 'long':
        start_degree = 66
        end_degree   = 99
    else:
        raise ValueError("Only allowed options are: 'lat' and 'long' ")
    minute = 60
    seconds= 60
    partition = int(30/contact_dist)
    #print(partition)
    contact_points =list()
    contact_points1 =list()
    
    com=[]
    com1=[]
    com2=[]
    com3=[]
    flag=True
    for i in range(start_degree,end_degree):
        for j in range(0,minute):
            for k in range(0,seconds):
                for l in range(partition):
                    # make sets out of lists
                    temp=[]
                    loc=[]
                    for m in tree_before[str(i)][str(j)][str(k)][str(l)]:
                    	temp.append(m[0])
                    	loc.append(m)
                    if i==j==k==l==0:
                    	com=loc.copy()
                    else:
                    	com1=loc.copy()
                    	pairwhichAreLessThan5mt=findp(com,com1)
                    	com=com1.copy()
                    set1=set(temp)
                    temp=[]
                    loc=[]
                    for m in tree_after[str(i)][str(j)][str(k)][str(l)]:
                    	temp.append(m[0])
                    	loc.append(m)
                    if i==j==k==l==0:
                    	com2=loc.copy()
                    else:
                    	com3=loc.copy()
                    	pairwhichAreLessThan5mt_1=findp(com2,com3)
                    	com2=com3.copy()
                    
                    set2=set(temp)
                    common = (set1.intersection(set2))
                    if len(common) > 1 : # not considering singleton set
                        contact_points.append(common)
                    if not(i==j==k==l==0):
                  
                        common1=inters(pairwhichAreLessThan5mt,pairwhichAreLessThan5mt_1)
                        if len(common1) > 1 : # not considering singleton set
                            contact_points1.append(common1)
                    
#                     store only contact points in a list as it is
    # #print('#',contact_points1)                
    return contact_points,contact_points1                
#                     returning dict of contact points take too much time
#                     for people in people_in_contacts:
#                         contact_points[people].extend(people_in_contacts-{people})

# %%
"""
Dynamic case: when the users are moving together, we need to have good estimate of user's speed
For Pedestrains:
        Avg speed of pedestrain is around 1.4 m/s. That means, in 5 mins, they will travel 420m which is 
        approx 14" sec time in GPS coordinates (420/30). Therefore, two people walking together can change their 
        clusters which are 14" left or right of the current cluster.
For cars and other vehicles:
        avg. speed can be taken around 100 km/h. So they will travel around 8.3 Km in 5 mins which is equal to 350" 
        in GPS coordinates. Therefore, two people in car can change their clusters which are 350" left or right of the
        current cluter.
Function to find intersection over two sets of coordinatess 
"""
def PedestrianIntersectGPSTree(tree_before, tree_after,  gps, contact_dist):
    if gps == 'lat':
        start_degree = 8
        end_degree   = 38
    elif gps == 'long':
        start_degree = 67
        end_degree   = 98
    else:
        raise ValueError("Only allowed options are: 'lat' and 'long' ")
    avgdist= 14
    minute = 60
    seconds= 60
    partition = int(30/contact_dist)
    contact_points =list()
    for i in range(start_degree, end_degree):
        for j in range(0,minute):
            for k in range(0,seconds):
                for l in range(partition):
                    set1 = set(tree_before[str(i)][str(j)][str(k)][str(l)])
                    target_coord = (i,j,k,l)
#                   find start and end of the cluster search coordinates
                    start        = subsec(target_coord, avgdist)
                    end          = addsec(target_coord, avgdist)
#                      There is possibility that start min and sec are greater than end min/sec so wrap around
                    if start[1]> end[1]:
                        mins = np.arange(start[1], 60 + end[1]+1)%60
                    else:
                        mins = np.arange(start[1], end[1]+1)
                    if start[2]> end[2]:
                        secs = np.arange(start[2], 60 + end[2]+1)%60
                    else:
                        secs = np.arange(start[2], end[2]+1)
#                     if i==10 and j==0 and k==0 and l==6:
#                         #print('atget:', target_coord)
#                         #print("set 1:",set1)
#                         #print("mins:", mins)
#                         #print("sec:", secs)
                    for a in range(start[0], end[0]+1): # + 1 to account for cases when user does not change degree/mins
                        for b in mins:
                            for c in secs:
                                for d in range(partition):
                                    # make sets out of lists
                                    set2 = set(tree_after[str(a)][str(b)][str(c)][str(d)])
#                                     if i==10 and j==0 and k==0 and l==6:
#                                         if a==10 and b==0 and c==10 and d == 6:
#                                         #print("set 1:", set1," set 2:",set2)

                                    common = (set1.intersection(set2))
                                    if len(common) >1 : # not considering singleton set
                                        contact_points.append(common)
                     
    return contact_points  

# %%
"""
Dynamic case: when the users are mvoing together, we need to have good estimate of user's speed
For Pedestrains:
        Avg speed of pedestrain is around 1.4 m/s. That means, in 5 mins, they will travel 420m which is 
        approx 14" sec time in GPS coordinates (420/30). Therefore, two people walking together can change their 
        clusters which are 14" left or right of the current cluster.
For cars and other vehicles:
        avg. speed can be taken around 100 km/h. So they will travel around 8.3 Km in 5 mins which is equal to 350" 
        in GPS coordinates. Therefore, two people in car can change their clusters which are 350" left or right of the
        current cluter.
Function to find intersection over two sets of coordinatess 
"""
def FastPedestrianIntersectGPSTree(tree_before, tree_after,  gps, contact_dist):
    if gps == 'lat':
        start_degree = 8
        end_degree   = 38
    elif gps == 'long':
        start_degree = 67
        end_degree   = 98
    else:
        raise ValueError("Only allowed options are: 'lat' and 'long' ")
    avgdist= 14
    minute = 60
    seconds= 60
    partition = int(30/contact_dist)
    contact_points =list()
#     first insert gps coordiantes which are 14" left and right of the starting GPS
    dq=deque()
    startGPS = (start_degree,0,0,0)
#      find start and end of the cluster search coordinates
    start        = subsec(startGPS, avgdist)
    end          = addsec(startGPS, avgdist)
#      There is possibility that start min and sec are greater than end min/sec so wrap around
    if start[1]> end[1]:
        mins = np.arange(start[1], 60 + end[1]+1)%60
    else:
        mins = np.arange(start[1], end[1]+1)
    if start[2]> end[2]:
        secs = np.arange(start[2], 60 + end[2]+1)%60
    else:
        secs = np.arange(start[2], end[2]+1)
    for a in range(start[0], end[0]+1): # + 1 to account for cases when user does not change degree/mins
        for b in mins:
            for c in secs:
                for d in range(partition):
                    aa=[]
                    for nn in tree_after[str(a)][str(b)][str(c)][str(d)]:
                        aa.append(nn[0])
                    dq.append(set(aa))
    com=[]
    com1=[]
    com2=[]
    com3=[]
    s1=[]
    s2=[]
    for i in range(start_degree, end_degree):
        #print(i)
        for j in range(0,minute):
            for k in range(0,seconds):
                for l in range(partition):
                    aa=[]
                    loc=[]
                    temp=[]
                    for nn in tree_before[str(a)][str(b)][str(c)][str(d)]:
                        aa.append(nn[0])
                        loc.append(nn)
                    com1=loc.copy()
                    pairwhichAreLessThan5mt=findp(com,com1)
                    com=com1.copy()
                    s1+=temp
                    temp=[]
                    loc=[]
                    for m in tree_after[str(i)][str(j)][str(k)][str(l)]:
                        temp.append(m[0])
                        loc.append(m)
                    com3=loc.copy()
                    pairwhichAreLessThan5mt_1=findp(com2,com3)
                    com2=com3.copy()
                    
                    s2+=temp
                    set1 = set(aa)
                    target_coord = (i,j,k,l)
#                   put last GPS in queue
                    a,b,c,d      = addsec(target_coord, avgdist)
                    aa=[]
                    for nn in tree_after[str(a)][str(b)][str(c)][str(d)]:
                        aa.append(nn[0])
                    
                    dq.append(set(aa))

#                   perform intersection
                    for set2 in list(dq):
                          common = (set1.intersection(set2))
                          if len(common) >1 : # not considering singleton set
                              contact_points.append(common)
                    dq.popleft() # remove set at the left
    con1=set(s1).intersection(set(s2))                    
    return contact_points,con1

# %%
"""
For pedstrains we add/subtarct seconds
"""
def addsec(t,s):
    sec = t[2]+s
    if sec >= 60:
        sec = sec-60
        mins = t[1] +1
        if mins >= 60:
            mins = mins - 60
            degree = t[0]+1 # we don't care latitude exceeding 90 for India since India is between 8 and 37 degree lat
        else:
            degree = t[0]
    else:
        mins = t[1]
        degree = t[0]
    return (degree, mins, sec, t[3])      

def subsec(t,s):
    sec = t[2]-s
    if sec < 0:
        sec = sec + 60
        mins = t[1] -1
        if mins <0 :
            mins = mins + 60
            degree = t[0]-1 # we don't care latitude exceeding 90 for India since India is between 8 and 37 degree lat
        else:
            degree = t[0]
    else:
        mins = t[1]
        degree = t[0]
    return (degree, mins, sec,t[3]) 

"""
For car, we add/subtract mins

"""
def addmin(t,s):
    mins = t[1] + s
    if mins >= 60:
        mins = mins - 60
        degree = t[0]+1 # we don't care latitude exceeding 90 for India since India is between 8 and 37 degree lat
    else:
        degree = t[0]
    return (degree, mins)      

def submin(t,s):
    mins = t[1] - s
    if mins < 0:
        mins = mins + 60
        degree = t[0]-1 # we don't care latitude exceeding 90 for India since India is between 8 and 37 degree lat
    else:
        degree = t[0]
    return (degree, mins)     

# %%
# t= (10, 0, 0,0.5103625041214924)   
# # data.iloc[1,0] = (10, 0, 0.540325041214924)  
# # data.iloc[0,2] = (10, 0, 10.7803625041214924)   
# # data.iloc[1,2] = (10, 0, 10.740325041214924)  

# s=14
# degree, mins, sec, frac = subsec(t,s)
# #print((degree, mins, sec, frac))
# degree, mins, sec, frac = addsec(t,s)
# #print((degree, mins, sec, frac))

# %%
"""
# Degree decimal to degree, minute, second and vice versa conversion. Note:
#  We only handle case for India
"""

# %%
def dd2dms(decdegrees):
    degrees = int(decdegrees)
    temp = 60 * (decdegrees - degrees)
    minutes = int(temp)
    seconds = 60 * (temp - minutes)
    return ((degrees, minutes, seconds))

def dms2dd(lat):
#     deg, minutes, seconds, direction =  re.split('[°\'"]', lat)
    deg, minutes, seconds =  lat
    return (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) 
    
