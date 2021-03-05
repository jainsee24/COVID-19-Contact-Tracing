# %%
"""
# clustering of GPS coordinates via  M-way tree
"""

# %%
import numpy as np, pandas as pd
import json
import time
import bisect
from util import *

# %%
# # Show part of the data
# data = pd.read_csv("data/usergps.csv", delimiter="\t", header=None)
# data = data.iloc[:,:4]

# %%
# #print(data.head())

# %%
# # data = data.iloc[:1000,:]
# # #print(data.shape)
# """
# Convert degree decimal (DD) to degree, minute, and second format (DMS) 
# """

# data=data.applymap(dd2dms)
# #print(data.head())

# %%
# #print(data.shape)

# %%
"""
# Create multilevel hash map
"""

# %%
"""
# We want to build a tree like below
![caption](tree.jpg)
"""

# %%
contact_dist = 5

# %%
"""
# Create trees
"""

# lattree = CreateGPSTree('lat',contact_dist)

# with open("data/lat_tree_before.json","w") as fid:
#     fid.write(json.dumps(lattree, indent=5))
# with open("data/lat_tree_after.json","w") as fid:
#     fid.write(json.dumps(lattree, indent=5)) 
    
# longtree = CreateGPSTree('long',contact_dist)
# with open("data/long_tree_before.json","w") as fid:
#     fid.write(json.dumps(longtree, indent=5))
# with open("data/long_tree_after.json","w") as fid:
#     fid.write(json.dumps(longtree, indent=5))
    

# %%
# # #  delete the tresss for after use in offline mode.
# del lattree
# del longtree

# %%
"""
# Data for Testing Static case
"""
s=[20,200,2000,20000,200000,2000000,4000000,6000000,8000000,10000000]
for samples in s:
# Generate some fake data
    end=59
    #end=2
    degree = np.random.randint(7,39, samples)
    minutes = np.random.randint(0,end, samples)
    col1 = np.random.rand(samples)
    col2 = np.random.uniform(0,end, samples)
    lat1 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    # degree = np.random.randint(7,39, samples)
    # minutes = np.random.randint(0,end, samples)
    col1 = np.random.rand(samples)
    col2 = np.random.uniform(0,end, samples)
    lat2 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    degree = np.random.randint(66,99, samples)
    minutes = np.random.randint(0,end, samples)
    col1 = np.random.rand(samples)
    col2 = np.random.uniform(0,end, samples)
    long1 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    # degree = np.random.randint(66,99, samples)
    # minutes = np.random.randint(0,end, samples)
    col1 = np.random.rand(samples)
    col2 = np.random.uniform(0,end, samples)
    long2 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    data=pd.concat([lat1, long1, lat2, long2], axis=1)
    #print(data.head())
    
    # %%
    rows =  np.arange(0,samples)
    degree = np.random.randint(7,39, samples)
    minutes = np.random.randint(0,end, samples)
    col1 = np.random.rand(samples)
    col2 = np.random.uniform(0,end, samples)
    lat1 = pd.DataFrame({"0":[(r,d,m,s+f) for r,d, m, s, f in zip(rows,degree, minutes,col1, col2)]})
    
    #print(lat1.head())
    lat1.to_csv(r'pyafter.txt', header=False, index=False)
    
    # %%
    # d=pd.read_csv('pybefore.csv',header=None)
    # #print(d.head())
    
    # %%
    """
    # Data for testing dynamic case
    """
    
    # %%
    # Generate some fake data
    # samples = 200
    # degree = np.random.randint(7,39, samples)
    # minutes = np.random.randint(0,end, samples)
    # col1 = np.random.rand(samples)
    # col2 = np.random.uniform(0,end, samples)
    # lat1 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    # # degree = np.random.randint(7,39, samples)
    # # minutes = np.random.randint(0,end, samples)
    # col1 = np.random.rand(samples)
    # # col2 = np.random.uniform(0,end, samples)
    # lat2 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    # degree = np.random.randint(66,99, samples)
    # minutes = np.random.randint(0,end, samples)
    # col1 = np.random.rand(samples)
    # col2 = np.random.uniform(0,end, samples)
    # long1 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    # # degree = np.random.randint(66,99, samples)
    # # minutes = np.random.randint(0,end, samples)
    # col1 = np.random.rand(samples)
    # # col2 = np.random.uniform(0,end, samples)
    # long2 = pd.DataFrame({"0":[(d,m,s+f) for d, m, s, f in zip(degree, minutes,col1, col2)]})
    # data=pd.concat([lat1, long1, lat2, long2], axis=1)
    # #print(data.head())
    
    # %%
    # #  sample Data for testing static/dynamic case
    # data = pd.read_csv("data/sample.csv")
    # data  = data.iloc[:,1:5]
    # data = data.applymap(eval)
    # #print(data)
    
    
    # %%
    # list(enumerate(data.iloc[:,0]))
    
    # %%
    # Load tress
    
    with open("data/lat_tree_before.json","r") as fid:
        lat_tree_before = json.load(fid)
    with open("data/lat_tree_after.json","r") as fid:
        lat_tree_after = json.load(fid)
        
    with open("data/long_tree_before.json","r") as fid:
        long_tree_before = json.load(fid)
    with open("data/long_tree_after.json","r") as fid:
        long_tree_after = json.load(fid)
    
    # %%
    """
    
    # -------------------------------------- Static Case------------------------------------------------------------
    """
    
    # %%
    # # #  map data to trees
    #print('lat_tree_before')
