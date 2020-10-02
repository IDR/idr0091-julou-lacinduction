#!/usr/bin/env python
# This script loads all the images in the study.
# For each image, the map annotation is loaded and the channel name
# is set if the image of the type "raw.

import sys
import argparse
import getpass

import omero
from omero.gateway import BlitzGateway

NAMESPACE = omero.constants.namespaces.NSBULKANNOTATIONS
KEY = "Image File Type"

CHANNELS_RAW = {1: "Phase", 2: "GFP"}
CHANNELS_FLATFIELD = {1: "GFP"}


def set_rnd_settings(image):
    image.setActiveChannels([1], colors=["00FF00"])
    image.setColorRenderingModel()
    image.saveDefaults()
    image.getThumbnail(size=(96,), direct=True)


def change_name(conn, image):
    for ann in image.listAnnotations():
        if ann.OMERO_TYPE == omero.model.MapAnnotationI \
           and ann.getNs() == NAMESPACE:
            image_type = dict(ann.getValue()).get(KEY)
            if image_type == "raw":
                conn.setChannelNames("Image", [image.getId()], CHANNELS_RAW,
                                     channelCount=None)
            elif image_type == "flatfield":
                print("image %s" % image.getId())
                conn.setChannelNames("Image", [image.getId()],
                                     CHANNELS_FLATFIELD,
                                     channelCount=None)
                set_rnd_settings(image)


def load_images(conn, id):
    datasets = conn.getObjects('Dataset', opts={'project': id})
    for dataset in datasets:
        for image in dataset.listChildren():
            change_name(conn, image)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help="The id of the project.")
    parser.add_argument('--username', default="demo")
    parser.add_argument('--server', default="localhost")
    parser.add_argument('--port', default=4064)
    args = parser.parse_args(args)
    password = getpass.getpass()
    # Create a connection
    try:
        conn = BlitzGateway(args.username, password, host=args.server,
                            port=args.port)
        conn.connect()
        load_images(conn, args.id)
    finally:
        conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])
