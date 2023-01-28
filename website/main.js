
function isMobile() {
    let check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
};

const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

let canvas_ratio = 0.2;
console.log(window.innerWidth, window.innerHeight)
if (window.innerWidth < window.innerHeight) {
    canvas_ratio = 0.9;
}

const pos = [10,10];

const width = canvas.width = canvas_ratio*window.innerWidth;

distance = (width - pos[0]) / 3.5  
console.log(distance)
diameter = 0.4 * distance
ctx.font = "48px serif";

const metrics  = ctx.measureText("3");
let fontHeight = metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent;
let actualHeight = metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent;
const height = canvas.height = pos[1]+3.5*distance + actualHeight;

const loop_starts = [[0,0,0],[0,1,0],[1,1,-1]];
const lengths = [3, 4, 3, 2];



function calculate_position(pos, i, j, distance, offsets) {
    x = pos[0]+j*distance;
    y = pos[1]+i*distance;
    x += offsets[i];
    return [x, y];
}

function calculate_position_center(pos, i, j, diameter, distance, offsets) {
    const [x, y] = calculate_position(pos, i, j, distance, offsets);
    return [x + diameter/2, y + diameter/2];
}


function draw_line(canvas, pos1, pos2, width, color) {
    // const cur_width = canvas.lineWidth
    // const cur_style = canvas.strokeStyle
    canvas.lineWidth = width;
    canvas.strokeStyle = color
    ctx.beginPath();
    ctx.moveTo(pos1[0], pos1[1]);
    ctx.lineTo(pos2[0], pos2[1]);
    ctx.stroke();
    
    // return canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], width=width, fill=color)

}

function draw_line_points(canvas, pos, coord1,coord2, diameter, distance, offsets, width, color) {
    const [i1,j1] = coord1;
    const [i2,j2] = coord2;
    const [x1, y1] = calculate_position_center(pos, i1, j1, diameter, distance, offsets);
    const [x2, y2] = calculate_position_center(pos, i2, j2, diameter, distance, offsets);
    return draw_line(canvas, [x1, y1], [x2, y2], width, color);
}

function draw_point(context, pos, diameter, color) {
    
    context.beginPath();
    context.arc(pos[0], pos[1], diameter / 2, 0, 2 * Math.PI, false);
    context.fillStyle = color;
    context.fill();
    context.lineWidth = 2
    context.stroke();

    // return canvas.create_oval(pos[0], pos[1], pos[0]+diameter, pos[1]+diameter, fill=color)
}

function draw_circle(context, pos, diameter, color) {
    
    context.beginPath();
    context.arc(pos[0], pos[1], diameter / 2, 0, 2 * Math.PI, false);
    // context.fillStyle = color;
    // context.fill();
    context.lineWidth = 2
    context.stroke();

    // return canvas.create_oval(pos[0], pos[1], pos[0]+diameter, pos[1]+diameter, fill=color)
}


function createLoop(start) {
    let items = [];
    const [row, column, offset] = start;
    items.push(start.slice(0, 2));
    items.push([row, column+1]);
    items.push([row+1, column+2+offset]);
    items.push([row+2, column+1+offset]);
    items.push([row+2, column+offset]);
    items.push([row+1, column+offset]);
    return items;
}

// function drawCircle(pos, diameter)
// const distance = 100;
// const diameter = 60;
const offsets = [distance/2, 0, distance/2, distance];
let loops = [];

for (start of loop_starts) {
    console.log(start);
    loops.push(createLoop(start));
}
console.log(loops[0]);

let state = new Uint16Array(1);

function get_bit_value(number, bit) {
    return (number >> bit) & 1;
}


function set_bit_value(number, bit, value) {
    if (value == 1)
        return number | (1 << bit);
    else
        return number & ~(1 << bit);
}

function get_value(state, i, j) {
    return get_bit_value(state, i*4+j);
}

function set_value(state, i, j, value) {
    return set_bit_value(state, i*4+j, value);
}

function get_color(state) {
    if (state == 0) {
        return "red";
    } else {
        return "green";
    }
}
// console.log(state[0])
// state[0] = set_bit_value(state[0],1, 1)
// console.log(state[0])

const loop_center = [[1,1],[1,2], [2,1]]
const colors = ["DarkBlue", "DarkOliveGreen", "DarkGoldenRod"]
let result_label = document.getElementById("result");
function redraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (loop of loops) {
        for (let i = 0; i < loop.length; i++) {
            draw_line_points(ctx, pos, loop[i],  loop[(i+1)%loop.length], diameter, distance, offsets, 2, "black");
        }
    }
    // for (start of loop_center) {
    //     const center = calculate_position_center(pos, start[0], start[1], diameter, distance, offsets)
    //     draw_circle(ctx, center, distance*2, "black")
    // }
    
    for (let i = 0; i <lengths.length; i++) {
        for (let j = 0; j < lengths[i]; j++) {
            color = get_color(get_value(state[0], i, j))

            const [x, y] = calculate_position_center(pos, i, j, diameter, distance, offsets);
            draw_point(ctx, [x, y], diameter, color);
        }
    }
    ctx.font = "48px serif";
    ctx.fillStyle = colors[0];
    ctx.fillText("1", pos[0] + distance / 6, pos[1] + distance / 1.5);
    ctx.fillStyle = colors[1];

    ctx.fillText("2", pos[0] + distance / 6 + 3*distance, pos[1] + distance / 1.5);

    ctx.fillStyle = colors[2];

    ctx.fillText("3", pos[0] + 1.6 * distance, pos[1] + distance / 1.5 + 3*distance);


}

redraw();

canvas.addEventListener('click', function(event) {
    const rect = canvas.getBoundingClientRect()
    var click_x = event.clientX - rect.left,
        click_y = event.clientY - rect.top;
    console.log(x, y);
    
    for (let i = 0; i < lengths.length; i++) {
        for (let j = 0; j < lengths[i]; j++) {
          let [x, y] = calculate_position_center(pos, i, j, diameter, distance, offsets);
          const cur_distance = Math.sqrt((click_x-x)**2 + (click_y-y)**2)
          if (cur_distance < diameter/2) {
            console.log("match")
            let old_value = get_value(state[0], i, j);
            let new_value = 1 - old_value;
            state[0] = set_value(state[0], i, j, new_value);
            redraw();
            break
          }
        }
      }
    // Collision detection between clicked offset and element.
    

}, false);
solutions = JSON.parse(moves);
console.log(solutions);
document.getElementById("solve").onclick = function() {
    count = 0
    for (let j = 0; j < 16; j++) {
        if (get_bit_value(state[0], j) == 1)
            count += 1
    }
    if (count != 6){
        result_label.innerHTML = `6 dots needs to be green.<br>Currently green: ${count}`;
        return
    }

    description = "";
    const moves = solutions[state[0]];
    if (moves.length == 0) {
        description = "The puzzle is already solved.";
    }
    for (let move of moves) {

        gear_number = move[0]+1;
        gear_with_color = "<span style='color:" + colors[move[0]] + "'>" + gear_number + "</span>";
        description += "Gear " + gear_with_color + " ";
        if (move[1] > 3) {
            description += "↶ counter-clockwise " + (6-move[1]) + " ";
            if (6-move[1] == 1) {
                description += "time";
            } else {
                description += "times";
            }
        } else {
            description += "↷ clockwise " + (move[1]) + " ";
            if (move[1] == 1) {
                description += "time";
            } else {
                description += "times";
            }
        }
        description += "<br>";
    }
    result_label.innerHTML = description;

    console.log(solutions[state[0]]);
}