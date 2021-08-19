# KeyCaps

## A foreword
This is a work in progress. There are many things missing. Hopefully the list of those things will grow smaller over
time.

# What is this?
CadQuery code to generate models of keyboard keycaps in various profiles, and formats. This repo hopes to be the
authoritative place to find models for your modeling or rendering needs.

# How to use 
Please visit the releases page to get an archive with the current version of the prepared resources.

Alternatively, clone this repo, and then run the following to set up your environment:

... instructions broken, fix me...

> conda env create -f keycaps_env.yml -n keycaps
> conda activate keycaps
> Make

...


# Filename patterns

The directories inside the archive represent the keycap profile in question, while the file names have the following
structure:

> xRyyyUm.(stl|stp)

x = Row indicator, starting from the row farthest away from the user of the
keyboard. This row numbering is the natural row numbering for SA keycaps, but
might be inverted for some other profiles.

yyy = width of the keycap model, expressed as hundredths of keycap unit size
(19.05mm). Eg 625 is a 6.25u keycap model commonly used for space bars.

m = modifier, as follows
    * HD - homing dish
    * HB - homing bump
    * HL - homing line
    * C - convex (typically for space bars)

