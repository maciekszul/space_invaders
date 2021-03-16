from psychopy import core, event
import psychopy.visual as visual
from psychopy import monitors
from psychopy.visual import SphereStim, LightSource, RigidBodyPose
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
    winType="pyglet",
    viewOri=45
)

win.lights = [
    visual.LightSource(win, pos=(0, 0, -5), lightType='point',
                diffuseColor=(0, 0, 0), specularColor=(1, 1, 1))
]

line_right = visual.Line(
    win,
    [1, -1],
    [1, 1],
    lineWidth=2,
    lineColor="white",
    units="deg"
)

line_left = visual.Line(
    win,
    [-1, -1],
    [-1, 1],
    lineWidth=2,
    lineColor="white",
    units="deg"
)

pivotPose = RigidBodyPose((0, 0, -2))
lightSphere = SphereStim(win, radius=0.05, color='white', useShaders=False)
sphere1 = SphereStim(win, radius=0.02, color='red', useShaders=False)
sphere2 = SphereStim(win, radius=0.02, color='red', useShaders=False)
sphere3 = SphereStim(win, radius=0.02, color='red', useShaders=False)
sphere4 = SphereStim(win, radius=0.02, color='red', useShaders=False)
sphere5 = SphereStim(win, radius=0.02, color='red', useShaders=False)


z = -10
while not event.getKeys():
    win.setPerspectiveView()
    lightSphere.thePose = pivotPose

    sphere1.setPos([0.2, 0, z])
    sphere2.setPos([-0.2, 0, z-2.])
    sphere3.setPos([0.2, 0, z-4.])
    sphere4.setPos([-0.2, 0, z-6])
    sphere5.setPos([0.2, 0, z-8])

    sphere1.draw()
    sphere2.draw()
    sphere3.draw()
    sphere4.draw()
    sphere5.draw()
    line_right.draw()
    line_left.draw()
    # lightSphere.draw()
    win.useLights = True
    win.flip()
    z += 0.005

win.close()
core.quit()