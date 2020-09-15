#!/usr/bin/env python
import argparse
import getpass
import sys
from omero.gateway import BlitzGateway

extension = ".ome.tif"

tokeep = ["20190605_glu_lowLac_1_MMStack.ome.tif",
          "20190606_gfpFlatfield_MMStack.ome.tif",
          "20190614_glu_lowLac_1_MMStack.ome.tif",
          "20190616_gfpFlatfield_MMStack.ome.tif",
          "20180606_gluLac_lac_switch16h_resaved_MMStack.ome.tif",
          "20161007_glu_lac_24h_1_MMStack.ome.tif",
          "20180531_20180604_gfpFlatfield_MMStack.ome.tif",
          "20180604_20180604_gfpFlatfield_MMStack.ome.tif",
          "20180606_20180604_gfpFlatfield_MMStack.ome.tif",
          "20180313_20180315_gfpFlatfield_MMStack.ome.tif",
          "20180316_20180315_gfpFlatfield_MMStack.ome.tif",
          "20180216_20180214_gfpFlatfield_MMStack.ome.tif",
          "20180214_20180214_gfpFlatfield_MMStack.ome.tif",
          "20180206_20180206_gfpFlatfield_MMStack.ome.tif",
          "20180207_20180206_gfpFlatfield_MMStack.ome.tif",
          "20180122_20180118_gfpFlatfield_MMStack.ome.tif",
          "20180119_20180118_gfpFlatfield_MMStack.ome.tif",
          "20180116_20180118_gfpFlatfield_MMStack.ome.tif",
          "20180123_20180118_gfpFlatfield_MMStack.ome.tif",
          "20161014_20161009_gfp_flatfield_MMStack.ome.tif",
          "20161007_20161009_gfp_flatfield_MMStack.ome.tif",
          "20151218_switch8h_1_MMStack_Pos0.ome.tif",
          ]


def fix_image_name(conn):
    query_svc = conn.getQueryService()
    for original in tokeep:
        name = original + "%"
        query = "select i from Image i where i.name like '%s'" % name
        images = query_svc.findAllByQuery(query, None)
        if len(images) == 0:
            continue
        else:
            for i in range(len(images)):
                image = conn.getObject("Image", images[i].getId())
                index = image.series
                print(image.getName())
                n = image.getName()
                values = n.split(" ")
                n = values[0]
                n = n.replace(extension, "_%s%s" % (index, extension))
                image.setName(n)
                image.save()



def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', default="demo")
    parser.add_argument('--server', default="localhost")
    parser.add_argument('--port', default=4064)
    args = parser.parse_args(args)
    password = getpass.getpass()
    # Load the images corresponding to the file names
    # Create a connection
    try:
        conn = BlitzGateway(args.username, password, host=args.server,
                            port=args.port)
        conn.connect()
        fix_image_name(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])
