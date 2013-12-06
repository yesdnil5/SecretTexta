#you'll need to change the path, but you can run an example using this code

import numpy
import os
import string

os.chdir('C:\Britni\Code\secretsanta')
import secretsanta

filename = 'inputdata.txt'
nodes,edges = secretsanta.build_graph(filename)
edges = secretsanta.exclude_edges(nodes['GroupNo'],edges)
edges = secretsanta.find_matches(edges)
nodes = secretsanta.assign_matches(nodes,edges)
secretsanta.print_matches(nodes)

# just a simple example to show you how recarrays work.
for i in range(len(nodes))
	print nodes[i]['Name'] + ' has ' + nodes[nodes[i]['BuyGiftFor']]['Name']

TODO:
- alternatively, create a class Node and do it object-oriented for real

