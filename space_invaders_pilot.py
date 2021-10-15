from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
import psychopy.tools.coordinatetools as ct
import numpy as np
import pandas as pd
from sympy.polys.polyfuncs import interpolate
from utilities import visang
import copy


monitors_ = {
    "office": [1920, 1080, 52.70, 29.64, 56]
}

which_monitor = "office"
mon = monitors.Monitor("default")
w_px, h_px, w_cm, h_cm, d_cm = monitors_[which_monitor]
mon.setWidth(w_cm)
mon.setDistance(d_cm)
mon.setSizePix((w_px, h_px))

va = visang.VisualAngle(w_px, h_px, w_cm, h_cm, d_cm)

win = visual.Window(
    [w_px, h_px],
    monitor=mon,
    units="deg",
    color="#808080",
    fullscr=True,
    allowGUI=False,
    winType="pyglet"
)

ms = event.Mouse(
    win
)

win.mouseVisible = False

# main settings 



# white bounds
line_offset = 11

line_left = visual.Line(
    win,
    [-line_offset, -line_offset],
    [-line_offset, line_offset],
    lineWidth=2,
    lineColor="white",
    units="deg"
)

line_right = visual.Line(
    win,
    [line_offset, -line_offset],
    [line_offset, line_offset],
    lineWidth=2,
    lineColor="white",
    units="deg"
)

# cursor
cursor_y_offset = -5

cursor = visual.Circle(
    win,
    radius=0.4,
    edges=40,
    units="deg",
    fillColor="red",
    lineWidth=None,
    pos=(0, cursor_y_offset),
    opacity=.5,
    interpolate=True
)

# zig zag object place holder
zigzag = visual.ShapeStim(
    win,
    units="deg",
    vertices=[[0, 0], [-1, -1]],
    closeShape=True,
    pos=[0,0],
    interpolate=True,
    lineWidth=2,
    color="black"
)

# text stim
score_stim = visual.TextBox(
    window=win,
    text="score",
    font_size=18,
    units="deg",
    size=(2,2),
    font_color=[-1,-1,-1],
    pos=(-18, 10)
)

# zig zag settings
# key - name: [length (in va), zigzag left right offset, offset from the centre,
# speed multiplier]
settings = {
    "fast": [70, 6, 12, 2],
    "slow": [340, 6, 12, 1]
}
zig_lr_off = 6 # side to side swing
zig_st_off = 12 # starting point offset
zig_dist = 2 # distance between points
# zigzag generation
zigzag_dict = dict()
zz_off = 0.2

for i in settings.keys():
    
    zz_len, lr_off, btm_off, speed = settings[i]
    y = np.arange(zig_st_off, zz_len + zig_st_off, zig_dist)
    x = np.tile([-zig_lr_off, -zig_lr_off, zig_lr_off, zig_lr_off], int(y.shape[0]/2))
    zz_off_m = np.tile([zz_off, -zz_off, -zz_off, zz_off], int(y.shape[0]/2))
    y_off = copy.copy(y)
    y_off = y_off
    x_off = copy.copy(x)
    x_off = x_off
    zigzag_dict[i] = np.array(list(zip(x,y)))

number = 0
pos = 0
overlap = False

for cond_key in zigzag_dict.keys():

    # set up the zig zag lead in and lead out line
    vertices = zigzag_dict[cond_key]
    start_st = np.array(
        [[0, (vertices[0, 1] - zig_st_off)],
        [0, vertices[0, 1] - zig_dist]]
    )
    end_st = np.array(
        [[0, vertices[-1, 1] + zig_dist],
        [0, (vertices[-1, 1] + zig_st_off)]]
    )
    vertices = np.vstack([start_st, vertices, end_st])
    vertices_offset = np.flip(copy.copy(vertices), axis=0)
    vertices_offset[:, 1] = vertices_offset[:, 1] + 0.7
    zigzag.vertices = np.vstack([vertices, vertices_offset])
    zigzag.setPos((0, 0))
    speed = 0.2
    cur_radius = 0.4
    while (vertices[-1,1] - zigzag.pos[1]*va.pixDeg()) > cursor_y_offset:
        # GETTING THE MOUSE POSITION
        x, y = ms.getPos()
        if np.abs(x) <= 10:
            pos = x
        elif x <= -10:
            pos = -10
        elif x >= 10:
            pos = 10

        # speed
        if event.getKeys(keyList=["up"], timeStamped=False):
            speed += 0.05
        if event.getKeys(keyList=["down"], timeStamped=False):
            speed -= 0.05

        # cursor diameter
        if event.getKeys(keyList=["left"], timeStamped=False):
            cur_radius += 0.05
        if event.getKeys(keyList=["right"], timeStamped=False):
            cur_radius -= 0.05

        # MODIFYING THE OBJECTS
        zigzag.pos -= (0, speed*va.pixDeg())
        cursor.pos = ((pos, cursor_y_offset))
        cursor.radius = cur_radius
                
        if cursor.overlaps(zigzag):
            number += 1
        #     cursor.fillColor = "green"
        # else:
        #     cursor.fillColor = "red"

        score_stim.setText("score: {}".format(number))
        
        zigzag_beg = vertices[0,1] - cursor_y_offset

        # DRAWING THE OBJECTS
        line_left.draw()
        line_right.draw()
        zigzag.draw()
        cursor.draw()
        score_stim.draw()
        win.flip()

        # ending
        zigzag_end = (vertices[-1, 1] - cursor_y_offset) + zigzag.pos[1]
        if (zigzag_end < 0) or event.getKeys(keyList=["q"], timeStamped=False):
            break

        # escape from the experiment
        if event.getKeys(keyList=["escape"], timeStamped=False):
            win.close()
            core.quit()


win.close()
core.quit()
