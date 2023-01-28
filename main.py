"""
Main app for solving the triangle puzzle from Machinarium
"""

import tkinter 
import tkinter as tk
import numpy as np
import math
from functools import partial
from state import *
from utils import *

root = tkinter.Tk() 
root.title("Machinarium Triangle Puzzle Solver")
frame = tk.Frame(root)

canvas = tkinter.Canvas(frame, bg="white")

pos = 50, 50
diameter = 20
distance = 50
offsets = [distance/2, 0, distance/2, distance]

# as we only have 12 points, we can use 16 bit integer to store the state
# this is quite efficient as we can use bitwise operations to rotate the state
# and it uses less memory which is helpful when we create a graph to solve the puzzle
state = BoardState(np.uint16(0))

# drawing lines that are connecting the points
points = []
for loop in loops:
    for i in range(len(loop)):
        draw_line_points(canvas, pos, loop[i],  loop[(i+1)%len(loop)], diameter, distance, offsets, 2, "black")

# drawing points
for i in range(len(lengths)):
    cur_points = []
    for j in range(lengths[i]):
        color = get_color(state.get_value(i, j))
        
        x, y = calculate_position(pos, i, j, distance, offsets)
        cur_points.append(draw_point(canvas, [x, y], diameter, color))
    points.append(cur_points)


# update colors by clicking on the points
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


# apply rotations presses to the state
def on_rotate_button_press(loop_number, direction):
    global state
    state.rotate(loop_number, direction)
    for point in loops[loop_number]:
        i, j = point
        canvas.itemconfig(points[i][j], fill=get_color(state.get_value(i, j)))


    
# solve a current state with a BFS
def solve_puzzle(lable):
    used_states = set()

    # give a warning if the state is not valid
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
    
    # regular BFS 
    while len(queue) > 0:
        cur_state, moves = queue.pop(0)

        for i in range(len(loops)):
            # we are only going clockwise, because it is equvalent
            # rotating clockwise by 4 is the same as rotating counter-clockwise by 1
            for offset in range(1, len(loops[i])):
                new_state = rotate_loop(cur_state, loops[i], offset)

                if new_state in used_states:
                    continue
                used_states.add(new_state)
                new_moves = moves.copy()
                new_moves.append((i, offset))
                queue.append((new_state, new_moves))

                # if we reached a solved state, print the solution
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
                    return

    lable.config(text="No solution found")
    return


# create buttons to rotate the gears 
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


# label to show the solution
answer_label = tk.Label(frame, text="", font=(None, 15), justify=tk.LEFT)
canvas.create_window(pos[0]+0.5*distance, pos[1]+4.5*distance, anchor=tk.NW, window=answer_label)


solve_button = tk.Button(canvas, text="Solve", command=partial(solve_puzzle, answer_label))

canvas.create_window(pos[0]+4*distance, pos[1]+3*distance/2, anchor=tk.W, window=solve_button)

canvas.create_text( pos[0] + distance / 6, pos[1] + distance / 2, text="1", font=(None, 15))
canvas.create_text( pos[0] + distance / 6 + 3*distance, pos[1] + distance / 2, text="2", font=(None, 15))
canvas.create_text( pos[0] + 1.7 * distance, pos[1] + distance / 2 + 2.9*distance, text="3", font=(None, 15))

answer_label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", on_canvas_click)
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()