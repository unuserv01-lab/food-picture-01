# food-picture-01 — round 2: "Ridge Line, 6AM — Padang"

One 3-cm rendang cube + one tight rice mound as a single hero, shot plate-level
(0 degrees, 100mm macro) on a matte black basalt slab. Hard snooted flash rakes
through a slatted banana leaf, carving shadow stripes; a mirror-thin pool of
sambal holds a live candle flame's reflection, and a lit steam ribbon crosses
the frame.

`main.py` (Python 3.13, stdlib only) validates the bundled photograph
(`assets/entry.jpg`, 1024x1024 JPEG) against the competition limits (<=1 MiB,
<=1024x1024) and copies it byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`,
so two runs always write identical bytes. RULES.txt allows a JPEG payload
under the `entry.png` name ("told apart by its first bytes").

## Run

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
