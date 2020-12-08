# ################ A simple graphical interface which communicates with the server #####################################

# This file  also takes input from the webcam, pick colours manually or randomize and solve it.

from tkinter import *
import face
import cubie
import solver
import vision_params
from vision import grab_colors

# ################################## some global variables and constants ###############################################
width = 60  # width of a facelet in pixels
facelet_id = [[[0 for col in range(3)] for row in range(3)] for fc in range(6)]
colorpick_id = [0 for i in range(6)]
curcol = None
t = ("U", "R", "F", "D", "L", "B")
cols = ("yellow", "green", "red", "white", "blue", "orange")
# ############################## Start the opencv color grabber and the GUI #############################

from threading import Thread
background_thread = Thread(args=(8080, 20, 2))
background_thread.start()
# Server listens now on port 8080, maxlength 20 moves, timeout 2 seconds

thr = Thread(target=grab_colors, args=())
thr.start()
# Run the opencv code and detect facelet colors
########################################################################################################################

# ################################################ Diverse functions ###################################################


def show_text(txt):
    """Display messages."""
    print(txt)
    display.insert(INSERT, txt)
    root.update_idletasks()


def create_facelet_rects(a):
    """Initialize the facelet grid on the canvas."""
    offset = ((1, 0), (2, 1), (1, 1), (1, 2), (0, 1), (3, 1))
    for f in range(6):
        for row in range(3):
            y = 10 + offset[f][1] * 3 * a + row * a
            for col in range(3):
                x = 10 + offset[f][0] * 3 * a + col * a
                facelet_id[f][row][col] = canvas.create_rectangle(x, y, x + a, y + a, fill="grey")
                if row == 1 and col == 1:
                    canvas.create_text(x + width // 2, y + width // 2, font=("", 14), text=t[f], state=DISABLED)
    for f in range(6):
        canvas.itemconfig(facelet_id[f][1][1], fill=cols[f])


def create_colorpick_rects(a):
    """Initialize the "paintbox" on the canvas."""
    global curcol
    global cols
    for i in range(6):
        x = (i % 3) * (a + 5) + 7 * a
        y = (i // 3) * (a + 5) + 7 * a
        colorpick_id[i] = canvas.create_rectangle(x, y, x + a, y + a, fill=cols[i])
        canvas.itemconfig(colorpick_id[0], width=4)
        curcol = cols[0]


def get_definition_string():
    """Generate the cube definition string from the facelet colors."""
    color_to_facelet = {}
    for i in range(6):
        color_to_facelet.update({canvas.itemcget(facelet_id[i][1][1], "fill"): t[i]})
    s = ''
    for f in range(6):
        for row in range(3):
            for col in range(3):
                s += color_to_facelet[canvas.itemcget(facelet_id[f][row][col], "fill")]
    return s


########################################################################################################################

# ############################### Solve the displayed cube with a local or remote server ###############################


def solve():
    """Connect to the server and return the solving maneuver."""
    display.delete(1.0, END)  # clear output window
    try:
        defstr = get_definition_string()
    except:
        show_text('Invalid facelet configuration.\nWrong or missing colors.')
        return
    show_text(defstr + '\n')
    show_text('\n')
    show_text(solver.solve(defstr, 20, 2))


########################################################################################################################

# ################################# Functions to change the facelet colors #############################################


def clean():
    """Restore the cube to a clean cube."""
    for f in range(6):
        for row in range(3):
            for col in range(3):
                canvas.itemconfig(facelet_id[f][row][col], fill=canvas.itemcget(facelet_id[f][1][1], "fill"))


def empty():
    """Remove the facelet colors except the center facelets colors."""
    for f in range(6):
        for row in range(3):
            for col in range(3):
                if row != 1 or col != 1:
                    canvas.itemconfig(facelet_id[f][row][col], fill="grey")


def random():
    """Generate a random cube and sets the corresponding facelet colors."""
    cc = cubie.CubieCube()
    cc.randomize()
    fc = cc.to_facelet_cube()
    idx = 0
    for f in range(6):
        for row in range(3):
            for col in range(3):
                canvas.itemconfig(facelet_id[f][row][col], fill=cols[fc.f[idx]])
                idx += 1


########################################################################################################################

# ################################### Edit the facelet colors ##########################################################


def click(event):
    """Define how to react on left mouse clicks"""
    global curcol
    idlist = canvas.find_withtag("current")
    if len(idlist) > 0:
        if idlist[0] in colorpick_id:
            curcol = canvas.itemcget("current", "fill")
            for i in range(6):
                canvas.itemconfig(colorpick_id[i], width=1)
            canvas.itemconfig("current", width=5)
        else:
            canvas.itemconfig("current", fill=curcol)


########################################################################################################################

def transfer():
    """Transfer the facelet colors detected by the opencv vision to the GUI editor."""
    if len(vision_params.face_col) == 0:
        return
    centercol = vision_params.face_col[1][1]

    vision_params.cube_col[centercol] = vision_params.face_col
    vision_params.cube_hsv[centercol] = vision_params.face_hsv

    dc = {}
    for i in range(6):
        dc[canvas.itemcget(facelet_id[i][1][1], "fill")] = i  # map color to face number
    for i in range(3):
        for j in range(3):
            canvas.itemconfig(facelet_id[dc[centercol]][i][j], fill=vision_params.face_col[i][j])

# ######################################################################################################################

#  ###################################### Generate and display the TK_widgets ##########################################

root = Tk()
root.wm_title("3 x 3 x 3 Rubik's cube solver")
canvas = Canvas(root, width=12 * width + 20, height=9 * width + 20)
canvas.pack()
bsolve = Button(text="Solve", height=2, width=10, relief=RAISED, command=solve)
bsolve_window = canvas.create_window(10 + 0.5 * width, 10 + 6.5 * width, anchor=NW, window=bsolve)
bclean = Button(text="Clean", height=1, width=10, relief=RAISED, command=clean)
bclean_window = canvas.create_window(10 + 0.5 * width, 10 + 7.5 * width, anchor=NW, window=bclean)
bempty = Button(text="Empty", height=1, width=10, relief=RAISED, command=empty)
bempty_window = canvas.create_window(10 + 0.5 * width, 10 + 8 * width, anchor=NW, window=bempty)
brandom = Button(text="Random", height=1, width=10, relief=RAISED, command=random)
brandom_window = canvas.create_window(10 + 0.5 * width, 10 + 8.5 * width, anchor=NW, window=brandom)
display = Text(height=7, width=39)
text_window = canvas.create_window(10 + 6.5 * width, 10 + .5 * width, anchor=NW, window=display)

canvas.bind("<Button-1>", click)
create_facelet_rects(width)
create_colorpick_rects(width)

btransfer = Button(text="Capture", height=2, width=13, relief=RAISED, command=transfer)
canvas.create_window(10 + 0.5 * width, 10 + 1 * width, anchor=NW, window=btransfer)

root.mainloop()

########################################################################################################################