# =============================================================================
#     start = time.perf_counter()
#     #print(data.iloc[:,0])
#     #print(data.iloc[:,2])
#     MapGPS(lat_tree_before, data.iloc[:,0], contact_dist)
#     end = time.perf_counter()
#     #print("Map GPS: Elapsed time: ", end-start)
#     start = time.perf_counter()
#     #MapGPS(lat_tree_after, data.iloc[:,2], contact_dist)
#     end = time.perf_counter()
#     #print("2nd MAP GPS Elapsed time: ", end-start)
#     
#     #  Intersect trees
#     
# # =============================================================================
# #     start = time.perf_counter()
# #     contact_list,endcase = IntersectGPSTree(lat_tree_before, lat_tree_after, 'lat', contact_dist)
# #     end = time.perf_counter()
# #     #print(contact_list)
# #     #print("IntersectGPSTree : Elapsed time: ", end-start)
# #     
# #     
# # =============================================================================
#     #  map data to trees
#     #print('long_tree_before')
#     start = time.perf_counter()
#     MapGPS(long_tree_before, data.iloc[:,1], contact_dist)
#     end = time.perf_counter()
#     #print("MapGPS: Elapsed time: ", end-start)
#     start = time.perf_counter()
#     MapGPS(long_tree_after, data.iloc[:,3], contact_dist)
#     end = time.perf_counter()
# =============================================================================
    #print("MapGPS 2: Elapsed time: ", end-start)
    
    #  Intersect trees
