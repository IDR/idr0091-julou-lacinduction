#!/usr/bin/env python
import argparse
import getpass
import sys
from omero.gateway import BlitzGateway

extension = ".ome.tif"


def fix_name(conn, dataset_name):
    dataset = conn.getObject("Dataset", attributes={"name": dataset_name})
    for image in dataset.listChildren():
        fs = image.getFileset()
        data = fs.copyImages()
        print(len(data))
        if len(data) > 1:
            index = image.series
            name = image.getName()
            name = name.replace(extension, "_%s%s" % (index, extension))
            image.setName(name)
            image.save()


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')
    parser.add_argument('--username', default="demo")
    parser.add_argument('--server', default="localhost")
    parser.add_argument('--port', default=4064)
    args = parser.parse_args(args)
    password = getpass.getpass()
    # Load the dataset corresponding to the file name
    # Create a connection
    try:
        conn = BlitzGateway(args.username, password, host=args.server,
                            port=args.port)
        conn.connect()
        fix_name(conn, args.dataset)
    finally:
        conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])
