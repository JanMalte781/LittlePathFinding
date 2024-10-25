import math


class AStarNode():

    def __init__(self, predecessor=None, position=None):
        self.predecessor = predecessor # AStarNode
        self.position = position # 2d touple 

        self.f = 0 # estimated cost of reaching the end from start through self 
        self.g = 0 # cost of reaching the Node
        self.h = 0 # estimated cost of reaching the end Node from self

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.position == other.position
        return False

    def setPos(self, position):
        self.position = position

    def setPredecessor(self, predecessor):
        self.predecessor = predecessor


    # updates the f,g,h value based on the predecessor
    def updateAttr(self, endPosition):
        if not self.predecessor == None:
            self.g = self.predecessor.g + math.sqrt( (self.predecessor.position[0] - self.position[0])**2 + (self.predecessor.position[1] - self.position[1])**2 )
            self.h = math.sqrt( (endPosition[0] - self.position[0])**2 + (endPosition[1] - self.position[1])**2 )
            self.f = self.g + self.h



def a_star(startingPos : tuple[int, int], finalPos : tuple[int, int], board : list[list[int]]):
    'finds shortest path between startingPos and finalPos using A*. startingPos and endPos must be 2d touples and board mus be 2d list'
    'free spaces in the board musst be represented by 0'
    'returns list of Tuples representing x,y corrdinates of the shortest path'
    'returns an empty list if there is no path'

    listOrderColor = [] # list all positions in order in which they are visited and which list, openList = 0, closed List = 1

    # ceck if positions are on the board
    if startingPos[0] < 0 or startingPos[1] < 0 or startingPos[0] >= len(board[0]) or startingPos[1] >= len(board):
        return []
    
    if finalPos[0] < 0 or finalPos[1] < 0 or finalPos[0] >= len(board[0]) or finalPos[1] >= len(board):
        return []

    openList = [] # contains AStarNodes in ascending order of f value
    closedList = set() # contains already searched Nodes

    # initializing openList, start and end Node
    startNode = AStarNode(None, startingPos)
    startNode.f = 0
    startNode.g = 0
    startNode.h = 0

    endNode = AStarNode(None, finalPos)

    # add starting point to list of nodes to search
    openList.append(startNode)
    listOrderColor.append((startNode.position, 0))

    # loop over all reachable nodes
    while not len(openList) == 0:
        
        # make sure we access element with the highest priority
        openList.sort(key= lambda c : c.f, reverse=True)
        
        currentNode = openList.pop()

        # add current node to already searched nodes
        closedList.add(currentNode.position)
        listOrderColor.append((currentNode.position, 1))

        # check if done
        if currentNode == endNode:
            return (path(currentNode), listOrderColor)
        
        neighbours = []

        # loop over all neighbours
        for deltaPosition in [(1,1), (1,-1), (-1,1,), (-1,-1), (-1,0), (0,-1), (0,1), (1,0)]:
            
            newPosition = (currentNode.position[0] + deltaPosition[0], currentNode.position[1] + deltaPosition[1])

            # skip positions that are not on the board
            if newPosition[0] < 0 or newPosition[1] < 0 or newPosition[0] >= len(board[0]) or newPosition[1] >= len(board):
                continue

            # skip walls
            if board[newPosition[1]][newPosition[0]] != 0:
                continue

            newNode = AStarNode(currentNode, newPosition)
            newNode.updateAttr(finalPos)
            neighbours.append(newNode)

        for node in neighbours:

            # update costs and heuristic
            node.setPredecessor(currentNode)
            node.updateAttr(finalPos)

            # if node was already searched, check if new path is better and update f,g,h values and predecessor
            
            for openNode in openList: 
                if node == openNode:
                    if node.g < openNode.g:
                        openNode.setPredecessor(node.predecessor)
                        openNode.updateAttr(finalPos)
                    continue
            
            
            if (not node.position in closedList) and (not node in openList):
                openList.append(node)
                listOrderColor.append((node.position, 0))
              

    return []


def path(node: AStarNode):
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

    path = a_star(start, end, maze)


if __name__ == '__main__':
    main()
