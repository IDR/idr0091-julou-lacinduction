# idr0091-julou-lacinduction

## Steps

Import
------

Processed files
~~~~~~~~~~~~~~~

Before importing the images, pattern files have been generated to combine processed images from 2015 and 2016 only. The [pattern_file_generator.py](scripts/pattern_file_generator.py) script was used to generate
the files.

Raw Files
~~~~~~~~~

There are MicroManager ``ome.tif`` files without ``metadata.txt``.
Only "ome.tif" without a position will be imported e.g. ``20190605_glu_lowLac_1_MMStack.ome.tif`` and not
``20190605_glu_lowLac_1_MMStack_1.ome.tif``. The ``ome.tiff`` files are not valid ome.tiff.
This means that when the file is imported into OMERO, we end up with images with exactly the same name
leading to error when applying the annotation.
To fix the naming issue, run [fix_image_name.py](scripts/fix_image_name.py).

Assay file
~~~~~~~~~~

When a modification is made to the assay file, the script [convert_assays.py](scripts/convert_assays.py)
must be run on the newly updated file to generated a correct assay file.

If a new name is used, [idr0091-experimentA-filePaths.tsv](experimentA/idr0091-experimentA-filePaths.tsv)


After import, run the script [roi_generator.py](scripts/pattern_file_generator.py) to
create the ROIs. The script 

## Import Status

### idr-pilot
| Task | Duration | Checked |
| :----: |:----:| :----:|
| Images| 2 days? | -- |
| Thumbnails | -- | -- |
| Annotations | -- | -- |

### idr-next
| Task | Duration | Checked |
| :----: |:----:| :----:|
| Images| -- | -- |
| Thumbnails | -- | -- |
| Annotations | -- | -- |