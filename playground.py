import math
import cadquery as cq
import units

bottom = cq.Workplane("XY").transformed(offset=(0, 0), rotate=(15, 0, 0)).rect(20, 20, centered=[False, False]).offset2D(1)
top = cq.Workplane("XY").transformed(offset=(0, (22-20)/2, 20)).rect(20, 20)

show_object(bottom)
show_object(top)
