import cadquery as cq
import units


def dummy_profile(row, uwidth, feature = None):
    rwidth = units.UNIT * uwidth - (units.UNIT - units.CU)
    return cq.Workplane("XY").box(rwidth, units.CU, units.CU, centered=[True, True, False])
