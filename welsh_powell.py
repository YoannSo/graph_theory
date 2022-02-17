# AUTHORS: Matt TAYLOR / Yoann SOCHAJ
# DATE: 18/05/21
# SUBJECT: Theorie des Graphes - L3 [S6] - Projet

import random #used to generate a random color
from pathlib import Path #to make sure the file containing the graph exists

#COLOR CLASS
class Color:
	def __init__(self, r, g, b, name):
		self.r = r
		self.g = g
		self.b = b
		self.name = name

	def randomColor(self):
		self.r = random.randint(100,255) #generate random int between 100 and 255 (both included)
		self.g = random.randint(100,255) #we chose between 100 and 255 so the colors are not too dark
		self.b = random.randint(100,255) #and you can see the node names (in black) on the .png file created


#NODE CLASS
class Node:
	def __init__(self, name, degree, color):
		self.name = name
		self.degree = degree
		self.color = color

	#returns 1 (True) if the current node is colored, 0 (False) otherwise
	def isColored(self):
		if(self.color.r !=0 or self.color.g != 0 or self.color.b != 0):
			return 1
		else:
			return 0

	#returns 1 (True) if the current node is adjacent to node 1, 0 (False) otherwise
	def isAdjacent(self, node1, matrix):
		if( (matrix[self.name][node1.name] == 1) ):
			return 1
		else:
			return 0

	#this method will allow us to sort the nodes according to their degree
	def __gt__(self, other): 
		return self.degree < other.degree


#LINK CLASS
class Link:
	def __init__(self, startNode, endNode):
		self.startNode = startNode
		self.endNode = endNode


#GRAPH CLASS
class Graph:
	def __init__(self, nbNodes, nbLinks, links, nodes):
		self.nbNodes = nbNodes
		self.nbLinks = nbLinks
		self.links = links
		self.nodes = nodes

	#method that returns the adjacency matrix from a given graph
	def adjMatrix(self):
		x = [ [0 for i in range (self.nbNodes)] for j in range (self.nbNodes)]
		for i in range (self.nbLinks):
			x[self.links[i].startNode][self.links[i].endNode] = 1
			x[self.links[i].endNode][self.links[i].startNode] = 1
		return x

	#method to display the adjacency matrix
	def showAdjMatrix(self):
		matrix = self.adjMatrix()
		print("Adjacency matrix: \n[")
		for i in range(self.nbNodes):
			print(matrix[i])
		print("]")

	#method to sort the nodes by their degree
	def sortDeg(self):
		matrix = self.adjMatrix()
		for i in range(self.nbNodes):
			self.nodes[i] = Node(i, 0, Color(0,0,0, "null"))
			for j in range(self.nbNodes):
				if(matrix[i][j] == 1):
					self.nodes[i].degree += 1
		self.nodes.sort() #sort the nodes from highest to lowest degree
		return self.nodes

	#method that implements the Welsh-Powell algorithm and returns a list of colored nodes and the chromatic number of the given graph
	def WelshPowell(self):
		chromaticNumber = 0
		sortedNodes = self.sortDeg() #get the nodes sorted by highest to lowest degree
		adjMatrix = self.adjMatrix() #get the adjacency matrix
		temp = []	#this temporary list will contain all the nodes that have been colored each "i" iteration
					#this allows us to make sure that the node we want to color is not adjacent to the current node "i" or any nodes in temp[] list
		
		for i in range(self.nbNodes):
			if (i != 0): 
				temp.clear() #the list gets cleared every iteration apart from i = 0
			if(sortedNodes[i].isColored() == 0): #if the node is not colored
				c = Color(0,0,0,"null") #create a color
				c.randomColor() #randomise the color
				sortedNodes[i].color = c #apply the color to the node
				chromaticNumber +=1 #increase the chromatic number
			
				for j in range(self.nbNodes):
					tempCounter = 0 #this counter makes sure we check the adjacency of all the nodes in the temp[] list
					if( (sortedNodes[i].isAdjacent(sortedNodes[j], adjMatrix) == 0) and (sortedNodes[j].isColored() == 0) ):
						if(len(temp) != 0): #if temp[] is not null
							for k in range(len(temp)):
								if(sortedNodes[j].isAdjacent(temp[k], adjMatrix) == 0): #if the temp[k] node is not adjacent to current "j" node increment the counter
									tempCounter +=1
									if(tempCounter == len(temp)): #if the counter has been incremented enough then it is not adjacent to any nodes in temp[]
										if(sortedNodes[j] not in temp): #if the nodes is not already in temp[]
											temp.append(sortedNodes[j]) #add it to temp[]
										sortedNodes[j].color = c #apply the color
						else: #if temp[] is null
							temp.append(sortedNodes[j]) #add it to temp[] directly
							sortedNodes[j].color = c #apply the color
					
		self.nodes = sortedNodes #give the current nodes of the graph the sortedNodes[] list with the correct colors
		return self.nodes, chromaticNumber #return the list of colored nodes and the chromatic number

