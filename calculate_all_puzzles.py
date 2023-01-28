"""
Calculated the solution to all possible puzzles using Dijkstra's algorithm.
The result is stored in the `solutions.json` file that is later used by the web app, 
so that no calculations are needed on the client side.
"""

from state import *
from utils import get_bit_value, set_bit_value
from priority_queue import PriorityQueue
import json
def calculate_all_puzzles_dijkstra():
    # calculate all possible states, i.e. all states where 6 points are green
    possible_states = []
    solved_state = 0
    for i in range(2**12):
        count = 0
        for j in range(12):
            if get_bit_value(i, j) == 1:
                count += 1
        if count == 6:
            # convert to 16 bit state
            cur_state = convert_12bit_to_16bit(i)

            possible_states.append(cur_state)
            if check_state_finished(cur_state):
                solved_state = cur_state

    # calculate all edges between states by performing all possible rotations
    # from a given state, so from each state we get 15 egdes, 5 possible rotations * 3 gears
    edges = {}
    edges_dict = {}
    for neighbor_state in possible_states:
        edges[neighbor_state] = []
        edges_dict[neighbor_state] = {}
        for i in range(len(loops)):
            for offset in range(1, len(loops[i])):
                new_state = rotate_loop(neighbor_state, loops[i], offset)
                edges[neighbor_state].append((new_state, (i, offset)))
                edges_dict[neighbor_state][new_state] = (i, offset)

    # run Dijkstra's algorithm from the solved state to calculate the shortest path to all other states
    visited = set()
    tentative_distances = PriorityQueue()
    distances = {}
    # stores a previous state in a shortest path to the source state
    # used to then restore the path
    previous_states = {}
    tentative_distances.put((0, solved_state))
    distances[solved_state] = 0
    while len(tentative_distances) > 0:
        _, cur_state = tentative_distances.pop()

        cur_distance = distances[cur_state] + 1
        for neighbor_node in edges[cur_state]:
            neighbor_state, _ = neighbor_node
            if neighbor_state not in distances:
                distances[neighbor_state] = cur_distance
                previous_states[neighbor_state] = cur_state
                tentative_distances.put((cur_distance, neighbor_state))
            elif neighbor_state not in visited and cur_distance < distances[neighbor_state]:
                distances[neighbor_state] = cur_distance
                previous_states[neighbor_state] = cur_state
                tentative_distances.update_elem(neighbor_state, cur_distance)

    # calculating the solutions, i.e. the moves from each state to the solved state
    moves = {}
    for state in possible_states:
        state = int(state)
        moves[state] = []
        cur_state = state
        while cur_state != solved_state:
            prev_state = previous_states[cur_state]
            moves[state].append(edges_dict[cur_state][prev_state])
            cur_state = prev_state

    # saving to json
    with open("solutions.json", "w") as outfile:
        json.dump(moves, outfile)

    # also save to text file for better readanility
    f = open("solutions.txt", "w")
    hard_f = open("hard.txt","w")
    i = 0
    for state, cur_moves in moves.items():
        if len(cur_moves) >= 4:
            i += 1
            print_state(state, file=hard_f)
            print(cur_moves, file=hard_f)

        print_state(state, file=f)
        print(cur_moves, file=f)
    print(i/len(moves))
    f.close()
    hard_f.close()
   

calculate_all_puzzles_dijkstra()
