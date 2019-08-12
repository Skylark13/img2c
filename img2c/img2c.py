#!/usr/bin/env python2

import sys
import os
from PIL import Image

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s [image name]" % (sys.argv[0],)
        sys.exit(-1)

    im = Image.open(sys.argv[1])
    pix = im.load()

    mode_to_bpp = {'L':8, 'RGB':24, 'RGBA':32}
    bpp = mode_to_bpp[im.mode]

    filename = os.path.splitext(sys.argv[1])[0]
    f = open(filename + ".h", "w+")
    f.write("#include <stdint.h>\n\n");
    f.write("static const uint32_t %s_WIDTH = %d;\n" % (filename.upper(), im.size[0]))
    f.write("static const uint32_t %s_HEIGHT = %d;\n" % (filename.upper(), im.size[1]))
    f.write("static const uint32_t %s_BPP = %d;\n" % (filename.upper(), bpp))
    f.write("static const uint8_t %s_DATA[] = \n{\n" % (filename.upper()))


    num = 0
    for y in xrange(0, im.size[1]):
        for x in xrange(0, im.size[0]):
            if num == 0:
                f.write("\t");
            if bpp == 8:
                r = pix[x, y]
                f.write("%s, " % hex(r))
                num = num + 1
            elif bpp == 24:
                r, g, b = pix[x, y]
                f.write("%s, " % hex(r))
                f.write("%s, " % hex(g))
                f.write("%s, " % hex(b))
                num = num + 3
            elif bpp == 32:
                r, g, b, a = pix[x, y]
                f.write("%s, " % hex(r))
                f.write("%s, " % hex(g))
                f.write("%s, " % hex(b))
                f.write("%s, " % hex(a))
                num = num + 4
            if num >= 16:
                f.write("\n");
                num = 0

    if num == 0:
        f.write("};\n")
    else:
        f.write("\n};\n")

    f.close()
