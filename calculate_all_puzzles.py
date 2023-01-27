from state import *
from utils import get_bit_value, set_bit_value
from priority_queue import PriorityQueue
def calculate_all_puzzles_dijkstra():
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
    edges_dict = {}
    for neighbor_state in possible_states:
        edges[neighbor_state] = []
        edges_dict[neighbor_state] = {}
        for i in range(len(loops)):
            for offset in range(1, len(loops[i])):
                new_state = rotate_loop(neighbor_state, loops[i], offset)
                edges[neighbor_state].append((new_state, (i, offset)))
                edges_dict[neighbor_state][new_state] = (i, offset)

    visited = set()
    tentative_distances = PriorityQueue()
    distances = {}
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

    # print(distances)
    moves = {}
    for state in possible_states:
        moves[state] = []
        cur_state = state
        while cur_state != solved_state:
            prev_state = previous_states[cur_state]
            moves[state].append(edges_dict[cur_state][prev_state])
            cur_state = prev_state
    # print(moves)
    f = open("solutions.txt", "w")
    hard_f = open("hard.txt","w")
    for state, moves in moves.items():
        if len(moves) >= 4:
            print_state(state, file=hard_f)
            # print()
            print(moves, file=hard_f)

        print_state(state, file=f)
        print(moves, file=f)

    f.close()
    hard_f.close()
    # length = 0
    # for edge in edges:
    #     length += len(edges[edge])
    # print(length)

calculate_all_puzzles_dijkstra()
