infinity = 1000000
invalid_node = -1

class Node:
        previous = invalid_node
        distFromSource = infinity
        visited = False

def populateNetwork(fileName):
    #reads in a fileName to store in network array
    #network array to store arrays for each line of values
    #reads through fileName (networkFile) one line at a time
    #splits each line in networkFile to seperate strings based on the ',' in file and strips whitespace from the end of each string
    #converts each seperated string to int and appends values to network array
    network = []
    networkFile = open(fileName, "r")
    for line in networkFile:
        network.append(map(int, line.strip('\r\n').split(',')))
    return network

def populateNodeTable(network, startNode):
    nodeTable = []
    for line in network:
        nodeTable.append(Node())
    nodeTable[startNode].distFromSource = 0
    nodeTable[startNode].visited = True
    return nodeTable

def returnNearNeighbours(network, nodeTable, currentNode):
    #find the unvisited neighbours of the current node
    #returns a list of nodes matching these criteria
    nearNeighbours = []
    for node, value in enumerate(network[currentNode]):
        if value != 0 and nodeTable[node].visited==False:
            nearNeighbours.append(node)

    return nearNeighbours

def calculateTentative(network, nodeTable, currentNode):
    #calculate tentative distances for nearest neighbours
    #overwrite existing values if tentative is lower
    NN = returnNearNeighbours(network, nodeTable, currentNode)
    for nodeIndex in NN:
        tentativeDist = nodeTable[currentNode].distFromSource + network[currentNode][nodeIndex]
        if tentativeDist < nodeTable[nodeIndex].distFromSource:
            nodeTable[nodeIndex].distFromSource = tentativeDist
            nodeTable[nodeIndex].previous = currentNode

def returnNextNode(nodeTable):
    shortDistFromSrc = infinity
    currentNode = invalid_node
    for nodeIndex, node in enumerate(nodeTable):
        if node.distFromSource < shortDistFromSrc and node.visited == False:
            currentNode = nodeIndex
            shortDistFromSrc = node.distFromSource
    return currentNode

    #1) Create a function called 'calculateShortestPath',
    #which works out the complete path from source to sink
    #and calculating total distance
def calculateShortestPath(network, startNode, currentNode, endNode):
    path = []
    nodeTable = populateNodeTable(network, startNode)
    
    while currentNode != endNode:
        calculateTentative(network, nodeTable, currentNode)
        tempNode = returnNextNode(nodeTable)
        
        if tempNode == currentNode:
            return path, nodeTable
        else:
            currentNode = tempNode
            
        nodeTable[currentNode].visited = True
        
    path.append(endNode)
    
    while currentNode != startNode:
        path.insert(0, nodeTable[currentNode].previous)
        currentNode = path[0]
    
    return path, nodeTable

def maxFlow(path, network, startNode, currentNode, endNode):
    maxFlow = 0
    
    while path != []:
        capacity = findCapacity(path, network, currentNode, endNode)
        print "Path Found:", [chr(x + 65) for x in path], "Bottleneck:", capacity
        maxFlow += capacity
        network = adjustPath(path, capacity, network)
        path, nodeTable = calculateShortestPath(network, startNode, currentNode, endNode)

    return maxFlow

def findCapacity(path, network, currentNode, endNode):
    length = len(path)
    capacity = infinity
    
    for nodeIndex, value in enumerate(path):
        if nodeIndex < (length-1):
            if network[value][path[nodeIndex + 1]] < capacity:
                capacity = network[value][path[nodeIndex + 1]]
    return capacity #bottleneck found


def adjustPath(path, capacity, network):
    length = len(path)

    for nodeIndex, value in enumerate(path):
        if nodeIndex < (length-1):
            network[value][path[nodeIndex + 1]] -= capacity
            network[path[nodeIndex + 1]][value] -= capacity
    return network

if __name__ == '__main__':
    #startNode = 0
    #endNode = 6
        
    startNode, endNode = [ord(x) - 65 for x in open("route.txt", "r").readline().strip('\r\n').split('>')]
    print chr(startNode + 65) + ">" + chr(endNode + 65)
    
    currentNode = startNode
    
    network = populateNetwork("network.txt")
    
    path, nodeTable = calculateShortestPath(network, startNode, currentNode, endNode)
    print "Shortest Path:", [chr(x + 65) for x in path], "Distance", nodeTable[endNode].distFromSource
    #SHOW DISTANCE OF SHORTESTPATH
  
    maxFlow = maxFlow(path, network, startNode, currentNode, endNode)
    print "Total Max Flow:", maxFlow
    
