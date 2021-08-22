import cadquery as cq
import units
import SA
import dummy
import cherry

profiles = {
    'dummy': dummy.dummy_profile,
    'SA': SA.sa_profile,
    'Cherry': cherry.cherry_profile,
}

profile = "Cherry"


keys = [
    [
        "1R", [1, 1], [1, 2]
    ],
    [
        "2R", [2, 1], [2, 1.5]
    ],
    [
        "3R", [3, 1], [3, 1.75], [3, 2.25]
    ],
    [
        "4R", [4, 1], [4, 2.25], [4, 2.75]
    ],
    [
        "5R", [5, 1], [5, 1.25], [5, 1.5], [5, 2], [5, 2.25], [5, 6.5]
    ],
    [
        profile
    ]
]

def draw_keys(generator, keys, writer):
    roff = 0
    coff = 0
    for row in keys:
        coff = 0

        for key in row:
            if not isinstance(key, str):
                kobj = generator(key[0], key[1])
                writer(key, roff, coff, kobj)
                coff += key[1]
            else:
                offset = 0 if (roff+1 == len(keys)) else -30
                halign = 'left' if (roff+1 == len(keys)) else 'right'
                kobj = cq.Workplane("XY").text(key, units.CU, 1, halign=halign).translate([offset, -roff * units.UNIT, 0])
                writer(key, roff, coff, kobj)

        roff += 1


def writer_file(key, row, column, kobj):
    if not isinstance(key, str):
        fname = "build/SA/%1dR%3dU.step" % (key[0], key[1] * 100)
        cq.exporters.export(kobj, fname)

def writer_cqgui(key, row, column, model):
    if not isinstance(key, str):
        model = model.translate([(column + key[1]/2) * units.UNIT, -row * units.UNIT, 0])

    show_object(model)

writer = writer_cqgui

draw_keys(profiles[profile], keys, writer)
#draw_keys(profiles[profile], [[[3, 1.25]]], writer)


