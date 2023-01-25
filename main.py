import tkinter 
import tkinter as tk
import numpy as np
import math
from functools import partial
# init tk
root = tkinter.Tk()

# create canvas
canv = tkinter.Canvas(root, bg="white", height=600, width=600)
pos = 50, 50
diameter = 20
distance = 50
offsets = [distance/2, 0, distance/2, distance]
def get_color(state):
    if state == 0:
        return "red"
    else:
        return "green"
def get_bit_value(number, bit):
    return (number >> bit) & 1

def set_bit_value(number, bit, value):
    if value == 1:
        return number | (1 << bit)
    else:
        return number & ~(1 << bit)

def get_value(state, i, j):
    return get_bit_value(state, i*4+j)

def set_value(state, i, j, value):
    return set_bit_value(state, i*4+j, value)

def calculate_position(i, j, distance, offsets):
    x = pos[0]+j*distance
    y = pos[1]+i*distance
    x += offsets[i]
    return x, y

def calculate_position_center(i, j, distance, offsets):
    x, y = calculate_position(i, j, distance, offsets)
    return x + diameter/2, y + diameter/2

def draw_point(pos, diameter, color):
    return canv.create_oval(pos[0], pos[1], pos[0]+diameter, pos[1]+diameter, fill=color)

def draw_line(pos1, pos2, width, color):
    return canv.create_line(pos1[0], pos1[1], pos2[0], pos2[1], width=width, fill=color)

def draw_line_points(coord1,coord2, distance, offsets, width, color):
    i1,j1 = coord1
    i2,j2 = coord2
    x1, y1 = calculate_position_center(i1, j1, distance, offsets)
    x2, y2 = calculate_position_center(i2, j2, distance, offsets)
    return draw_line([x1, y1], [x2, y2], width, color)

state = np.uint16(0)
lengths = [3, 4, 3, 2]
# for i in range(4):
#     for j in range(8):
#         print(get_bit_value(numbers[i], j), end=" ")
#     print()



def create_loop(start):
    items = [start[:2]]
    row, column, offset = start
    items.append([row, column+1])
    items.append([row+1, column+2+offset])
    items.append([row+2, column+1+offset])
    items.append([row+2, column+offset])
    items.append([row+1, column+offset])
    return items

def rotate_loop(state, loop, offset):
    new_state = state
    for i in range(len(loop)):
        next_position = (i+offset) % len(loop)
        new_state = set_value(
            new_state, 
            loop[next_position][0], loop[next_position][1], 
            get_value(state, loop[i][0], loop[i][1]))
    return new_state

def rotate_button_press(loop_number, direction):
    # print(loop_number, direction)
    global state
    new_state = rotate_loop(state, loops[loop_number], direction)
    for point in loops[loop_number]:
        i, j = point
        canv.itemconfig(points[i][j], fill=get_color(get_value(new_state, i, j)))
    state = new_state

loop_starts = [[0,0,0],[0,1,0],[1,1,-1]]

loops = []
for start in loop_starts:
    loops.append(create_loop(start))
    print(loops[-1])

points = []
for loop in loops:
    for i in range(len(loop)):
        if i == len(loop)-1:
            draw_line_points(loop[i],  loop[0], distance, offsets, 2, "black")
        else:
            draw_line_points(loop[i],  loop[i+1], distance, offsets, 2, "black")

for i in range(len(lengths)):
    cur_points = []
    for j in range(lengths[i]):
        color = get_color(get_value(state, i, j))
        
        x, y = calculate_position(i, j, distance, offsets)
        cur_points.append(draw_point([x, y], diameter, color))
    points.append(cur_points)
        # canv.create_oval(, pos[0]+diameter, pos[1]+diameter, fill="green")

def callback(event):
    global state
    print(distance, offsets)
    for i in range(len(lengths)):
        for j in range(lengths[i]):
            x, y = calculate_position_center(i, j, distance, offsets)
            if math.dist((x,y), (event.x, event.y)) < diameter/2:
                old_value = get_value(state, i, j)
                new_value = 1-old_value
                state = set_value(state, i, j, new_value)
                print(state)
                # for i in range(4):
                #     for j in range(8):
                #         print(get_bit_value(numbers[i], j), end=" ")
                #     print()
                canv.itemconfig(points[i][j], fill=get_color(new_value))
                break
                # x, y = calculate_position(i, j, distance, offsets)

                # draw_point([x, y], diameter, "green" if new_value == 1 else "red")
                # print("clicked at rel", i, j)
    print("clicked at", event.x, event.y)
        
# draw arcs
python_green = "#476042"
coord = 10, 10, 300, 300
left = "🡰"
right = "🡲"

buttons = []
for i in range(3):
    cur_buttons = [
        tk.Button(canv, text=left ,command=partial(rotate_button_press, loop_number=i,direction=-1)), 
        tk.Button(canv, text=right,command=partial(rotate_button_press, loop_number=i,direction=+1))]
    buttons.append(cur_buttons)
buttons_pos = [
    [pos[0]+distance/2, 10],
    [pos[0]+5*distance/2, 10],
    [pos[0]+7/4*distance, 10+9/2*distance]
]
for i,button_pos in enumerate(buttons_pos):
    canv.create_window(button_pos[0], button_pos[1], anchor=tk.NW, window=buttons[i][1])
    canv.create_window(button_pos[0], button_pos[1], anchor=tk.NE, window=buttons[i][0])


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
canv.bind("<Button-1>", callback)
canv.pack()
root.mainloop()