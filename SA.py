import cadquery as cq
import math


UNIT = 19.05
CU = 18.415

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


def sa_sideways_profile(alpha, height, width, concave = True):
    r = 12.7
    alpha_rad = (alpha*math.pi)/180

    dish = (1 if concave else -1) * 0.8

    w = (CU - r * math.cos(alpha_rad)) / 2

    dish = cq.Workplane("XY").sphere(33.5).translate([0, 0, height+33.5-1.2])
    #show_object(dish)
    
    return cq.Workplane("YZ")\
        .moveTo(CU/2, 0)\
        .sagittaArc((CU/2 - w, height + r*math.sin(alpha_rad)), -0.5)\
        .lineTo(-CU/2 + w, height)\
        .sagittaArc((-CU/2, 0), -0.5)\
        .close().extrude(width/2, both=True)\
        .intersect(sa_front_profile(alpha, height, width, concave)).cut(dish)

def sa_profile(row, width):
    BOTTOM = 11.7348
    ROWS = [[], [13, 2], [7, 0], [0, 0], [-7, 1.7], [0, 0]]

    rwidth = width * UNIT - (UNIT-CU)

    return sa_sideways_profile(ROWS[row][0], BOTTOM + ROWS[row][1], rwidth, False if (row == 5 and width > 3) else True).edges(cq.selectors.BoxSelector((-UNIT*width, -UNIT, 5), (UNIT*width, UNIT, 11))).fillet(1)

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
draw_keys([[[3, 1]]])

#show_object(profile(0, BOTTOM, UNIT, False).translate([0, -1*UNIT, 0]))
#show_object(profile(7, BOTTOM+0.5).rotate(axisStartPoint=(0, 0, 0), axisEndPoint=(0, 0, 1), angleDegrees=180).translate([0, 0*UNIT, 0]))
#show_object(sa_profile(3, 1))
#show_object(profile(7, BOTTOM+0.5).translate([0, 2*UNIT, 0]))
#show_object(profile(13, BOTTOM+2).translate([0, 3*UNIT, 0]))


