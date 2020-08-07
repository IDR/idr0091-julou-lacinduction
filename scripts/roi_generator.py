#!/usr/bin/env python

# This script parses the value and generates lines in the centre of the image
# The script need to be run Julou_2020_lacInduction_GL_Preproc directory
import csv
import os
from pathlib import Path
import sys

from omero.model import LineI, RoiI

from omero.rtypes import rdouble, rint, rstring
from omero.gateway import BlitzGateway


def process_row(row, x, roi, end_type, parent_id=-1):
    """
    Convert each row into a line shape.
    Add the identifier of the parent shape if applicable.
    """
    frame = int(row[0])
    top = int(row[1])
    bottom = int(row[2])
    # Create the line
    line = LineI()
    line.x1 = rdouble(x)
    line.x2 = rdouble(x)
    line.y1 = rdouble(top)
    line.y2 = rdouble(bottom)
    line.theT = rint(frame)
    name = end_type
    #print(parent_id)
    if parent_id > -1:
        name += ", come from shapeID:%s" % parent_id
    line.textValue = rstring(name)
    # Use yellow
    line.strokeColor = rint(int.from_bytes([255, 255, 0, 255],
                            byteorder='big', signed=True))
    roi.addShape(line)
    return frame


def get_last_shape(roi, timepoint):
    """
    Return the identifier of the shape corresponding to the specified
    timepoint.
    """
    for s in roi.copyShapes():
        if s.getTheT().getValue() == timepoint:
            return s.getId().getValue()
    return -1


def process_file(inputfile, image, svc):
    """
    Read each line of the file
    """
    parents = dict()
    line_count = 0
    roi = None
    parent_shape_id = -1
    parent_id = -1
    cell_id = 0
    x = image.getSizeX()/2
    last_frame = 0
    with open(inputfile) as fp:
        csv_reader = csv.reader(fp, delimiter="\t", quotechar='"')
        for row in csv_reader:
            if line_count > 1:
                # Check the first element to parse
                name = row[0]
                if name.find(">CELL") >= 0:
                    # extract cell info
                    if roi is not None:
                        # we save the roi before starting a new shape
                        roi = svc.saveAndReturnObject(roi)
                        parents[cell_id] = get_last_shape(roi, last_frame)
                    last_frame = -1
                    cell_id = int(row[1])
                    parent_id = int(row[2])
                    end_type = row[6]
                    roi = RoiI()
                    roi.setImage(image._obj)
                    value = "cellID:%s, parent_id: %s" % (cell_id, parent_id)
                    print(value)
                    if parent_id != -1:
                        parent_shape_id = parents[parent_id]
                    else:
                        parent_shape_id = -1
                else:
                    last_frame = process_row(row, x, roi, end_type,
                                             parent_shape_id)
                    parent_shape_id = -1
            line_count += 1


def parse_dir(directory, conn):
    """
    Parse the text files contained the directories.
    The name of each text file should allow us to find the corresponding image.
    """
    query_svc = conn.getQueryService()
    svc = conn.getUpdateService()
    for subdir, dirs, files in os.walk(directory):
        for f in Path(subdir).glob('*.txt'):
            file_name = Path(f).stem
            if file_name.find("fileList") > 0:
                continue
            name = file_name.split("_frames")[0]
            name += ".pattern"
            image = conn.getObjects("Image", attributes={"name": name})
            if image is None:
                print("image not found")
                continue
            else:
                print("processing roi")
                process_file(f, image, svc)


def main(argv):
    if len(argv) == 0:
        directory = os.getcwd()
    else:
        directory = argv[0]
    print(directory)
    # Load the image corresponding to the file name
    # Create a connection
    try:
        conn = BlitzGateway(username, password, host=servername, port=4064)
        conn.connect()
        parse_dir(directory, conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])
