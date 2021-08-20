import cadquery as cq

UNIT = 19.05
CU = 18.415

def dummy_profile(row, uwidth, feature = None):
    return cq.Workplane("XY").box(CU*uwidth, CU, CU, centered=[True, True, False])
