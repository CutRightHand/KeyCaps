import cadquery as cq
import math


UNIT = 19.05
CU = 18.415
CAP_TOP = 12.7

def sa_front_profile(alpha, height, width, concave = True):
    r = 12.7
    w = (CU-r)/2
    alpha_rad = (alpha*math.pi)/180

    dish = (1 if concave else -1) * 1

    rp = (CU - r * math.cos(alpha_rad)) / 2

    cronk = cq.Workplane("XZ") \
        .moveTo(width/2, 0) \
        .sagittaArc((width/2 - w, height), -0.5) \
        .lineTo(-width/2+w, height) \
        .sagittaArc((-width/2, 0), -0.5) \
        .close().extrude(UNIT, both=True)\
        .union(cq.Workplane("XY").box(width, 2*UNIT, UNIT, centered=[True, True, False]).translate([0, 0, -UNIT]))\
        .rotate(axisStartPoint=(0, -CU/2+rp, height), axisEndPoint=(1, -CU/2+rp, height), angleDegrees=alpha)
    
    #show_object(cronk)
    
    return cronk


def sa_sideways_profile(alpha, height, rwidth, uwidth, concave = True):
    r = 12.7
    alpha_rad = (alpha*math.pi)/180

    dish = (1 if concave else -1) * 0.8

    w = (CU - r * math.cos(alpha_rad)) / 2

    dish = sa_indent(height, uwidth)
    #show_object(dish, "Cutter", {'alpha': 0.75})
    
    return cq.Workplane("YZ")\
        .moveTo(CU/2, 0)\
        .sagittaArc((CU/2 - w, height + r*math.sin(alpha_rad)), -0.5)\
        .lineTo(-CU/2 + w, height)\
        .sagittaArc((-CU/2, 0), -0.5)\
        .close().extrude(rwidth / 2, both=True)\
        .intersect(sa_front_profile(alpha, height, rwidth, concave))#.cut(dish)#.edges(cq.selectors.BoxSelector((-UNIT * rwidth, -UNIT, 4), (UNIT * rwidth, UNIT, 20))).fillet(0.5)

def sa_indent(height, width):
    DISH_RADIUS = 45
    DIP = 0.738

    real_width = CAP_TOP/2 # UNIT * width - (UNIT-CU)

    if width == 1:
        return cq.Workplane("YZ").sphere(DISH_RADIUS).translate([0, +0.2, height+DISH_RADIUS-DIP])

    return cq.Workplane("YZ").sphere(DISH_RADIUS) \
        .circle(DISH_RADIUS).extrude(real_width/2) \
        .translate([-real_width/2, 0, height+DISH_RADIUS-DIP]) \
        .mirror(mirrorPlane="YZ", union=True)


def sa_profile(row, uwidth):
    BOTTOM = 11.7348
    ROWS = [[], [13, 2], [7, 0], [0, 0], [-7, 1.7], [0, 0]]

    rwidth = uwidth * UNIT - (UNIT - CU)

    return sa_sideways_profile(ROWS[row][0], BOTTOM + ROWS[row][1], rwidth, uwidth, False if (row == 5 and uwidth > 3) else True)#.faces("<Z").shell(-0.01)


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
        [5, 1], [5, 2], [5, 2.25], [5, 6.5]
    ],

]





def draw_keys(keys):
    roff = 0
    coff = 0
    for row in keys:
        coff = 0

        for key in row:
            kobj = sa_profile(key[0], key[1]).translate([(coff + key[1]/2) * UNIT, -roff * UNIT, 0])#.fillet(0.0001)
            log(kobj.val())
            show_object(kobj, "Key (%.2f x %d)" % (coff, roff))
            coff += key[1]

        roff += 1

#draw_keys(keys)
#draw_keys([[[3, 1]]])
#show_object(sa_indent(0, 2))

#show_object(profile(0, BOTTOM, UNIT, False).translate([0, -1*UNIT, 0]))
#show_object(profile(7, BOTTOM+0.5).rotate(axisStartPoint=(0, 0, 0), axisEndPoint=(0, 0, 1), angleDegrees=180).translate([0, 0*UNIT, 0]))
show_object(sa_profile(1, 1), "SA Profile", {'alpha': 0.3, 'color': 'blue'})
#show_object(profile(7, BOTTOM+0.5).translate([0, 2*UNIT, 0]))
#show_object(profile(13, BOTTOM+2).translate([0, 3*UNIT, 0]))


LOFT = 1
LA = 1

cronk = cq.Workplane("XY").rect(CU, CU)
cronk = cronk.workplane(offset = LOFT).transformed(rotate = (LA, 0, 0)).rect(CU * 0.99, CU * 0.99)
cronk = cronk.add(cq.Workplane("XY")).transformed(offset = (0, 0, 14.2), rotate = (13 - LA, 0, 0)).rect(CAP_TOP, CAP_TOP)
cronk = cronk.loft()#.faces("<Z").shell(-1)
show_object(cronk, "Loft profile", {'alpha': 0.3, 'color': 'red'})
