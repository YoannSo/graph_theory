# AUTHORS: Matt TAYLOR / Yoann SOCHAJ
# DATE: 18/05/21
# SUBJECT: Theorie des Graphes - L3 [S6] - Projet

from pathlib import Path  # to make sure the file containing the graph exists

# NODE CLASS


class Node:
    def __init__(self, name):
        self.name = name


# LINK CLASS
class Link:
    def __init__(self, startNode, endNode, weight):
        self.startNode = startNode
        self.endNode = endNode
        self.weight = weight


# GRAPH CLASS
class Graph:
    def __init__(self, nbNodes, nbLinks, links, nodes):
        self.nbNodes = nbNodes
        self.nbLinks = nbLinks
        self.links = links
        self.nodes = nodes

    # method that returns the adjacency matrix from a given graph
    def adjMatrixWeight(self):
        x = [[0 for i in range(self.nbNodes)] for j in range(self.nbNodes)]
        for i in range(self.nbLinks):
            x[self.links[i].startNode][self.links[i].endNode] = self.links[i].weight
            x[self.links[i].endNode][self.links[i].startNode] = self.links[i].weight
        return x

    # method to display the adjacency matrix with the weights
    def showAdjMatrixWeight(self):
        matrix = self.adjMatrixWeight()
        print("Adjacency matrix with weights: \n[")
        for i in range(self.nbNodes):
            print(matrix[i])
        print("]")

    # method to print nice path (0  1  2  3)
    def showPath(self, path, index):
        if(path[index] == -1):
            print(index, " ", end='')
            return

        self.showPath(path, path[index])
        print(index, " ", end='')

    # method that implements the Dijkstra algorithm and returns the distance from the startNode to every other node and the paths
    def Dijkstra(self, startNode, endNode):
        adjMatrixWeight = self.adjMatrixWeight()
        inf = 99999  # "infinity"
        # fill the distance with infinity apart from the source (startNode)
        distance = [
            0 if i == startNode.name else inf for i in range(self.nbNodes)]
        # fill the smallestTree with False's
        smallestTree = [False for i in range(self.nbNodes)]
        path = [-1 for i in range(self.nbNodes)]  # fill the path with -1's

        for i in range(self.nbNodes):
            minDist = 99999
            for j in range(self.nbNodes):
                # if the distance is smaller
                if(distance[j] < minDist and smallestTree[j] == False):
                    minDist = distance[j]  # update the minimum distance
                    minIndex = j  # the index of the minimum distance

            # set that index to True (node has been visited)
            smallestTree[minIndex] = True

            for k in range(self.nbNodes):
                # all these conditions have to be met to continue:
                if((adjMatrixWeight[minIndex][k] > 0) and (smallestTree[k] == False) and (distance[k] > distance[minIndex] + adjMatrixWeight[minIndex][k])):
                    # the 1st condition makes sure that there is a link between "minIndex" and "k"
                    # the 2nd condition makes sure that this tree has not already been set to True
                    # the 3rd condition compares the existing distance in our distance [] list and the sum of the other path; if the existing distance is bigger then we update it to the new path
                    # update our distance [] list as the sum of the weight of the path
                    distance[k] = distance[minIndex] + \
                        adjMatrixWeight[minIndex][k]
                    path[k] = minIndex

        return distance, path  # return the list of distances to every node and the path


# method to create graph from text file
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
                    N = Node(intNodeNumber)
                    nodes.append(N)
                lineNumber += 1
            else:
                startEndLink = line.split()
                L = Link(convert(startEndLink[0]), convert(
                    startEndLink[2]), convert(startEndLink[1]))
                nbLinks += 1
                links.append(L)

    # return the number of nodes, the number of links, the links and the nodes to create the Graph
    return nbNodes, nbLinks, links, nodes


# method that converts "text" to an int (removes "")
def convert(text):
    try:
        return int(text)
    except ValueError:
        return text


# main method
def main():
    print("Dijkstra:")
    while(1):
        try:
            # ask file name to user
            fileName = (input("Enter file name: (without .txt)\n"))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if (not Path(fileName+".txt").is_file()):  # make sure the file exists
            print("File does not exist.")
            continue
        else:
            break

    print("File read successfully: %s.txt" % fileName)

    nbNodes, nbLinks, links, nodes = readFile(fileName)
    print("Number of nodes:", nbNodes)
    print("Number of links:", nbLinks)

    g = Graph(nbNodes, nbLinks, links, nodes)
    g.showAdjMatrixWeight()

    while(1):
        try:
            # ask start node to user
            startNode = int(input("Enter the start node:\n"))
            # ask end node to user
            endNode = int(input("Enter the end node:\n"))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        break

    # apply the Dijkstra algorithm to the graph (specifying the starting and ending node)
    distance, path = g.Dijkstra(g.nodes[startNode], g.nodes[endNode])
    print("Shortest path from node", startNode, "to node %d:" % endNode)
    print("Cost:", distance[endNode])
    print("Path: ", end=''), g.showPath(path, endNode)


# MAIN METHOD
if __name__ == "__main__":
    main()