# =============================================================================
#     
#     start = time.perf_counter()
#     contact_list1,endcase1 = IntersectGPSTree(long_tree_before, long_tree_after, 'long', contact_dist)
#     end = time.perf_counter()
#     #print(contact_list1)
#     #print("IntersectGPSTree: Elapsed time: ", end-start)
#     
#     a=[]
#     start = time.perf_counter()
#     for i in contact_list:
#     	for j in range(0,len(i)):
#     		for k in range(j+1,len(i)):
#     			i=list(i)
#     			a.append((min(i[j],i[k]),max(i[j],i[k])))
#     for i in endcase:
#     	i=list(i)
#     	for j in i:
#     		a.append((min(j[0],j[1]),max(j[0],j[1])))
#     #print(a)
#     a=set(a)
#     
#     b=[]
#     for i in contact_list1:
#     	for j in range(0,len(i)):
#     		for k in range(j+1,len(i)):
#     			i=list(i)
#     			b.append((min(i[j],i[k]),max(i[j],i[k])))
#     for i in endcase1:
#     	i=list(i)
#     	for j in i:
#     		b.append((min(j[0],j[1]),max(j[0],j[1])))
#     b=set(b)
#     #print(a)
#     #print(a.intersection(b))
#     end = time.perf_counter()
#     #print(contact_list1)
#     #print("Final Intersect(STATICCASE): Elapsed time: ", end-start)
#     ##print("Possible Hotspot: ",hotspot(lat_tree_before,long_tree_before,5,a.intersection(b)))
# =============================================================================
    covid19pos=[0]*samples#ids of covid patient
    Suspected=[0]*samples
    import time
    a=time.time()
    longh=(81, 26, 33.00675601725927)
    lath=(35, 29, 9.72002468329106)
    x=hotspotpeople(lath,longh,lat_tree_after,long_tree_after)
    #print(x)
    y=realhotspotpeople(lath,longh,data.iloc[:,1], data.iloc[:,3],x)
    #print(y)
    print(time.time()-a)
    #deftomap(x,data.iloc[:,1], data.iloc[:,3],covid19pos,Suspected)
    
    
    # %%
    # contact_list
    
    # %%
    """
    # -------------------------------------- Dynamic Case------------------------------------------------------------
    """
    # =============================================================================
    # 
    # # %%
    # #  map data to trees
    # start = time.perf_counter()
    # MapGPS(lat_tree_before, data.iloc[:,0], contact_dist)
    # end = time.perf_counter()
    # #print("Lat Elapsed time for mapping to tree: ", end-start)
    # start = time.perf_counter()
    # MapGPS(lat_tree_after, data.iloc[:,2], contact_dist)
    # end = time.perf_counter()
    # #print("Lat Elapsed time for mapping to tree: ", end-start)
    # 
    # #  Intersect trees
    # 
    # start = time.perf_counter()
    # contact_list1 ,endcase1= FastPedestrianIntersectGPSTree(lat_tree_before, lat_tree_after, 'lat', contact_dist)
    # end = time.perf_counter()
    # #print("Lat Elapsed time for Intersection: ", end-start)
    # 
    # ##LONG....
    # 
    # start = time.perf_counter()
    # MapGPS(long_tree_before, data.iloc[:,0], contact_dist)
    # end = time.perf_counter()
    # #print("Long Elapsed time for mapping to tree: ", end-start)
    # start = time.perf_counter()
    # MapGPS(long_tree_after, data.iloc[:,2], contact_dist)
    # end = time.perf_counter()
    # #print("Long Elapsed time for mapping to tree: ", end-start)
    # 
    # #  Intersect trees
    # 
    # start = time.perf_counter()
    # contact_list2,endcase2 = FastPedestrianIntersectGPSTree(long_tree_before, long_tree_after, 'long', contact_dist)
    # end = time.perf_counter()
    # #print("Long Elapsed time for Intersection: ", end-start)
    # 
    # 
    # a=[]
    # start = time.perf_counter()
    # for i in contact_list1:
    # 	for j in range(0,len(i)):
    # 		for k in range(j+1,len(i)):
    # 			i=list(i)
    # 			a.append((min(i[j],i[k]),max(i[j],i[k])))
    # for i in endcase1:
    # 	i=list(i)
    # 	for j in i:
    # 		a.append((min(j[0],j[1]),max(j[0],j[1])))
    # a=set(a)
    # 
    # b=[]
    # for i in contact_list2:
    # 	for j in range(0,len(i)):
    # 		for k in range(j+1,len(i)):
    # 			i=list(i)
    # 			b.append((min(i[j],i[k]),max(i[j],i[k])))
    # for i in endcase2:
    # 	i=list(i)
    # 	for j in i:
    # 		b.append((min(j[0],j[1]),max(j[0],j[1])))
    # b=set(b)
    # # #print(a)
    # # #print(b)
    # #print(a.intersection(b))
    # end = time.perf_counter()
    # #print(contact_list1)
    # #print("Final Intersect(DYNAMICCASE): Elapsed time: ", end-start)
    # =============================================================================
    
    
    # # %%
    # contact_list[0]
    
    # %%
    """
    # Parallel Implementation of the mapping
    """
    
    # %%
    
    # data=[1,2,3,1,3,1]
    # # sharedtree= manager.dict({"1":manager.list(),"2":manager.list(),"3":manager.list()})
    # sharedtree = manager.dict({"1":[],"2":[],"3":[]})
    # with Pool(processes=3) as pool:
    #     pool.map(partial(mapTo, tree=sharedtree), list(enumerate(data,start=1)))
        
    
    # %%
    # def mapTo(i_d,tree):
    #     idx,item = i_d
    #     l = tree[str(item)]
    #     l.append(idx)
    #     tree[str(item)] = l
        
    
           
    
    # %%
    # from functools import partial
    # from multiprocessing import Pool, Manager
    # manager = Manager()
    # lat_shared_before = manager.dict(lat_tree_before)
    
    # start = time.perf_counter()
    # with Pool(processes=8) as pool:
    #     pool.map(partial(MapGPSInParallel, tree=lat_shared_before, contact_dist=contact_dist),list(enumerate(data.iloc[:,0])))
    
    # # MapGPS(lat_tree_before, data.iloc[:,0], contact_dist)
    
    # end = time.perf_counter()
    # #print("Elapsed time: ", end-start)
    
    # %%
    # from objsize import get_deep_size
    # #print(get_deep_size(tree))
    # #print(get_deep_size(gps_tree))