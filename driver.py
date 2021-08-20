import cadquery as cq
import units
import SA
import dummy

profiles = {
    'dummy': dummy.dummy_profile,
    'SA': SA.sa_profile
}

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

def draw_keys(generator, keys, writer):
    roff = 0
    coff = 0
    for row in keys:
        coff = 0

        for key in row:
            kobj = generator(key[0], key[1]).translate([(coff + key[1]/2) * units.UNIT, -roff * units.UNIT, 0])
            #show_object(kobj, "Key (%.2f x %d)" % (coff, roff))
            writer(key, kobj)
            coff += key[1]

        roff += 1

def writer_file(key, kobj):
    fname = "build/SA/%1dR%3dU.step" % (key[0], key[1] * 100)
    cq.exporters.export(kobj, fname)

def writer_cqgui(keyspec, model):
    show_object(model)


profile = "dummy"
writer = writer_cqgui


#draw_keys(keys)
draw_keys(profiles[profile], [[[3, 1.25]]], writer)


