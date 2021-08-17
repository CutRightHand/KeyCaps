import cadquery as cq
import math

UNIT = 19.05
CU = 18.415
CAP_TOP = 12.7

def sa_indent(angle, height, uwidth):
    DISH_RADIUS = 55
    DIP = 0.738 + 0.001

    rwidth = UNIT * uwidth - (UNIT-CAP_TOP)

    total_dish_r = DISH_RADIUS-DIP

    if uwidth == 1:
        return cq.Workplane("YZ").sphere(DISH_RADIUS).translate([0, math.sin(math.radians(-angle)) * total_dish_r, height + math.cos(math.radians(-angle)) * total_dish_r])

    return cq.Workplane("YZ").sphere(DISH_RADIUS) \
        .circle(DISH_RADIUS).extrude(rwidth/2 - CAP_TOP/2) \
        .translate([-rwidth/2+CAP_TOP/2, math.sin(math.radians(-angle)) * total_dish_r, height + math.cos(math.radians(-angle)) * total_dish_r])\
        .mirror(mirrorPlane="YZ", union=True)

def sa_profile_loft(angle, uwidth, height):
    LOFT = 2

    rwidth = UNIT * uwidth - (UNIT - CU)
    rwidth_cap = UNIT * uwidth - (UNIT - CAP_TOP)

    cronk = cq.Workplane("XY").rect(rwidth, CU)
    cronk = cronk.workplane(offset=LOFT).transformed(rotate=(0, 0, 0)).rect(rwidth - 0.1, CU * 0.99)
    cronk = cronk.add(cq.Workplane("XY")).transformed(offset=(0, 0, height-LOFT), rotate=(angle, 0, 0)).rect(rwidth_cap, CAP_TOP)
    cronk = cronk.loft()

    dish = sa_indent(angle, height, uwidth)
    cronk = cronk.cut(dish)

    cronk = cronk.faces("<Z").shell(-1.5, kind = 'arc')
    cronk = cronk.edges("not <Z").fillet(1)

    #cronk = cq.Workplane("XY").box(UNIT, UNIT, UNIT, centered = [True, True, False]).cut(dish).edges().fillet(2)

    return cronk


def sa_profile(row, uwidth):
    BOTTOM = 11.7348
    ROWS = [[], [13, 3.5], [7, 1], [0, 0], [-7, 1], [0, 0]]

    return sa_profile_loft(ROWS[row][0], uwidth, BOTTOM+ROWS[row][1])


keys = [
    [
        [1, 1], [1, 2]
    ],
    [
        [2, 1], [2, 1.5]
    ],
    [
        [3, 1], [3, 1.75], [3, 2.25]
    ],
    [
        [4, 1], [4, 2.25], [4, 2.75]
    ],
    [
        [5, 1], [5, 1.25], [5, 1.5], [5, 2], [5, 2.25], [5, 6.5]
    ],

]


def draw_keys(keys):
    roff = 0
    coff = 0
    for row in keys:
        coff = 0

        for key in row:
            kobj = sa_profile(key[0], key[1]).translate([(coff + key[1]/2) * UNIT, -roff * UNIT, 0])#.fillet(0.0001)
            show_object(kobj, "Key (%.2f x %d)" % (coff, roff))
            coff += key[1]

        roff += 1


draw_keys(keys)
#draw_keys([[[5, 6.5]]])

#show_object(sa_profile(3, 1.25))
