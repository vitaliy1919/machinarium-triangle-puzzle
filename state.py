from utils import get_bit_value, set_bit_value
import numpy as np

def create_loop(start):
    """
    Creates a loop that defines the rotation of the gear.
    In the puzzle, there are 3 gears and thus 3 loops, with 6 points in each.
    The loops are defined by the start position and the offset 
    (as the third loop has a slightly different shape, we compensate for that with the offset )
    """
    items = [start[:2]]
    row, column, offset = start
    items.append([row, column+1])
    items.append([row+1, column+2+offset])
    items.append([row+2, column+1+offset])
    items.append([row+2, column+offset])
    items.append([row+1, column+offset])
    return items


# defing lengths of each row of poitns and the start positions of the loops
lengths = [3, 4, 3, 2]
loop_starts = [[0,0,0],[0,1,0],[1,1,-1]]

# create the loops
loops = []
for start in loop_starts:
    loops.append(create_loop(start))

# bit operations on the state to access ith row and jth column
# as we deal with 16 bit numbers, but need to store 12 bits, some bits are not used
def get_value(state, i, j):
    return get_bit_value(state, i*4+j)

def set_value(state, i, j, value):
    return set_bit_value(state, i*4+j, value)


def rotate_loop(state, loop, offset):
    """
    Applies a rotation to the state using a given loop. 
    Offset defines the magnitude of the rotation. The positive offset means clockwise rotation, 
    negative offset means counter-clockwise rotation.
    """
    new_state = state
    for i in range(len(loop)):
        next_position = (i+offset) % len(loop)
        new_state = set_value(
            new_state, 
            loop[next_position][0], loop[next_position][1], 
            get_value(state, loop[i][0], loop[i][1]))
    return new_state

def convert_12bit_to_16bit(state):
    """
    A helper function to convert the 12 bit state number to a prober 16 bit state.
    It is used when we generate all prosible states, as it's easier just to go through all numbers 
    until 2^12. After we figured out all the possible states, we convert them to 16 bit numbers.
    See `calculate_all_puzzles.py` for more details.
    """
    final_state = np.uint16(0)
    current_used = 0
    for i in range(len(lengths)):
        for j in range(lengths[i]):
            final_state = set_value(final_state,i, j, get_bit_value(state, current_used))
            current_used += 1
    return final_state

def check_state_finished(state):
    """
    Check if the current state is already completed, i.e. all the triangle points are green.
    """
    positions = [[0,1],[1,1],[1,2],[2,0],[2,1],[2,2]]
    for i in range(len(positions)):
        if get_value(state, positions[i][0], positions[i][1]) == 0:
            return False
    return True

def print_state(state, file=None):
    """
    Prints the state to the console or to a file for the better visualization.
    """
    for i in range(len(lengths)):
        if i == 0 or i == 2:
            print(" ", end="", file=file)
        if i == 3:
            print("  ", end="", file=file)
        for j in range(lengths[i]):
            print(get_value(state, i, j), end=" ", file=file)
        print(file=file)
        
class BoardState:
    """
    A helper class to perform main operations on the state in an OOP way.
    """
    def __init__(self, state):
        self.state = state
    
    def rotate(self, loop, offset):
        self.state = rotate_loop(self.state, loops[loop], offset)
    
    def get_value(self, i, j):
        return get_value(self.state, i, j)
    
    def set_value(self, i, j, value):
        self.state = set_value(self.state, i, j, value)

    def is_finished(self):
        return check_state_finished(self.state)