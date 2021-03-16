from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
import psychopy.tools.coordinatetools as ct
import numpy as np
import pandas as pd
from utilities import visang


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

line_left = visual.Line(
    win,
    [-10, -10],
    [-10, 10],
    lineWidth=2,
    lineColor="white",
    units="deg"
)

line_right = visual.Line(
    win,
    [10, -10],
    [10, 10],
    lineWidth=2,
    lineColor="white",
    units="deg"
)

cursor = visual.Circle(
    win,
    radius=0.4,
    edges=40,
    units="deg",
    fillColor="red",
    lineColor="red",
    pos=(0, 0)
)

text_stim = visual.TextBox(
    window=win,
    text="xxx",
    font_size=18,
    units="deg",
    size=(2,2),
    font_color=[-1,-1,1],
    color_space='rgb',
    pos=(-15, 10)
)

y=np.arange(12, 50, 2)
x=np.tile([-6,6], int(y.shape[0]/2))
vertices=np.array(list(zip(x,y)))

zig_zag_zig = visual.ShapeStim(
    win,
    units="deg",
    vertices=vertices,
    closeShape=False,
    pos=[0,0],
    interpolate=True,
    lineWidth=10
)

data = {
    "x": [],
    "y": [],
    "zig_pos": [],
    "cur_pos": [],
    "overlap": [],
    "time": []
}

number = 0
pos = 0
overlap = False
while not event.getKeys(keyList=['q'], timeStamped=False):
    x, y = ms.getPos()
    if np.abs(x) <= 10:
        pos = x
    elif x <= -10:
        pos = -10
    elif x >= 10:
        pos = 10
    
    
    zig_zag_zig.pos -= (0, .2*va.pixDeg())
    cursor.setPos((pos, 0))
    if cursor.overlaps(zig_zag_zig):
        number += 1
        overlap = True
    else:
        overlap = False
    text_stim.setText(str(number))
    line_left.draw()
    line_right.draw()
    zig_zag_zig.draw()
    text_stim.draw()
    cursor.draw()
    time = win.flip()
    print(x, y, zig_zag_zig.pos[1], cursor.pos[0], overlap, time)
    data["x"].append(x)
    data["y"].append(y)
    data["zig_pos"].append(zig_zag_zig.pos[1])
    data["cur_pos"].append(cursor.pos[0])
    data["overlap"].append(overlap)
    data["time"].append(time)
else:
    out = pd.DataFrame.from_dict(data)
    out.to_csv("response.csv", index=False)
    np.save("zigzag.npy", zig_zag_zig.vertices)
    core.quit()
    win.close()

