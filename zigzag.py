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
from shapely.geometry import LineString
from descartes import PolygonPatch

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

lead = 3
offset = 0.5
y_core = np.arange(-12, 12, 2)
beg = np.array([y_core[0]-lead*2, y_core[0]-lead])
end = np.array([y_core[-1]+lead, y_core[-1]+lead*2])
y = np.hstack([beg, y_core, end])
x_core = np.tile([-3,3], int(y_core.shape[0]/2))
x = np.hstack([np.zeros(2), x_core, np.zeros(2)])
x2 = np.flip(x + offset)
x2[:2] = offset/2
x2[-2:] = offset/2
x2[2] = x2[2]-offset/2
x2[-3] = x2[-3]-offset/2
y2 = np.flip(y)
zigzag_ = np.array(list(zip(np.hstack([x, x2]), np.hstack([y, y2]))))
zigzag_ = np.array(list(zip(x, y)))


lead = 4
offset = 0.5

y_core = np.arange(-12, 12, 2)
x_core = np.tile([-3, -3, 3, 3], int(y_core.shape[0]/4))
xy = np.array(list(zip(x_core, y_core)))

# def create_shape(line, lead, offset):
#     x_core = line[:,0]
#     y_core = line[:,1]
#     beg = np.array([y_core[0]-lead*2, y_core[0]-lead])
#     end = np.array([y_core[-1]+lead, y_core[-1]+lead*2])
#     y1 = np.hstack([beg, y_core, end])
#     x1 = np.hstack([np.zeros(2), x_core, np.zeros(2)])
#     x2 = np.flip(x1 + offset)
#     # x2[:2] = offset/2
#     # x2[-2:] = offset/2
#     # x2[2] = x2[2] - offset/2
#     # x2[-3] = x2[-3] - offset/2
#     y2 = np.flip(y1)
#     shape = np.array(list(zip(np.hstack([x1, x2]), np.hstack([y1, y2]))))
#     return shape


# zigzag_ = create_shape(xy,lead, offset)

def create_shape(xy, buffer):
    zz = LineString(xy)
    line = zz.buffer(buffer)
    patch = PolygonPatch(line)
    vertices = patch.get_path().vertices
    transform = patch.get_patch_transform()
    points = transform.transform(vertices)
    return points






zigzag = visual.ShapeStim(
    win,
    units="deg",
    vertices=points,
    closeShape=True,
    pos=[0,0],
    interpolate=True,
    lineWidth=0,
    fillColor=(0,0,0),
    colorSpace="rgb255"
)


# zigzag2 = visual.ShapeStim(
#     win,
#     units="deg",
#     vertices=zigzag_,
#     closeShape=False,
#     pos=[0,0],
#     interpolate=True,
#     lineWidth=2,
#     lineColor=(0,0,0),
#     colorSpace="rgb255"
# )

while not event.getKeys(keyList=["escape"], timeStamped=False):
    zigzag.draw()
    # zigzag2.draw()
    win.flip()

win.close()
core.quit()
