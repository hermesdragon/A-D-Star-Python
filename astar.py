import sys, pygame, math, heapq
from pygame.locals import *

cell_size =  8
num_cells = 101


cells = {}
for x in range(num_cells):
    for y in range(num_cells):
        cells[(x,y)]= {'state':None,'f_score':None,'h_score':None,'g_score':None,'parent':None}  

black = (0,0,0)             
bright_green = (0, 204, 102) 
red = (255, 44, 0)          
orange = (255, 175, 0)     
blue = (0, 124, 204)        
white = (250,250,250)       

pygame.init()
size = width, height = (cell_size*num_cells)+2, (cell_size*num_cells)+2
screen = pygame.display.set_mode(size)
pygame.display.set_caption = ('Pathfinder')

start = None
goal = None

traversedcells = []      
fscoredicts = {}
closed_list = {}    


def initBoard(board):
    background = pygame.Surface(board.get_size())
    background = background.convert()
    background.fill (white)
    
    for i in range(0,(cell_size*num_cells)+1)[::cell_size]:
        pygame.draw.line(background, black, (i, 0), (i, cell_size*num_cells), 2)
        pygame.draw.line(background, black, (0, i), (cell_size*num_cells, i), 2)
    return background

def onBoard(node):
    x, y = node
    return x >= 0 and x < num_cells and y >= 0 and y < num_cells

def orthoganals(current):
    x, y = current
    N = x-1, y
    E = x, y+1
    S = x+1, y
    W = x, y-1
    directions = [N, E, S, W]
    return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list]


def diagonals(current):
    x, y = current
    NE = x-1, y+1
    SE = x+1, y+1
    SW = x+1, y-1
    NW = x-1, y-1
    directions = [NE, SE, SW, NW]
    return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list]

def unwind_path(coord):
    if cells[coord]['parent'] != None:
        left, top = coord
        left = (left*cell_size)+2
        top = (top*cell_size)+2
        r = pygame.Rect(left, top, cell_size-2, cell_size-2)
        pygame.draw.rect(board, blue, r, 0)
        screen.blit(board, (0,0))
        pygame.display.flip()
        unwind_path(cells[coord]['parent'])
def processNode(coord):
    global goal, traversedcells, closed_list, fscoredicts, board, screen
    if coord == goal:
        print "Cost is" ,  cells[goal]['g_score']/float(10)
        unwind_path(cells[goal]['parent'])
        return
    l = [] 
    for x in diagonals(coord):
        if cells[x]['g_score'] == None:
        	cells[x]['g_score'] = cells[coord]['g_score'] + 14
        	cells[x]['parent'] = coord
        	l.append(x)
        elif cells[x]['g_score'] > cells[coord]['g_score'] + 14:
            cells[x]['g_score'] = cells[coord]['g_score'] + 14
    	    cells[x]['parent'] = coord
            l.append(x)
    
    for x in orthoganals(coord):
        if cells[x]['g_score'] == None:
            cells[x]['g_score'] = cells[coord]['g_score'] + 10
            cells[x]['parent'] = coord
            l.append(x)
        elif cells[x]['g_score'] > cells[coord]['g_score'] + 10:
            cells[x]['g_score'] = cells[coord]['g_score'] + 10
            cells[x]['parent'] = coord
            l.append(x)
    
    for x in l:
        if x != goal:
            left, top = x
            left = (left*cell_size)+2
            top = (top*cell_size)+2
            r = pygame.Rect(left, top, cell_size-2, cell_size-2)
            pygame.draw.rect(board, white, r, 0)
            screen.blit(board, (0,0))
            pygame.display.flip()
        if cells[x]['f_score'] in fscoredicts:
            if len(fscoredicts[cells[x]['f_score']]) > 1:
                fscoredicts[cells[x]['f_score']].remove(x)
            else:
                fscoredicts.pop(cells[x]['f_score'])
            traversedcells.remove(cells[x]['f_score'])
        x1, y1 = goal
        x0, y0 = x
        cells[x]['h_score'] = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )*10
        cells[x]['f_score'] = cells[x]['h_score'] + cells[x]['g_score']
        traversedcells.append(cells[x]['f_score'])
        if cells[x]['f_score'] in fscoredicts:
            fscoredicts[cells[x]['f_score']].append(x)
        else:
            fscoredicts[cells[x]['f_score']] = [x]

    heapq.heapify(traversedcells)
    if len(traversedcells) == 0:
        print 'No path detected'
        return
    f = heapq.heappop(traversedcells)
    if len(fscoredicts[f]) > 1:
        node = fscoredicts[f].pop()
    else:
        node = fscoredicts.pop(f)[0]    
    heapq.heapify(traversedcells)
    closed_list[node]=True
    if node != goal:
        left, top = node
        left = (left*cell_size)+2
        top = (top*cell_size)+2
        r = pygame.Rect(left, top, cell_size-2, cell_size-2)
        pygame.draw.rect(board, white, r, 0)
        screen.blit(board, (0,0))
        pygame.display.flip()
    processNode(node)
