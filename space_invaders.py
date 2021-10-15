from threading import Condition
from numpy.core.overrides import verify_matching_signatures
from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
import psychopy.tools.coordinatetools as ct
import numpy as np
import pandas as pd
from utilities import visang
from things import create_shape, create_zigzag
from datetime import datetime

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
    opacity=0.5,
    interpolate=True
)


# zig zag object placeholder
zigzag = visual.ShapeStim(
    win,
    units="deg",
    vertices=[[0, 0], [-1, -1]],
    closeShape=True,
    pos=[0,0],
    interpolate=True,
    lineWidth=2,
    lineColor=(255,0,0),
    colorSpace="rgb255"
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

current_stim = visual.TextBox(
    window=win,
    text="score",
    font_size=18,
    units="deg",
    size=(2,2),
    font_color=[-1,-1,-1],
    pos=(-18, 8)
)

# zigzag creation length, swing, start_point, spacing, lead, speed_multiplier,
# cursor size, thiccness

conditions = {
    "short": [120, 6, 24, 3, 6, 0.2, 0.2, 0.25],
    "long": [240, 6, 24, 3, 6, 0.6, 0.2, 0.25]
}

zigzags = {}
for i in conditions.keys():
    length, swing, start_point, spacing, lead, speed_multiplier, cursor_rad, thicc = conditions[i]
    line = create_zigzag(length, swing, start_point, spacing, lead)
    zigzags[i] = [create_shape(line, thicc), speed_multiplier, cursor_rad, line]

number = 0
pos = 0
overlap = False



for ix, zz in enumerate(["short", "long", "short", "long"]):
    vertices, speed_multiplier, cur_radius, line = zigzags[zz]
    zigzag.vertices = vertices
    zigzag.setPos((0, 0))
    data = {
        "device_x": [],
        "device_y": [],
        "cursor_pos": [],
        "time": [],
        "overlap": [],
        "speed": [],
        "cursor_size": [],
        "zigzag_pos": [],
        "shape_thicc": []
    }
    while (np.max(vertices[:,1]) - zigzag.pos[1]*va.pixDeg()) > cursor_y_offset:
        # GETTING THE MOUSE POSITION
        x, y = ms.getPos()
        if np.abs(x) <= 10:
            pos = x
        elif x <= -10:
            pos = -10
        elif x >= 10:
            pos = 10

        # # speed
        # if event.getKeys(keyList=["up"], timeStamped=False):
        #     speed_multiplier += 0.05
        # if event.getKeys(keyList=["down"], timeStamped=False):
        #     speed_multiplier -= 0.05

        # # cursor diameter
        # if event.getKeys(keyList=["left"], timeStamped=False):
        #     cur_radius += 0.05
        # if event.getKeys(keyList=["right"], timeStamped=False):
        #     cur_radius -= 0.05

        # MODIFYING THE OBJECTS
        zigzag.pos -= (0, speed_multiplier*va.pixDeg())
        cursor.pos = ((pos, cursor_y_offset))
        cursor.radius = cur_radius
                
        if cursor.overlaps(zigzag):
            number += 1
            cursor.fillColor = "green"
            cursor.opacity = 0.5
            overlap = True
        else:
            cursor.fillColor = "red"
            cursor.opacity = 0.5
            overlap = False

        score_stim.setText("score: {}".format(number))
        current_stim.setText("{}\n {}".format(x, y))

        # DRAWING THE OBJECTS
        line_left.draw()
        line_right.draw()
        zigzag.draw()
        cursor.draw()
        current_stim.draw()
        score_stim.draw()
        time = win.flip()
        
        # collecting the data
        zigzag_beg = (np.min(vertices[:,1]) - cursor_y_offset) + zigzag.pos[1]
        zigzag_end = (np.max(vertices[:,1]) - cursor_y_offset) + zigzag.pos[1]

        if zigzag_beg <= 0:
            data["device_x"].append(x)
            data["device_y"].append(y)
            data["cursor_pos"].append(pos)
            data["time"].append(time)
            data["overlap"].append(overlap)
            data["speed"].append(speed_multiplier*va.pixDeg())
            data["zigzag_pos"].append(zigzag.pos[1])
            data["cursor_size"].append(cursor.radius),
            data["shape_thicc"].append(thicc)
        
        # ending
        if (zigzag_end <= 0) or event.getKeys(keyList=["q"], timeStamped=False):
            ord = str(ix).zfill(3)
            now = datetime.now()
            tst = datetime.timestamp(now)
            data_file = "data/{}_{}_traj.csv".format(ord, tst)
            pd.DataFrame.from_dict(data).to_csv(data_file,index=False)
            vert_file = "data/{}_{}_vert.csv".format(ord, tst)
            np.save(vert_file, vertices)
            line_file = "data/{}_{}_line.csv".format(ord, tst)
            np.save(line_file, line)
            break

        # escape from the experiment
        if event.getKeys(keyList=["escape"], timeStamped=False):
            win.close()
            core.quit()


win.close()
core.quit()
