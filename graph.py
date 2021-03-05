import networkx as nx 
import heapq


def dijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
    """ calculates a shortest path tree routed in src
    """    
    # a few sanity checks
    if src not in graph:
        return -1,-1
    if dest not in graph:
        return -1,-1    
    # ending condition
    if src == dest:
        # We build the shortest path and display it
        path=[]
        pred=dest
        while pred != None:
            path.append(pred)
            pred=predecessors.get(pred,None)
        # reverses the array, to display the path nicely
        readable=path[0]
        for index in range(1,len(path)): readable = path[index]+'--->'+readable
        #prints it 
        cost=str(distances[dest])
        print("path: "+readable+",   cost="+str(distances[dest]))   
        return path,cost
    else:    
        # if it is the initial  run, initializes the cost
        if not visited: 
            distances[src]=0
        # visit the neighbors
        for neighbor in graph[src] :
            if neighbor not in visited:
                new_distance = distances[src] + graph[src][neighbor]
                if new_distance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = src
        # mark as visited
        visited.append(src)
        # now that all neighbors have been visited: recurse                         
        # select the non visited node with lowest distance 'x'
        # run Dijskstra with src='x'
        unvisited={}
        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k,float('inf'))        
        x=min(unvisited, key=unvisited.get)
        path,cost=dijkstra(graph,x,dest,visited,distances,predecessors)
        return path,cost
import matplotlib.pyplot as plt 
file=open('cities.txt')
cities=[]
red=[]
net=[]
x=[]
graph={}
s=file.readline()
k=0
while s!='':
	y=s.replace('\n','')
	if y=='' and k==0:
		cities=x.copy()
		k=1
		x=[]
	elif y=='' and k==1:
		net=x.copy()
		k=2
		x=[]
	elif y=='' and k==2:
		red=x.copy()
		k=3
		x=[]
	else:
		x.append(y)
	s=file.readline()
print(cities)
print(red)
print(net)
city={}
for i in range(0,len(cities)):
	city[i]=cities[i]
g = nx.Graph() 
for i in net:
	xx=i.split(' ')
	a,b=xx[0].split('-')
	a,b=int(a),int(b)
	g.add_edge(city[a], city[b]) 
# drawing in circular layout 
nx.draw_circular(g, with_labels = True) 
plt.savefig("InitialGraph.png") 
plt.clf() 

g = nx.Graph() 
for i in net:
	xx=i.split(' ')
	a,b=xx[0].split('-')
	a,b=int(a),int(b)
	if not((city[a] in red) or (city[b] in red)):
		print(a,b)
		g.add_edge(city[a], city[b])
		a=str(a)
		b=str(b)
		if a in graph:
			graph[a][b]=int(xx[1])
		else:
			graph[a]={}
			graph[a][b]=int(xx[1]) 
		if b in graph:
			graph[b][a]=int(xx[1])
		else:
			graph[b]={}
			graph[b][a]=int(xx[1]) 
		
	else:
		if (city[a] in red):
			g.add_edge(city[a],city[a])
		if city[b] in red: 
			g.add_edge(city[b],city[b])
		
# drawing in circular layout 
nx.draw_circular(g, with_labels = True) 
plt.savefig("AfterHotGraph.png") 

# clearing the current plot 
plt.clf() 
print(graph)
path,cost=dijkstra(graph,'8','11')
path.reverse()
print(path,cost)


plt.clf() 

g = nx.Graph() 
for i in range(len(cities)):
	g.add_edge(city[i], city[i]) 
for  i in range(0,len(path)-1):
	g.add_edge(city[int(path[i])], city[int(path[i+1])]) 
nx.draw_circular(g, with_labels = True) 
plt.savefig("Route.png") 

# clearing the current plot 
plt.clf() 
