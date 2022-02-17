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
    def __init__(self, startNode, endNode):
        self.startNode = startNode
        self.endNode = endNode


# GRAPH CLASS
class Graph:
    def __init__(self, nbNodes, nbLinks, links, nodes):
        self.nbNodes = nbNodes
        self.nbLinks = nbLinks
        self.links = links
        self.nodes = nodes

    # method that returns the adjacency matrix from a given graph
    def adjMatrix(self):
        x = [[0 for i in range(self.nbNodes)] for j in range(self.nbNodes)]
        for i in range(self.nbLinks):
            x[self.links[i].startNode][self.links[i].endNode] = 1
            x[self.links[i].endNode][self.links[i].startNode] = 1
        return x

    def directedMatrix(self):
        x = [[0 for i in range(self.nbNodes)] for j in range(self.nbNodes)]
        for i in range(self.nbLinks):
            x[self.links[i].startNode][self.links[i].endNode] = 1
        return x

    # method to display the adjacency matrix
    def showAdjMatrix(self):
        matrix = self.adjMatrix()
        print("Adjacency matrix: \n[")
        for i in range(self.nbNodes):
            print(matrix[i])
        print("]")

    # method to display the directed matrix
    def showDirectedMatrix(self):
        matrix = self.directedMatrix()
        print("Directed matrix: \n[")
        for i in range(self.nbNodes):
            print(matrix[i])
        print("]")

    # method to get the transitive closure of a graph as a matrix
    def transitiveClosure(self):
        directedMatrix = self.directedMatrix()
        for k in range(self.nbNodes):
            for i in range(self.nbNodes):
                for j in range(self.nbNodes):
                    directedMatrix[i][j] = directedMatrix[i][j] or (
                        directedMatrix[i][k] and directedMatrix[k][j])
        for l in range(self.nbNodes):
            for m in range(self.nbNodes):
                if(l == m):
                    directedMatrix[l][m] = 1  # a node can reach itself
        return directedMatrix

    # method to display the transitive closure of a graph
    def showTransitiveClosure(self):
        matrix = self.transitiveClosure()
        print("Transitive closure: \n[")
        for i in range(self.nbNodes):
            print(matrix[i])
        print("]")

    # method to display strongly connected components in a graph
    def stronglyConnected(self):
        matrix = self.transitiveClosure()
        # we create a rotated matrix (lines = columns) to simplify comparing the sublists
        rotatedMatrix = []

        for i in range(self.nbNodes):
            columnJ = [matrix[j][i] for j in range(self.nbNodes)]
            rotatedMatrix.append(columnJ)

        stronglyConnectedComponents = {}  # create a dictionary
        for i in range(self.nbNodes):
            stronglyConnectedComponents.setdefault(tuple(rotatedMatrix[i]), list()).append(
                i)  # append the node if the colum is the same (in this case the row)

        print("Strongly connected components:")
        for value in stronglyConnectedComponents.values():
            print(value, " ", end='')


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
                    N = Node(stringNodeNumber)
                    nodes.append(N)
                lineNumber += 1
            else:
                startEndLink = line.split()
                L = Link(convert(startEndLink[0]), convert(startEndLink[1]))
                nbLinks += 1
                links.append(L)

    return nbNodes, nbLinks, links, nodes


# method that converts "text" to an int (removes "")
def convert(text):
    try:
        return int(text)
    except ValueError:
        return text


# main method
def main():
    print("Strongly connected components:")
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

    g.showDirectedMatrix()
    g.showTransitiveClosure()
    g.stronglyConnected()


# MAIN METHOD
if __name__ == '__main__':
    main()