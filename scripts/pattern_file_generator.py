#!/usr/bin/env python

# This script generates the pattern files used to import the data
# The top directory containing the folder with images
# should be specified i.e. Julou_2020_lacInduction_GL_Images

import datetime
import glob
import os
import re
import shutil
import sys

base_path = "/uod/idr/filesets/idr0091-julou-lacinduction/"
generation_path = "/uod/idr/metadata/idr0091-julou-lacinduction/"

def find_range(value):
    """
    Find the t and c range
    """
    m = re.search('_t(.+?)_c', value)
    if not m:
        return -1, -1
    t = m.group(1)
    m = re.search('_c(.+?).tif', value)
    if not m:
        return -1, -1
    c = m.group(1)
    return t, c


def generate_pattern_file(directory):
    """
    Walk through the various directories and generate
    a pattern file in each directory containing the *.tif images
    """
    date = str(datetime.date.today()).replace("-", "")
    pattern_location = generation_path + date + "-pattern"
    if (os.path.exists(pattern_location)):
        shutil.rmtree(pattern_location)
    os.mkdir(pattern_location, 0755)
    for subdir, dirs, files in os.walk(directory):
        values = subdir.split("/")
        if len(values) == 1:
            v = values[0]
        else:
            v = values[1]
        pattern = subdir + "/*.tif"
        fnames = sorted(glob.glob(pattern))
        if len(fnames) == 0:
            continue
        name = values[len(values)-1]
        file_name = name + ".pattern"
        t1, c1 = find_range(fnames[0])
        if t1 == -1 or c1 == -1:
            continue
        t2, c2 = find_range(fnames[-1])
        if t2 == -1 or c2 == -1:
            continue
        value = base_path
        value += subdir + "/"
        value += name + "_t"
        value += "<%s-%s>" % (t1, t2)
        value += "_c<%s-%s>" % (c1, c2)
        value += ".tif"
        print("creating pattern file: %s" % file_name)
        with open(os.path.join(generation_path, file_name), "w") as f:
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
