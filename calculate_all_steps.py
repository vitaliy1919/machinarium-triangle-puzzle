from state import *
from utils import get_bit_value, set_bit_value
def calculate_all_steps_dijkstra():
    possible_states = []
    solved_state = 0
    for i in range(2**12):
        count = 0
        for j in range(12):
            if get_bit_value(i, j) == 1:
                count += 1
        if count == 6:
            cur_state = convert_12bit_to_16bit(i)
            possible_states.append(cur_state)
            if check_state_finished(cur_state):
                solved_state = cur_state
                # print_state(solved_state)

    edges = {}
    for state in possible_states:
        edges[state] = []
        for i in range(len(loops)):
            for offset in range(1, len(loops[i])):
                new_state = rotate_loop(state, loops[i], offset)
                edges[state].append((new_state, (i, offset)))

calculate_all_steps_dijkstra()
