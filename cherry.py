import math
import cadquery as cq
import units

BOTTOM = 18.1
CAP = 14.15
RADIUS_BOTTOM = 0.5
RADIUS_TOP = 1.5

LOFT = 1

ROW_HEIGHTS = [8.6, 9.2, 7.65, 7.5, 8.8]
ROW_ANGLES = [0, -0.5, -3, -5.62, -10.71]
CAP_OFFSET_Y = [0.75, 0.62, 0.62, 0.42, 0.42]

def cylindrical_indent(angle, height, uwidth):
    DISH_RADIUS = 55
    DIP = 0.738 + 0.1

    rwidth = units.UNIT * uwidth - (units.UNIT-CAP)

    total_dish_r = DISH_RADIUS-DIP

    if uwidth == 1:
        return cq.Workplane("XZ").circle(DISH_RADIUS).extrude(100, both = True) \
            .rotate((0, 0, 0), (1, 0, 0), angle)\
            .translate([0, math.sin(math.radians(-angle)) * total_dish_r, height + total_dish_r])

    cyl = cq.Workplane("XZ").circle(DISH_RADIUS).extrude(100, both=True)
    box = cq.Workplane("XZ").box(rwidth/2 - CAP/2, 2*DISH_RADIUS, 200, centered = [False, True, True])

    return cyl.union(box) \
        .rotate((0, 0, 0), (1, 0, 0), angle)\
        .translate([-rwidth/2+CAP/2, math.sin(math.radians(-angle)) * total_dish_r, height+total_dish_r])\
        .mirror(mirrorPlane="YZ", union=True)


def cherry_profile(row, uwidth, feature = None):
    rwidth = units.UNIT * uwidth - (units.UNIT - BOTTOM)
    rwidth_top = units.UNIT * uwidth - (units.UNIT - CAP)

    bottom = cq.Workplane("XY").rect(rwidth - 2*RADIUS_BOTTOM, BOTTOM - 2*RADIUS_BOTTOM).offset2D(RADIUS_BOTTOM)
    top = cq.Workplane("XY").transformed(offset=(0, (rwidth-rwidth_top)/2 - CAP_OFFSET_Y[row-1], ROW_HEIGHTS[row-1]), rotate=(ROW_ANGLES[row-1], 0, 0)).rect(rwidth_top - 2 * RADIUS_TOP, CAP - 2 * RADIUS_TOP).offset2D(RADIUS_TOP).consolidateWires()

    keycap = cq.Workplane("XY").add(bottom).add(top).toPending().loft(ruled = True)

    return keycap#.cut(cylindrical_indent(ROW_ANGLES[row-1], ROW_HEIGHTS[row-1], uwidth))


