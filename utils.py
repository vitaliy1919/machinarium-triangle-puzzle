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

def get_color(state):
    if state == 0:
        return "red"
    else:
        return "green"

def calculate_position(pos, i, j, distance, offsets):
    x = pos[0]+j*distance
    y = pos[1]+i*distance
    x += offsets[i]
    return x, y

def calculate_position_center(pos, i, j, diameter, distance, offsets):
    x, y = calculate_position(pos, i, j, distance, offsets)
    return x + diameter/2, y + diameter/2

def draw_point(canvas, pos, diameter, color):
    return canvas.create_oval(pos[0], pos[1], pos[0]+diameter, pos[1]+diameter, fill=color)

def draw_line(canvas, pos1, pos2, width, color):
    return canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], width=width, fill=color)

def draw_line_points(canvas, pos, coord1,coord2, diameter, distance, offsets, width, color):
    i1,j1 = coord1
    i2,j2 = coord2
    x1, y1 = calculate_position_center(pos, i1, j1, diameter, distance, offsets)
    x2, y2 = calculate_position_center(pos, i2, j2, diameter, distance, offsets)
    return draw_line(canvas, [x1, y1], [x2, y2], width, color)
