import tkinter 
import tkinter as tk
import numpy as np
import math
from functools import partial
from state import *
from utils import *
# init tk
root = tkinter.Tk() 
root.title("Machinarium Traingle Puzzle Solver")
frame = tk.Frame(root)

# root.attributes('-topmost', True)
# root.update()

# create canvas
# canvas = tkinter.Canvas(root, bg="white", height=600, width=600)
canvas = tkinter.Canvas(frame, bg="white")
pos = 50, 50
diameter = 20
distance = 50
offsets = [distance/2, 0, distance/2, distance]

state = BoardState(np.uint16(0))




points = []
for loop in loops:
    for i in range(len(loop)):
        # if i == len(loop)-1:
        draw_line_points(canvas, pos, loop[i],  loop[(i+1)%len(loop)], diameter, distance, offsets, 2, "black")

for i in range(len(lengths)):
    cur_points = []
    for j in range(lengths[i]):
        color = get_color(state.get_value(i, j))
        
        x, y = calculate_position(pos, i, j, distance, offsets)
        cur_points.append(draw_point(canvas, [x, y], diameter, color))
    points.append(cur_points)
        # canv.create_oval(, pos[0]+diameter, pos[1]+diameter, fill="green")

def on_canvas_click(event):
    global state
    for i in range(len(lengths)):
        for j in range(lengths[i]):
            x, y = calculate_position_center(pos, i, j, diameter, distance, offsets)
            if math.dist((x,y), (event.x, event.y)) < diameter/2:
                old_value = state.get_value(i, j)
                new_value = 1-old_value
                state.set_value(i, j, new_value)

                canvas.itemconfig(points[i][j], fill=get_color(new_value))
                break


def on_rotate_button_press(loop_number, direction):
    # print(loop_number, direction)
    global state
    state.rotate(loop_number, direction)
    for point in loops[loop_number]:
        i, j = point
        canvas.itemconfig(points[i][j], fill=get_color(state.get_value(i, j)))



class State:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.move = move
        self.parent = parent

    
# def find_solution_for_state(state, solutions):
#     used_states = set()


#     used_states.add(state)
#     if check_state_finished(state):
#         if state not in solutions:
#             solutions[state] = []
#         return
#     queue = [State(state)]
#     while len(queue) > 0:
#         cur_state = queue.pop(0)

#         for i in range(len(loops)):
#             for offset in range(1, len(loops[i])):
#                 new_state = rotate_loop(cur_state.state, loops[i], offset)

#                 cur_move = (i, offset)
#                 new_state = State(new_state, cur_move, cur_state)
                
#                 if new_state.state in solutions or check_state_finished(new_state.state):

#                     # no_sol = solutions.get(new_state.state, []) is None
                        
#                     cur_state = new_state
#                     if new_state.state in solutions:
#                         moves = solutions[new_state.state]
#                     else:
#                         moves = []
#                     while cur_state != None:
#                         if cur_state.state not in solutions:
#                             solutions[cur_state.state] = moves.copy()
#                         if cur_state.move != None:
#                             moves.append(cur_state.move)
                        
#                         cur_state = cur_state.parent
#                     return

#                 if new_state in used_states:
#                     continue
#                 used_states.add(new_state)
                
                
#                 queue.append(new_state)
#     print("no solution for state", print_state(state))
#     solutions[state] = None


# # print("test state", test_state_16)
# def solve_all_puzzles():
#     possible_states = []
#     solutions = {}
#     for i in range(2**12):
#         count = 0
#         for j in range(12):
#             if get_bit_value(i, j) == 1:
#                 count += 1
#         if count == 6:
#             possible_states.append(convert_12bit_to_16bit(i))

    

#     for state in possible_states:
#         find_solution_for_state(state, solutions)
#     f = open("solutions.txt", "w")
#     print(len(solutions))
#     max_len = 0
#     for key in solutions:
#         for i in range(len(lengths)):
#             if i == 0 or i == 2:
#                 f.write(" ")
#             if i == 3:
#                 f.write("  ")
#             for j in range(lengths[i]):
#                 f.write(str(get_value(key, i, j))+" ")
#             f.write("\n")
#         f.write(str(solutions[key])+"\n")
#         cur_len = len(solutions[key])
#         if cur_len > max_len:
#             max_len = cur_len
#     print(max_len)
#     f.close()

                    



