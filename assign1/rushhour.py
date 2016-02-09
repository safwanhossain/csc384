#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint

##################################################
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################


class rushhour(StateSpace):
    def __init__(self, action, gval, board_size, vehicle_list, 
            goal_entrance, goal_direction, parent=None ):
        """Initialize a rushhour search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.board_size = board_size
        self.vehicle_list = vehicle_list
        self.goal_entrance = goal_entrance
        self.goal_direction = goal_direction


    def successors(self):
        '''Return list of rushhour objects that are the successors of the current object'''
        
        def position_not_valid( curr_vehicle ):
            '''Check whether the current vehicle being considered is 
            about to go to a position that is invalid'''
           
            def process_cars( position, length, is_horizontal ):
                '''Since we allow cars to be split, the position validity algorithm requries that
                we treat split cars as independent car'''
                if is_horizontal and ((position[0] + length) >= self.board_size[1]):
                    # car overlaps(horizontally); so make two "goal" cars
                    overflow = length - (self.board_size[1] - position[0])
                    car1 = { 'y':position[1], 'x_start':position[0], 'x_end':self.board_size[1] }
                    car2 = { 'y':position[1], 'x_start':0, 'x_end': overflow-1 }
                    car1['is_horizontal'], car2['is_horizontal'] = True, True
                    return (car1, car2)
                elif is_horizontal:
                    car = { 'y':position[1], 'x_start':position[0], 'x_end':position[0]+length-1 }
                    car['is_horizontal'] = True
                    return car
                elif (not is_horizontal) and ((position[1] + length) >= self.board_size[0]):
                    # car overlaps(vertically); so make two "goal" cars
                    overflow = length - (self.board_size[0] - position[1])
                    car1 = { 'x':position[0], 'y_start':position[1], 'y_end':self.board_size[0] }
                    car2 = { 'x':position[0], 'y_start':0, 'y_end': overflow-1 }
                    car1['is_horizontal'], car2['is_horizontal'] = False, False
                    return (car1, car2)
                elif (not is_horizontal):
                    car = { 'x':position[0], 'y_start':position[1], 'y_end':position[1]+length-1 }
                    car['is_horizontal'] = False
                    return car
            
            def interval_match( curr_car, other_cars ):
                match = False
                for vehicle in other_cars:
                    # currCar is horizontal and vehicle is vertical
                    if curr_car['is_horizontal'] and (not vehicle['is_horizontal']):
                        match = (vehicle['x'] >= curr_car['x_start'] and vehicle['x'] <= curr_car['x_end']) and \
                            (curr_car['y'] >= vehicle['y_start'] and curr_car['y'] <= vehicle['y_end'])

                    # currCar is vertical and vehicle is horizontal
                    if (not curr_car['is_horizontal']) and vehicle['is_horizontal']:
                        match = (vehicle['y'] >= curr_car['y_start'] and vehicle['y'] <= curr_car['y_end']) and \
                            (curr_car['x'] >= vehicle['x_start'] and curr_car['x'] <= vehicle['x_end'])

                    # both cars are horizontal
                    if curr_car['is_horizontal'] and vehicle['is_horizontal']:
                        if curr_car['y'] != vehicle['y']:
                            match = False
                        else:
                            match = (curr_car['x_start'] >= vehicle['x_start'] and curr_car['x_start'] <= vehicle['x_end']) or \
                                (vehicle['x_start'] >= curr_car['x_start'] and vehicle['x_start'] <= curr_car['x_end'])  
                    
                    # both cars are vertical
                    if (not curr_car['is_horizontal']) and (not vehicle['is_horizontal']):
                        if curr_car['x'] != vehicle['x']:
                            match = False
                        else:
                            match = (curr_car['y_start'] >= vehicle['y_start'] and curr_car['y_start'] <= vehicle['y_end']) or \
                                (vehicle['y_start'] >= curr_car['y_start'] and vehicle['y_start'] <= curr_car['y_end'])  
                    if match == True:
                        return match
                return False

            vehicles = []
            for v in self.vehicle_list:
                if v[0] == curr_vehicle[0]:
                    continue
                cars = process_cars( v[1], v[2], v[3])
                if isinstance(cars, tuple):
                    vehicles.append( cars[0] )
                    vehicles.append( cars[1] )
                else:
                    vehicles.append( cars )

            curr_cars = process_cars( curr_vehicle[1], curr_vehicle[2], curr_vehicle[3])
            if isinstance(curr_cars, tuple):
                match1 = interval_match( curr_cars[0], vehicles )
                match2 = interval_match( curr_cars[1], vehicles )
                return (match1 or match2)
            else:
                return interval_match( curr_cars, vehicles )
        
        def get_new_vehicle_positions( vehicle ):
            '''Return a pair of the same vehicle in different valid positions'''
            
            def assign_vehicle_pos( vehicle, new_pos1, new_pos2 ):
                '''Create a Vehicle pair with given positions'''
                new_vehicle_states = []
                
                new_vehicle_state1 = list(vehicle)
                new_vehicle_state1[1] = new_pos1
                if position_not_valid( new_vehicle_state1 ) == False:
                    new_vehicle_states.append( new_vehicle_state1 )

                new_vehicle_state2 = list(vehicle)
                new_vehicle_state2[1] = new_pos2
                if position_not_valid( new_vehicle_state2 ) == False:
                    new_vehicle_states.append( new_vehicle_state2 )
                
                return new_vehicle_states

            curr_pos = vehicle[1]
            m, n = self.board_size[0], self.board_size[1] 
            new_vehicle_states = None
            if vehicle[3] == True:      # Horizontal
                if curr_pos[0] == n-1:  # Need to wrap around for +ve move 
                    new_pos1 = ( 0, curr_pos[1] )
                    new_pos2 = ( curr_pos[0]-1, curr_pos[1] )
                    new_vehicle_states = assign_vehicle_pos(vehicle, new_pos1, new_pos2)
                elif curr_pos[0] == 0:   # Need to wrap around for -ve move
                    new_pos1 = ( n-1, curr_pos[1] )
                    new_pos2 = ( curr_pos[0]+1, curr_pos[1] )
                    new_vehicle_states = assign_vehicle_pos(vehicle, new_pos1, new_pos2)
                else:                   # General Case
                    new_pos1 = ( curr_pos[0]-1, curr_pos[1] )
                    new_pos2 = ( curr_pos[0]+1, curr_pos[1] )
                    new_vehicle_states = assign_vehicle_pos(vehicle, new_pos1, new_pos2)
            else:                       # Vertical 
                if curr_pos[1] == m-1:  # Need to wrap around to +ve move 
                    new_pos1 = ( curr_pos[0], 0 )
                    new_pos2 = ( curr_pos[0], curr_pos[1]-1 )
                    new_vehicle_states = assign_vehicle_pos(vehicle, new_pos1, new_pos2)
                elif curr_pos[1] == 0:   # Need to wrap around to -ve move
                    new_pos1 = ( curr_pos[0], m-1 )
                    new_pos2 = ( curr_pos[0], curr_pos[1]+1 )
                    new_vehicle_states = assign_vehicle_pos(vehicle, new_pos1, new_pos2)
                else:                   # General Case
                    new_pos1 = ( curr_pos[0], curr_pos[1]-1 )
                    new_pos2 = ( curr_pos[0], curr_pos[1]+1 )
                    new_vehicle_states = assign_vehicle_pos(vehicle, new_pos1, new_pos2)
            return new_vehicle_states

        def get_action( new_vehicle_state, old_vehicle_state ):
            is_horizontal = new_vehicle_state[3]
            action_name = 'move_vehicle(' + new_vehicle_state[0]
            m, n = self.board_size[0], self.board_size[1] 
            if is_horizontal == True:
                # at the eastern edge, moving east
                if (old_vehicle_state[1][0] == n-1) and (new_vehicle_state[1][0] == 0):
                    action_name += ', E)'
                # at the western edge, moving west
                elif (old_vehicle_state[1][0] == 0) and (new_vehicle_state[1][0] == n-1):
                    action_name += ', W)'
                # general case
                elif new_vehicle_state[1][0] > old_vehicle_state[1][0]: 
                    action_name += ', E)'
                elif new_vehicle_state[1][0] < old_vehicle_state[1][0]: 
                    action_name += ', W)'
            else:
                # at the southern edge, moving south
                if (old_vehicle_state[1][1] == m-1) and (new_vehicle_state[1][1] == 0):
                    action_name += ', S)'
                # at the northern edge, moving north
                elif (old_vehicle_state[1][1] == 0) and (new_vehicle_state[1][1] == m-1):
                    action_name += ', N)'
                # general case
                elif new_vehicle_state[1][1] > old_vehicle_state[1][1]: 
                    action_name += ', S)'
                elif new_vehicle_state[1][1] < old_vehicle_state[1][1]: 
                    action_name += ', N)'
            return action_name
        
        def is_vehicle_movable( vehicle ):
            length = vehicle[2]
            is_horizontal = vehicle[3]
            if( is_horizontal and length == self.board_size[1] ):
                return False
            elif( not is_horizontal and length == self.board_size[0] ):
                return False
            return True

        next_states = []
        # each vehicle can move in two ways (+ve and -ve in the direction of orient.)
        # Thus for each vehicle, we need to generate 2 states (max)
        for i in range(0, len(self.vehicle_list)):
            # new possible states for self.vehicle_list[i]
            if ( is_vehicle_movable( self.vehicle_list[i] ) ):
                new_vehicle_states = get_new_vehicle_positions( self.vehicle_list[i] )
                for new_vehicle_state in new_vehicle_states:
                    new_vehicle_list = [ list(v) for v in self.vehicle_list ]
                    new_vehicle_list[i] = new_vehicle_state
                    
                    action_name = get_action( new_vehicle_state, self.vehicle_list[i] )
                    new_game_state = rushhour( action_name, self.gval+1, self.board_size, new_vehicle_list, 
                            self.goal_entrance, self.goal_direction, parent=self ) 
                    next_states.append( new_game_state )
        return next_states 

    def hashable_state(self):
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.
        Our Key will essentially be the vehicle_list but sorted on x pos and deeply
        represented as a tuple'''
        new_list = sorted( self.vehicle_list, key=lambda x: x[1][0], reverse=False )
        hash_tup = tuple( tuple(prop for prop in vehicle) for vehicle in new_list )
        return hash_tup

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

#Data accessor routines.

    def get_vehicle_statuses(self):
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the robot (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        return self.vehicle_list
    
    def get_board_properties(self):
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return (self.board_size, self.goal_entrance, self.goal_direction)    

#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_min_moves(state):
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.
   
    def horizontal_heur( car_pos, des_pos, n ):
        distance_E, distance_W = 0, 0
        if des_pos[0] > car_pos[0]:
            distance_E = des_pos[0] - car_pos[0]
            distance_W = n - distance_E
        else:
            distance_W = car_pos[0] - des_pos[0]
            distance_E = n - distance_W
        return min( distance_E, distance_W )

    def vertical_heur( car_pos, des_pos, m ):
        distance_N, distance_S = 0, 0
        if des_pos[1] > car_pos[1]:
            distance_S = des_pos[1] - car_pos[1]
            distance_N = m - distance_S
        else:
            distance_N = car_pos[1] - des_pos[1]
            distance_S = m - distance_N
        return min( distance_N, distance_S )
    
    def get_min_over_goalcars( car ):
        car_pos = car[1]
        length = car[2]
        is_horizontal = car[3]
        m, n = state.board_size[0], state.board_size[1] 
        
        # goal car horizontal but position not reachable
        if is_horizontal and (car_pos[1] != goal_pos[1]):
            return float("inf")
        # goal car horizontal but goal position is vertical
        elif is_horizontal and (orientation == 'N' or orientation == 'S'):
            return float("inf")
        elif is_horizontal:
            if orientation == 'W':
                return horizontal_heur( car_pos, goal_pos, n )
            else:
                des_pos = ( (goal_pos[0] - length + 1) % n, goal_pos[1] )
                return horizontal_heur( car_pos, des_pos, n )
        
        # goal car vertical but position not reachable
        elif (not is_horizontal) and (car_pos[0] != goal_pos[0]):
            return float("inf")
        # goal car vertical but goal position is horizontal
        elif (not is_horizontal) and (orientation == 'E' or orientation == 'W'):
            return float("inf")
        elif (not is_horizontal):
            if orientation == 'N':
                return vertical_heur( car_pos, goal_pos, m )
            else:
                des_pos = ( goal_pos[0], (goal_pos[1] - length + 1) % m )
                return vertical_heur( car_pos, des_pos, m )
    
    # Already at the goal state
    if rushhour_goal_fn( state ) == True:
        return 0
    goal_pos = state.goal_entrance
    orientation = state.goal_direction
    car = None
   
    goal_cars = []
    for vehicle in state.vehicle_list:
        if vehicle[4] == True:
            goal_cars.append( vehicle )

    heur_vals = []
    for car in goal_cars:
        heur_vals.append( get_min_over_goalcars( car ) )
    return min( heur_vals )

def rushhour_goal_fn(state):
    '''Have we reached a goal state ?'''
    
    def car_at_goal( car ):
        car_pos = car[1]
        length = car[2]
        is_horizontal = car[3]
        if (orientation == 'N') and (is_horizontal == False) and (car_pos == goal_pos):
            return True
        elif (orientation == 'S') and (is_horizontal == False):
            des_y_pos = (goal_pos[1] - length + 1) % state.board_size[0]
            if (car_pos[0] == goal_pos[0]) and (des_y_pos == car_pos[1]):
                return True
        elif (orientation == 'W') and (is_horizontal == True) and (car_pos == goal_pos):
            return True
        elif (orientation == 'E') and (is_horizontal == True):
            des_x_pos = (goal_pos[0] - length + 1) % state.board_size[1]
            if (car_pos[1] == goal_pos[1]) and (des_x_pos == car_pos[0]):
                return True
        return False
    
    goal_pos = state.goal_entrance
    orientation = state.goal_direction
    car = None
    
    for vehicle in state.vehicle_list:
        if vehicle[4] == True:
            at_goal = car_at_goal(vehicle)
            if at_goal == True:
                return True
    return False

def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
       goal_entrance is the coordinates of the entrance tile to the goal and
       goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

    NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''
    rushHrObj = rushhour('START', 0, board_size, vehicle_list, 
            goal_entrance, goal_direction)
    return rushHrObj

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''
    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):
    s0 = make_rand_init_state(nvehicles, board_size)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, rushhour_goal_fn, heur_zero)

