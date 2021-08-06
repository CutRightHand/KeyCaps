import cadquery as cq
import math


UNIT = 19.05
CU = 18.415
CAP_TOP = 12.7
BOTTOM = 11.7348

LOFT = 1
LA = 1

cronk = cq.Workplane("XY").rect(CU, CU)
cronk = cronk.workplane(offset = LOFT).transformed(rotate = (LA, 0, 0)).rect(CU * 0.99, CU * 0.99)
cronk = cronk.workplane(offset =BOTTOM - LOFT).transformed(rotate = (13 - LA, 0, 0)).rect(CAP_TOP, CAP_TOP)
cronk = cronk.loft()#.faces("<Z").shell(-1)#.faces("not <Z").fillet(0.5)
show_object(cronk)