import math

class DijkstraNode():

    def __init__(self, predecessor=None, position=None):
        self.predecessor = predecessor # AStarNode
        self.position = position # 2d touple 

        self.g = 0 # cost of reaching the Node

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.position == other.position
        return False

    def setPos(self, position):
        self.position = position

    def setPredecessor(self, predecessor):
        self.predecessor = predecessor

    # updates the f,g,h value based on the predecessor
    def updateAttr(self):
        if not self.predecessor == None:
            self.g = self.predecessor.g + math.sqrt( (self.predecessor.position[0] - self.position[0])**2 + (self.predecessor.position[1] - self.position[1])**2 )
            

def dijkstraPath(startingPos : tuple[int, int], finalPos : tuple[int, int], board : list[list[int]]):
    
    listOrderColor = [] # list all positions in order in which they are visited and which list they are in, unvisited = 0, visited = 1

    # ceck if positions are on the board
    if startingPos[0] < 0 or startingPos[1] < 0 or startingPos[0] >= len(board[0]) or startingPos[1] >= len(board):
        return []
    
    if finalPos[0] < 0 or finalPos[1] < 0 or finalPos[0] >= len(board[0]) or finalPos[1] >= len(board):
        return []
    
    unvisitedNodes = []
    visitedNodes = set()

    startingNode = DijkstraNode(None, startingPos)
    startingNode.g = 0

    endNode = DijkstraNode(None, finalPos)

    unvisitedNodes.append(startingNode)
    listOrderColor.append((startingNode.position, 1))

    while not len(unvisitedNodes) == 0:

        unvisitedNodes.sort(key= lambda f : f.g, reverse= True)
        
        currentNode = unvisitedNodes.pop()
        visitedNodes.add(currentNode.position)
        listOrderColor.append((currentNode.position,1))

        if currentNode == endNode:
            return (path(currentNode), listOrderColor)
        
        neighbours = []

        for deltaPosition in [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]:

            newPosition = (currentNode.position[0] + deltaPosition[0], currentNode.position[1] + deltaPosition[1])

            # skip positions that are not on the board
            if newPosition[0] < 0 or newPosition[1] < 0 or newPosition[0] >= len(board[0]) or newPosition[1] >= len(board):
                continue

            # skip walls
            if board[newPosition[1]][newPosition[0]] != 0:
                continue

            newNode = DijkstraNode(currentNode, newPosition)
            newNode.updateAttr()
            neighbours.append(newNode)

        for node in neighbours:
            
            node.setPredecessor(currentNode)
            node.updateAttr()


            for unvisitedNode in unvisitedNodes:
                if unvisitedNode == node:
                    if node.g < unvisitedNode.g:
                        unvisitedNode.setPredecessor(node.predecessor)
                        unvisitedNode.updateAttr()
                    continue
            
            if (node.position not in visitedNodes) and (node not in unvisitedNodes):
                unvisitedNodes.append(node)
                listOrderColor.append((node.position, 0))

    return[]

def path(node: DijkstraNode):
    path = []
    current = node
    while current is not None:
        path.append(current.position)
        current = current.predecessor
    return path[::-1]

def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (9, 9)

    path = dijkstraPath(start, end, maze)


if __name__ == '__main__':
    main()
