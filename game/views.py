from django.shortcuts import render,redirect
from copy import deepcopy



DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}




StartBox = [[0 for i in range(3)] for i in range(3)]
ENDBOX=[[0 for i in range(3)] for i in range(3)]
startarray=[['' for i in range(3)] for i in range(3)]
endarray=[['' for i in range(3)] for i in range(3)]
arrayToPrint = []
arrayTomove=[]






#it is the node which store each state of puzzle
class GamePuzzleNode:
    def __init__(self, current_state, previous_state, g, h, direction):
        self.current_state = current_state
        self.previous_state = previous_state
        self.g = g
        self.h = h
        self.direction = direction

    def f(self):
        return self.g + self.h







def get_position_element(current_array, element):
    for row in range(len(current_array)):
        if element in current_array[row]:
            return (row, current_array[row].index(element))








def Cost(current_array):
    cost = 0
    for row in range(len(current_array)):
        for col in range(len(current_array[0])):
            pos = get_position_element(ENDBOX, current_array[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost








#get adjucent Nodes
def getChilds(node):
    listchild = []
    emptyplace = get_position_element(node.current_state, 0)

    for dir in DIRECTIONS.keys():
        newPosition = (emptyplace[0] + DIRECTIONS[dir][0], emptyplace[1] + DIRECTIONS[dir][1])
        if 0 <= newPosition[0] < len(node.current_state) and 0 <= newPosition[1] < len(node.current_state[0]):
            newState = deepcopy(node.current_state)
            newState[emptyplace[0]][emptyplace[1]] = node.current_state[newPosition[0]][newPosition[1]]
            newState[newPosition[0]][newPosition[1]] = 0
            listchild.append(GamePuzzleNode(newState, node.current_state, node.g + 1, Cost(newState), dir))

    return listchild






#get the best node available among nodes
def getBestChild(openMap):
    firstchild = True
    for node in openMap.values():
        if firstchild or node.f() < bestF:
            firstchild = False
            bestchild = node
            bestF = bestchild.f()
    return bestchild






#this functionn create the smallest path
def PrintPath(closedMap):
    node = closedMap[str(ENDBOX)]
    branch=list()
    while node.direction:
        branch.append({
            'dir': node.direction,
            'node': node.current_state
        })
        node = closedMap[str(node.previous_state)]
    branch.append({
        'dir': '',
        'node': node.current_state
    })
    branch.reverse()
    return branch






#main function of node
def main(puzzle):
    open_map = {str(puzzle): GamePuzzleNode(puzzle, puzzle, 0, Cost(puzzle), "")}
    closed_map = {}

    while True:
        test_child = getBestChild(open_map)
        closed_map[str(test_child.current_state)] = test_child

        if test_child.current_state == ENDBOX:
            return PrintPath(closed_map)

        child_node = getChilds(test_child)
        for child in child_node:
            if str(child.current_state) in closed_map.keys()\
                    or str(child.current_state) in open_map.keys() \
                    and open_map[str(child.current_state)].f() < child.f():
                continue
            open_map[str(child.current_state)] = child

        del open_map[str(test_child.current_state)]







def homegame(request):
    empty='N'
    virsum=1
    if request.method=='POST':
        for i in range(3):
            for j in range(3):
                virable = str(virsum)
                startarray[i][j]=request.POST[virable]
                virsum=virsum+1
            if request.POST[virable] == '':
                empty = "one or two boxes are empty"
                return render(request,'homegame.html',{'empty':empty})

        for i in range(3):
            for j in range(3):
                 virable = str(virsum)
                 endarray[i][j] = request.POST[virable]
                 virsum = virsum + 1
                 if request.POST[virable] == '':
                     empty = "one or two boxes are empty or all empties"
                     return render(request,'homegame.html',{'empty':empty})

        for i in range(3):
            for j in range(3):
                StartBox[i][j] = int(startarray[i][j])
                ENDBOX[i][j] = int(endarray[i][j])

        return redirect('gamestarted')
    return render(request,'homegame.html')

def gamestarted(request):
    arrayToPrint.clear()
    arrayTomove.clear()

    if request.method=="POST":
        return redirect('homegame')

    br = main(StartBox)
    for i in br:
        arrayToPrint.append(i['node'])
        arrayTomove.append(i['dir'])

    return render(request,'gamestarted.html',{'arrayToPrint':arrayToPrint,'arrayTomove':arrayTomove})