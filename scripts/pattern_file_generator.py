#!/usr/bin/env python

# This script generates the pattern files used to import the data
# The top directory containing the folder with images
# should be specified i.e. Julou_2020_lacInduction_GL_Images

import glob
import os
from pathlib import Path
import re
import sys


def find_range(value):
    """
    Find the t and c range
    """
    m = re.search('_t(.+?)_c', value)
    t = m.group(1)
    m = re.search('_c(.+?).tif', value)
    c = m.group(1)
    return t, c


def generate_pattern_file(directory):
    """
    Walk through the various directories and generate
    a pattern file in each directory containing the *.tif images
    """
    for subdir, dirs, files in os.walk(directory):
        pattern = subdir + "/*.tif"
        fnames = sorted(glob.glob(pattern))
        if len(fnames) == 0:
            continue
        name = Path(subdir).stem
        file_name = name + ".pattern"

        t1, c1 = find_range(fnames[0])
        t2, c2 = find_range(fnames[-1])
        value = name + "_t"
        value += "<%s-%s>" % (t1, t2)
        value += "_c<%s-%s>" % (c1, c2)
        value += ".tif"
        print("creating pattern file: %s" % file_name)
        with open(os.path.join(subdir, file_name), "w") as f:
            f.write(value)


def main(argv):
    if len(argv) == 0:
        directory = os.getcwd()
    else:
        directory = argv[0]
    print(directory)
    generate_pattern_file(directory)


if __name__ == "__main__":
    main(sys.argv[1:])
