import numpy
import string
import random

def build_graph(filename): 
	#build_graph initalizes the edges and nodes of a fully-connected
	#graph based on the input file
	
	#open the file where data is stored
	f = open(filename,'r')
	
	#count how many participants we have
	nPeople = sum(1 for line in f)

	#initalize the nodes of our graph
	nodes = numpy.zeros(nPeople, dtype = [('Name','a10'),
		('Number','a10'),('GroupNo',int),('BuyGiftFor',int)])

	#fill in the data from our text file
	f.seek(0,0)
	i = 0
	for curLine in f:
		nodes[i]['Name'] = string.split(curLine)[0]
		nodes[i]['Number'] = string.split(curLine)[1]
		nodes[i]['GroupNo'] = int(string.split(curLine)[2])
		i += 1
	#we start with every node connected to every other node, 
	#including self-connections
	edges = numpy.ones((nPeople,nPeople), dtype = numpy.int)

	return nodes, edges

def exclude_edges(groupIDs,edges):
	#removes edges from the graph based on group ID.  Any two nodes with
	#the same group ID will not be connected.
	
	#find all unique groups
	groups = set(groupIDs)
	
	#for each group, remove the edges between them
	for g in groups:
		ingroup = (groupIDs == g)
		sz = sum(ingroup)
		edges[numpy.ix_(ingroup,ingroup)] = numpy.zeros((sz,sz),dtype=int)

	return edges

def find_matches(edges):
	# finds a hamiltonian path from the given graph (a path
	# that visits every node in the graph exactly once). 
	# This function essentially works by trial and error,
	# since there is no closed-form way (except brute force)
	# to solve this problem.  Hamiltonian paths are the preferred
	# solution to the secret santa problem, since you can ensure
	# that there are no weird side groups (e.g. A gives a gift to 
	# B and B gives a gift to A).  However, THIS FUNCTION DOES NOT
	# CHECK TO MAKE SURE THAT A HAMILTONIAN PATH EVEN EXISTS IN
	# THE INPUT GRAPH AND WILL RUN FOREVER IF THAT IS NOT THE CASE


	# we will need to try several times before succeeding
	# in generating a hamiltonian path, so it is best to
	# make a copy of the original graph with the exclusions
	E = numpy.copy(edges)
	n = numpy.shape(E)[0]

	# if the trace of the graph is 2*n, that means this function
	# has found a path by visiting every node exactly once, so 
	# we can stop
	# the sum condition is just a check to make sure that every
	# node has two edges, because sometimes this method finds a
	# path that hits every node only once but make a full loop
	while (numpy.trace(E) != 2*n) or (sum(sum(E)) != 4*n):
	
		E = numpy.copy(edges)
		# pick a random start node
		child = random.randint(0,n-1)
		# find all nodes connected to our start node, and
		# shuffle them
		poss = numpy.arange(n)[E[child] == 1]
		numpy.random.shuffle(poss)
		# delete all connections except two
		E[child,poss[2:len(poss)]] = 0
		E[:,child] = E[child]
		# set the diagonal value to 2, to indicate that we have
		# visited this node once
		E[child,child] = 2
		
		# move randomly to one of the two connections left,
		# but keep track of the previous node (because we need
		# to preserve that connection)
		parent = child
		child = poss[0]

		# this loop continues until we reach a node we have already
		# visited
		while E[child,child] != 2:
			# find all nodes connected to our node
			poss = numpy.arange(n)[E[child]==1]
			# if there are fewer than two connections,
			# something has gone horribly wrong 
			if sum(poss) <= 2:
				break
			# preserve the connection to the previous node 
			poss = poss[poss != parent]
			# shuffle the rest
			numpy.random.shuffle(poss)
			# delete all connections but one
			E[child,poss[1:len(poss)]] = 0
			E[:,child] = E[child]
			# mark this node as having been visited
			E[child,child] = 2
			# traverse to the next node, if possible
			parent = child
			if len(poss) == 0:
				break
			child = poss[0]
	return E

def assign_matches(nodes,edges):
	# once a hamiltonian path through the graph has been found
	# this function will update the nodes with a pointer to their
	# secret santa match

	# start with the first node
	parent = 0
	n =  numpy.shape(edges)[0]
	poss = numpy.arange(n)[edges[parent]==1]
	numpy.random.shuffle(poss)
	# randomly pick a direction to traverse the hamiltonian path
	child = poss[0]
	# assign match
	nodes[parent]['BuyGiftFor'] = child

	# traverse the path until we end up back at start
	while child !=0: 
		poss = numpy.arange(n)[edges[child]==1]
		poss = poss[poss != parent]
		nodes[child]['BuyGiftFor'] = poss[0]
		parent = child
		child = poss[0]
	return nodes

def print_matches(nodes):
	# just a stupid small program to print all the matches on the screen
	# mostly as an example of how the node structure works

	for i in range(len(nodes)):
		print nodes[i]['Name'] + ' has ' + nodes[nodes[i]['BuyGiftFor']]['Name']