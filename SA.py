import cadquery as cq
import math

UNIT = 19.05
CU = 18.415
CAP_TOP = 12.7

CAP_RADIUS = 1.5


def sa_indent(angle, height, uwidth):
    DISH_RADIUS = 55
    DIP = 0.738 + 0.1

    rwidth = UNIT * uwidth - (UNIT-CAP_TOP)

    total_dish_r = DISH_RADIUS-DIP

    if uwidth == 1:
        return cq.Workplane("YZ").sphere(DISH_RADIUS).translate([0, math.sin(math.radians(-angle)) * total_dish_r, height + math.cos(math.radians(-angle)) * total_dish_r])

    return cq.Workplane("YZ").sphere(DISH_RADIUS) \
        .circle(DISH_RADIUS).extrude(rwidth/2 - CAP_TOP/2) \
        .translate([-rwidth/2+CAP_TOP/2, math.sin(math.radians(-angle)) * total_dish_r, height + math.cos(math.radians(-angle)) * total_dish_r])\
        .mirror(mirrorPlane="YZ", union=True)

def sa_profile_loft(angle, uwidth, height):
    LOFT = 1

    rwidth = UNIT * uwidth - (UNIT - CU)
    rwidth_cap = UNIT * uwidth - (UNIT - CAP_TOP)

    dish = sa_indent(angle, height, uwidth)

    bottom = cq.Workplane("XY").rect(rwidth - 1, CU - 1).offset2D(0.5)
    support = cq.Workplane("XY").transformed(offset=(0, 0, LOFT)).rect(rwidth - 1.1, CU - 1.1).offset2D(0.5)
    top = cq.Workplane("XY").transformed(offset=(0, 0, height), rotate=(angle, 0, 0)).rect(rwidth_cap - 2*CAP_RADIUS, CAP_TOP - 2*CAP_RADIUS).offset2D(1.5).consolidateWires()

    keycap = cq.Workplane("XY").add(bottom).add(support).add(top).toPending().loft().cut(dish)
    keycap = keycap.edges(cq.selectors.BoxSelector((-rwidth/2, -CU/2, height-2), (rwidth/2, CU/2, height+5))).fillet(0.25)

    return keycap


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
            kobj = sa_profile(key[0], key[1]).translate([(coff + key[1]/2) * UNIT, -roff * UNIT, 0])
            fname = "build/SA/%1dR%3dU.step" % (key[0], key[1]*100)
            cq.exporters.export(kobj, fname)
            show_object(kobj, "Key (%.2f x %d)" % (coff, roff))
            coff += key[1]

        roff += 1


draw_keys(keys)
#draw_keys([[[3, 1.25]]])