#method to create graph from text file					
def readFile(filePath):
	nbNodes = 0
	nbLinks = 0
	links = []
	nodes = []
	lineNumber = 0
	with open(filePath+".txt", 'r') as f:
		for line in f:
			if(lineNumber == 0):
				firstLineSplit = line.split()
				nbNodes = len(firstLineSplit)
				for stringNodeNumber in firstLineSplit:
					intNodeNumber = convert(stringNodeNumber)
					N = Node(stringNodeNumber, 0, Color(0,0,0,"null"))
					nodes.append(N)
				lineNumber +=1
			else:
				startEndLink = line.split()
				L = Link(convert(startEndLink[0]), convert(startEndLink[1]))
				nbLinks +=1
				links.append(L)

	return nbNodes, nbLinks, links, nodes #return the number of nodes, the number of links, the links and the nodes to create the Graph

#method that converts "text" to an int (removes "")
def convert(text):
	try:
		return int(text)
	except ValueError:
		return text
	
#main method
def main():
	print("Welsh-Powell:")
	while(1):
		try:
			fileName = (input("Enter file name: (without .txt)\n")) #ask file name to user
		except ValueError:
			print("Sorry, I didn't understand that.")
			continue
		if (not Path(fileName+".txt").is_file()): #make sure the file exists
			print("File does not exist.")
			continue
		else:
			break

	print("File read succesfully: %s.txt" %fileName)

	nbNodes, nbLinks, links, nodes = readFile(fileName)
	print("Number of nodes:", nbNodes)
	print("Number of links:", nbLinks)

	g = Graph(nbNodes, nbLinks, links, nodes) #create the graph with all the file information
	#g.showAdjMatrix() #show the adjacency matrix
	coloredNodes, chromaticNumber = g.WelshPowell() #apply the Welsh-Powell algorithm to the graph
	
	for i in range (len(g.nodes)): #for each node in the graph show its name and its color
		print("Node:", coloredNodes[i].name, "Color:", coloredNodes[i].color.r, coloredNodes[i].color.g, coloredNodes[i].color.b)

	print("The chromatic number of this graph is:", chromaticNumber)


	#VISUAL REPRESENTATION OF GRAPH (uncomment if you have pydot installed on your machine)
	#***************** 

	# import pydot
	# graph = pydot.Dot(graph_type="graph")
	# for i in range (len(g.nodes)):
	# 	color = str(g.nodes[i].color.r/255) + " " +  str(g.nodes[i].color.g/255) + " " +  str(g.nodes[i].color.b/255)
	# 	node = pydot.Node(g.nodes[i].name, style="filled", fillcolor=color)
	# 	graph.add_node(node)
	# for i in range(len(g.links)):
	# 	arc = pydot.Edge(g.links[i].startNode, g.links[i].endNode)
	# 	graph.add_edge(arc)
	# #print(graph)
	# graph.write_png("%s.png"%fileName)
	# print("%s.png"%fileName , "created.")

	# ***************


#MAIN METHOD
if __name__ == "__main__":
	main()