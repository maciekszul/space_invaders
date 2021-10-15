import numpy as np
from shapely.geometry import LineString
from descartes import PolygonPatch


def create_zigzag(length, swing, start_point, spacing, lead, shuffle=False):
    """Create a consistent zigzag line
    Arguments
    length -- y axis "height" of the shape, excluding a lead in and out lines
    swing -- x axis absolute distance of the zig grom the center
    start point -- offset of the starting point of the zigzag from the center
    spacing -- distance between the points
    lead -- length of the center line leading to the zigzag and ending it
    shuffle -- boolean whether to shuffle the zigs and zags

    Returns an array of xy coordinates of points forming a zigzag line
    """

    y_core = np.arange(start_point, length + start_point, spacing)
    x_core = np.tile([-swing, -swing, swing, swing], int(y_core.shape[0]/4))
    beg = np.array([y_core[0] - (lead + spacing), y_core[0] - spacing])
    end = np.array([y_core[-1] + spacing, y_core[-1] + (lead + spacing)])
    y = np.hstack([beg, y_core, end])
    x = np.hstack([np.zeros(2), x_core, np.zeros(2)])
    return np.array(list(zip(x, y)))





def create_shape(xy, buffer):
    """Create a buffered polygon from a line.
    Arguments
    xy -- list of xy coordinates of the points
    buffer -- half of the thickness of the line

    Returns an array of xy coordinates of points
    forming a closed shape polygon.
    """
    zz = LineString(xy)
    line = zz.buffer(buffer)
    patch = PolygonPatch(line)
    vertices = patch.get_path().vertices
    transform = patch.get_patch_transform()
    points = transform.transform(vertices)
    return points
