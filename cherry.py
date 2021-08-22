import cadquery as cq
import units

BOTTOM = 18.1
CAP = 14.15
RADIUS_BOTTOM = 0.5
RADIUS_TOP = 1.5

LOFT = 1

ROW_HEIGHTS = [10, 7.6, 6.65, 7.5, 8.8]
ROW_ANGLES = [0, -3, -5.5, -11, -10]
CAP_OFFSET_Y = [0.975, 1.2, 1.3, 1.3, 1.45]


def cherry_profile(row, uwidth, feature = None):
    rwidth = units.UNIT * uwidth - (units.UNIT - BOTTOM)
    rwidth_top = units.UNIT * uwidth - (units.UNIT - CAP)

    bottom = cq.Workplane("XY").rect(rwidth - 2*RADIUS_BOTTOM, BOTTOM - 2*RADIUS_BOTTOM).offset2D(RADIUS_BOTTOM)
    top = cq.Workplane("XY").transformed(offset=(0, CAP_OFFSET_Y[row-1], ROW_HEIGHTS[row-1]), rotate=(ROW_ANGLES[row-1], 0, 0)).rect(rwidth_top - 2 * RADIUS_TOP, CAP - 2 * RADIUS_TOP).offset2D(RADIUS_TOP).consolidateWires()

    keycap = cq.Workplane("XY").add(bottom).add(top).toPending().loft(ruled = True)

    return keycap


