import queue
import time
def misplaced(current, goal):  # h(n) A heuristic function

    '''A heuristic function that calculates & returns 
    the number of misplaced puzzles
    by comparing the current state to the goal state'''

    difference = 0 # counter of tiles that are misplaced

    # a loop that compares every puzzle tiles at the current state to goal state
    for i in range(len(current)):
        if current[i] != 0:
            if current[i] != goal[i]:
                difference += 1

    return difference

def manhattan(current, goal):  # h(n) A heuristic function

    '''A heuristic function that calculates & returns 
    the sum of the manhattan distance every puzzles 
    from current state to the goal state
    by comparing the current state to the goal state'''

    distance = 0

    # a list stores 2d coordinates in a 1d array
    pos1dCon2d= [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

    # a for loop to get the sum of taxi distance of a puzzle tiles
    for i in range(1,len(goal)):
        # '0' in the puzzle does not count as a tile, 
        # so its distance to goal state is ignored. Starts at 1.
        
        # puzzle 'i' 2d coordinates at start state
        # linear index convertion 2d coordinates of tile 'i'
        # print(current)
        con1dTo2dpos0 = pos1dCon2d[current.index(i)] 

        y0,x0 = con1dTo2dpos0

        # puzzle 'i' 2d coordinates at goal state
        # linear index convertion 2d coordinates of tile 'i'
        con1dTo2dpos1 = pos1dCon2d[goal.index(i)] 
        y1,x1 = con1dTo2dpos1

        # manhattan distance = |horizonton| + |vertical| distance
        temp = abs(x1-x0) + abs(y1-y0)

        distance += temp
            

    return distance

def swap(state, action):

    '''
    A function that perfrom sliding a tile to the empty space '0'
    according to the direction given in parameter 'action'. 
    Returns a new 8-puzzle after a successful slide.
    '''
    puzzle = state[:]
    pos0 = puzzle.index(0)

    # a list stores 2d coordinates in a 1d array
    pos1dCon2d= [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

    # puzzle 'i' 2d coordinates at start state
    # linear index convertion 2d coordinates of tile 'i'
    y0,x0 = pos1dCon2d[pos0]

    '''
    U: y0-1,x0 -1<y<3
    D: y0+1,x0 -1<y<3
    L: y0,x0-1 -1<x<3
    R: y0,x0+1 -1<x<3
    '''
    
    # convert 3D movement to an array
    directions={'U':(y0-1,x0),
                'D':(y0+1,x0),
                'L':(y0,x0-1),
                'R':(y0,x0+1) }


    (y1,x1) = directions[action] # position of the item that is swaping with '0'
    newpos = (y1,x1)

    

    try: # catch the out of bound error from moveing a tile to the wrong way
        #find the linear index from the 2d coordinates
        newIndex = pos1dCon2d.index(newpos)

        # print("newIndex: ")
        # print(newIndex)
        # print("newpos: ")
        # print(newpos)

        if (y1 < 0) or (y1 > 2) or (x1 < 0) or (x1 > 2): # an invalid swap when moveing a tile to the wrong way
            # print('<0 move fail!!!')
            return puzzle
        else: # a valid swap
            # set puzzle[pos0] in list, value to puzzle[newpos]
            puzzle[pos0] = puzzle[newIndex]
            # set puzzle[newpos] in list, value to 0
            puzzle[newIndex] = 0

            return puzzle
    except: # an invalid swap returns the same puzzle
        # print('Error! move fail!!!')
        return puzzle

def puzzle_display(grid):

    '''A function to display a list of numbers into a puzzle.'''
    
    #The zero represents an empty space in the puzzle.
    
    puzzle = f'''
    ╔═══╦═══╦═══╗
    ║ {grid[0]} ║ {grid[1]} ║ {grid[2]} ║
    ╠═══╬═══╬═══╣
    ║ {grid[3]} ║ {grid[4]} ║ {grid[5]} ║
    ╠═══╬═══╬═══╣
    ║ {grid[6]} ║ {grid[7]} ║ {grid[8]} ║
    ╚═══╩═══╩═══╝
    '''
    print(puzzle)

def solver(h,start, goal):

    '''Solve the puzzle with A* algorithm'''
    
    toExpand = queue.PriorityQueue() # a list of states ranked to be explored
    # this is a priority queue to store all possible states, 
    # and returns the lowest state on the the 1st item

    explored = [] # stores states that has been explored 
    # so the same state discover later in the search tree 
    # won't be added to the queue and the explored list again
    # This implies a better cost to the same state exist already in the queue,
    # or another potentially better path to reach goal state to explore

    puzzle = start[:] # a copy of list content from start state

    target = [goal] # a copy of list content from goal state

    toExpand.put((0,0,0,puzzle)) # add the start state to the queue to start searching

    # print('-1-')

    found = [] #stores the state object solved

    while True:
        '''
        Change search path when the same state with lower cost is found
        '''
        
        # current puzzle object in queue: (fn,gn,hn,["tiles"])
        temp_puzzle = toExpand.get() # get the state with lowest f(n)

        print(f'g(n): {temp_puzzle[1]} | h(n): {temp_puzzle[2]}')
        puzzle_display(temp_puzzle[-1])

        if (temp_puzzle[3] in target): # check if the current state is the goal
            print('Target found!')
            found.append(temp_puzzle) # stores the object outside of this scope
            break # stop searching when the target is found
       
        # print('-2-')

        # Produce all next possible states, with f(n) on each
        # f(n) = g(n) + h(n)
        # g(n) the total cost taken to get to the current state
        # h(n) the heuristic distance of all tiles to its goal state
        moves = ['U','D','L','R'] # all possible movements for the empty space
        
        for i in moves: # Repeat action for left, right, up, down
            # produce a puzzle state after one of the possible action
            moved = swap(temp_puzzle[-1],i) 

            # if produced state has not been explored
            if not(moved in explored): 
                
                explored.append(moved) # add state to explored
                he = 0
                if h == '1': # choice of heuristic function: 
                    he = misplaced(moved,goal) # '1' for misplaced tiles; 
                elif h == '2': 
                    he = manhattan(moved,goal) #'2' for manhattan distance

                g = temp_puzzle[1]+1 #step cost = previous state's step cost + 1
                f = g + he
                toExpand.put((f,g,he, moved)) # store states to queue

                
            
            
        # print('-3-')
        
        # print('-4-')

    # print("Search finished!")
    if len(found) != 0:
        print("---Goal State:---")
        puzzle_display(found[0][3])
        print("\nSteps taken:")
        print(found[0][1])
        print("\nPossible states explored:")
        print(len(explored))
    else:
        print("A* Search returns no results!")
    
    return

def validDigits(strState):

    """
    Function that checks for valid amount of numbers are entered
    """

    try: # if the string contants any non-numerical text
        test = int(strState)
    except:
        return False # the string is not valid

    digitCounter = set() # checks duplicated numbers

    for i in strState:
        if i == '9': # '9' does not exist in 8-puzzle
            return False
        else:
            digitCounter.add(i)
    # print(len(digitCounter)) # test code

    if (len(digitCounter) > 0 and len(digitCounter) == 9):
        # print("length!")
        # return False # returns false if duplicated numbers are found
        return True
    else:
        # return True
        # print("length!") # test code
        return False # returns false if duplicated numbers are found

def inputState():

    '''
    Puzzle state input validation.
    Either '' or '0-8'
    '''

    while True:

        strState = str(input("Enter state:"))

        if ((len(strState) == 0) or validDigits(strState)):
            break
        else:
            Warning = '''
            ╔══════════════════════════════════════════════════════╗
            ║ ********* Warning: Invalid state input! ************ ║
            ║                                                      ║
            ║ Please either press Enter for default state,         ║
            ║ or follow the guidance above to input a valid state! ║
            ║                                                      ║
            ╚══════════════════════════════════════════════════════╝
            '''
            print(Warning)
    
    return strState

def conList(strState):

    '''
    Function converts a string of numbers to a list of numbers
    '''

    # convert string of numbers to a list
    listOfState = []
    for i in strState:
        listOfState.append(int(i))

    return listOfState

def menu():

    '''
    This is the menu function for the entire program.
    '''

    welcome = '''
    ╔═════════════════════════════════════════╗
    ║ ECM2423 - Coursework exercise           ║
    ║ Question 1 |                            ║
    ║ Implement a heuristic search algorithm: ║
    ║ A* and the 8-puzzle game.               ║
    ╚═════════════════════════════════════════╝
    *This program does not an check for unsolvable puzzles

    '''

    message = '''
    ╔══════════════════════════════════╗
    ║ A 8-puzzle state input example:  ║
    ║                                  ║
    ║ Enter: 123456780                 ║
    ║           ╔═══╦═══╦═══╗          ║
    ║ It means: ║ 1 ║ 2 ║ 3 ║          ║
    ║           ╠═══╬═══╬═══╣          ║
    ║           ║ 4 ║ 5 ║ 6 ║          ║
    ║           ╠═══╬═══╬═══╣          ║
    ║           ║ 7 ║ 8 ║ 0 ║          ║
    ║           ╚═══╩═══╩═══╝          ║
    ║           *** Note: ***          ║
    ║ - Only enter the number 0-8 once!║
    ║ - Press Enter for default states!║
    ║                                  ║    
    ║ Default start states:            ║
    ║ 724506831                        ║
    ║                                  ║
    ║ Default goal states:             ║
    ║ 012345678                        ║
    ║                                  ║
    ╚══════════════════════════════════╝

    '''
    m0 = '''
    ╔═════════════════════════════╗
    ║ Please enter a start state: ║
    ╚═════════════════════════════╝
    '''
    m1 = '''
    ╔═════════════════════════════╗
    ║ Please enter a goal state:  ║
    ╚═════════════════════════════╝
    '''
    print(welcome)
    print(message+'\n')
    print(m0+'\n')
    state0 = inputState()

    print(m1+'\n')
    state1 = inputState()

    m3 = '''
    ╔══════════════════════════════════════╗
    ║ Please choose a heuristic function:  ║
    ║                                      ║ 
    ║ Enter: 1                             ║ 
    ║ or                                   ║
    ║ Enter: 2                             ║
    ║                                      ║
    ║ 1: Misplaced tiles                   ║
    ║                                      ║
    ║ 2: Manhattan distance                ║
    ╚══════════════════════════════════════╝
    '''
    print(m3)
    while True:
        h = str(input("Enter:"))
        if (h == '1') or (h == '2'):
            print('Valid choice!')
            break

        else:
            m4 = '''
                        ╔══════════════════════════════════════════════════════╗
                        ║ ********* Warning: Invalid choice input! *********** ║
                        ║                                                      ║
                        ║ Please enter a valid function choice advised above!  ║
                        ║                                                      ║
                        ╚══════════════════════════════════════════════════════╝
                        '''
            print(m4)

    

    # default state & goal state
    if state0 == '':
        start_state = [7, 2, 4, 5, 0, 6, 8, 3, 1]
    else:
        start_state = conList(state0)

    if state1 == '':
        goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    else:
        goal_state = conList(state1)


    print('-----Start State:-----')
    puzzle_display(start_state)
    start = time.time()
    solver(h,start_state,goal_state)
    end = time.time()
    diff = end - start
    print("Time taken: ", diff)

    print("\nThe search is finish! \n")

if __name__ == '__main__':
    menu()