def findPath():
    if start != None and goal != None:
        cells[start]['g_score'] = 0
        x1, y1 = goal
        x0, y0 = start
        cells[start]['h_score'] = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )*10
        cells[start]['f_score'] = cells[start]['h_score'] + cells[start]['g_score']
        closed_list[start]=True
        processNode(start)

board = initBoard(screen)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        key=pygame.key.get_pressed()
        left_click, middle_click, right_click = pygame.mouse.get_pressed()
        ctrl = key[pygame.K_LCTRL] or key[pygame.K_RCTRL]
        escape = key[pygame.K_ESCAPE]
        shift = key[pygame.K_LSHIFT]
        enter = key[pygame.K_RETURN]
        

        x, y = pygame.mouse.get_pos()
        left = ((x/cell_size)*cell_size)+2
        top = ((y/cell_size)*cell_size)+2
        x_index = (left-2)/cell_size
        y_index = (top-2)/cell_size
        
        if (x_index, y_index) in cells:
            if ctrl and left_click:
            	x_index = 100
            	y_index = 60
            	left = (x_index*cell_size)+2
            	top = (y_index*cell_size)+2
                cells[(x_index, y_index)]['state']='Start'
                r = pygame.Rect(left, top, cell_size-2, cell_size-2)
                pygame.draw.rect(board, bright_green, r, 0)
                start = (x_index, y_index)
            elif ctrl and right_click:
            	x_index = 51
            	y_index = 51
            	left = (x_index*cell_size)+2
            	top = (y_index*cell_size)+2
                cells[(x_index, y_index)]['state']='Goal'
                r = pygame.Rect(left, top, cell_size-2, cell_size-2)
                pygame.draw.rect(board, red, r, 0)
                goal = (x_index, y_index)
            elif shift and left_click:
            	fileobj = open ( 'matrix.txt' , 'r')
            	lst = [ map(int,line.split()) for line in fileobj ]
            	for obx,lstobx in enumerate(lst):
            		for oby,lstob in enumerate(lstobx):
            			if(lstob == 1):
            				x_index = oby
            				y_index = obx 
            				left = (x_index*cell_size)+2
            				top = (y_index*cell_size)+2
            				cells[(x_index, y_index)]['state']='Wall'
            				r = pygame.Rect(left, top, cell_size-2, cell_size-2)
            				pygame.draw.rect(board, black, r, 0)
            	fileobj.close()
            elif escape:
                for cell in cells:
                    for x in cells[cell]:
                        cells[cell][x]=None
                board = initBoard(screen)
                start = goal = None
                traversedcells = []
                closed_list = {}
                fscoredicts = {}
            elif enter:
                findPath()
            screen.blit(board, (0,0))
            pygame.display.flip()