def solve_puzzle(lable):
    used_states = set()
    count = 0
    for j in range(16):
        if get_bit_value(state.state, j) == 1:
            count += 1
    if count != 6:
        lable.config(text=f"6 dots needs to be green.\nCurrently green: {count}")

        return
    used_states.add(state)
    if state.is_finished():
        lable.config(text="Already solved")
        return
    queue = [(state.state,[])]
    
    while len(queue) > 0:
        cur_state, moves = queue.pop(0)

        for i in range(len(loops)):
            for offset in range(len(loops[i])):
                new_state = rotate_loop(cur_state, loops[i], offset)
                # print("change", i, offset)
                # print_state(new_state)

                if new_state in used_states:
                    continue
                used_states.add(new_state)
                new_moves = moves.copy()
                new_moves.append((i, offset))
                queue.append((new_state, new_moves))

                if check_state_finished(new_state):
                    description = ""
                    for move in new_moves:
                        description += f"gear {move[0]+1} "
                        if move[1] > 3:
                            description += f"↶ counter-clockwise {6-move[1]} "
                            if 6-move[1] == 1:
                                description += "time"
                            else:
                                description += "times"
                        else:
                            description += f"↷ clockwise {move[1]} "
                            if move[1] == 1:
                                description += "time"
                            else:
                                description += "times"
                        description +="\n"
                    lable.config(text=description)
                    print("solution found")
                    print(new_moves)
                    return

                
    lable.config(text="No solution found")
    print("no solution found")
    return


# draw arcs
python_green = "#476042"
coord = 10, 10, 300, 300
left = "🡰"
right = "🡲"

buttons = []
for i in range(3):
    cur_buttons = [
        tk.Button(canvas, text=left ,command=partial(on_rotate_button_press, loop_number=i,direction=-1)), 
        tk.Button(canvas, text=right,command=partial(on_rotate_button_press, loop_number=i,direction=+1))]
    buttons.append(cur_buttons)
buttons_pos = [
    [pos[0]+distance/2, 10],
    [pos[0]+5*distance/2, 10],
    [pos[0]+7/4*distance, 10+9/2*distance]
]
for i,button_pos in enumerate(buttons_pos):
    canvas.create_window(button_pos[0], button_pos[1], anchor=tk.NW, window=buttons[i][1])
    canvas.create_window(button_pos[0], button_pos[1], anchor=tk.NE, window=buttons[i][0])

# canva

answer_label = tk.Label(frame, text="", font=(None, 15), justify=tk.LEFT)
canvas.create_window(pos[0]+0.5*distance, pos[1]+4.5*distance, anchor=tk.NW, window=answer_label)

solve_button = tk.Button(canvas, text="Solve", command=partial(solve_puzzle, answer_label))

canvas.create_window(pos[0]+4*distance, pos[1]+3*distance/2, anchor=tk.W, window=solve_button)

canvas.create_text( pos[0] + distance / 6, pos[1] + distance / 2, text="1", font=(None, 15))
canvas.create_text( pos[0] + distance / 6 + 3*distance, pos[1] + distance / 2, text="2", font=(None, 15))
canvas.create_text( pos[0] + 1.7 * distance, pos[1] + distance / 2 + 2.9*distance, text="3", font=(None, 15))

# arc = myCanvas.create_arc(coord, start=0, extent=150, fill="red")
# arv2 = myCanvas.create_arc(coord, start=150, extent=215, fill="green")
# possible = 0
# for i in range(2**12):
#     count = 0
#     for j in range(12):
#         if get_bit_value(i, j) == 1:
#             count += 1
#     if count == 6:
#         possible += 1
# print("possible", possible)

# positions 
# for 

# canv.create_oval(pos[0], pos[1], pos[0]+diameter, pos[1]+diameter, fill=python_green)
# canv.create_oval(pos[0], pos[1], pos[0]+diameter, pos[1]+diameter, fill="red")

# add to window and show
# answer_label.config(text="1\n1\n1\n1\n1\n")
answer_label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", on_canvas_click)
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()