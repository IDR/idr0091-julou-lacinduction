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

In the 2019 folders, there are MicroManager ``ome.tif`` files without ``metadata.txt``.
Only "ome.tif" without a position will be imported e.g. ``20190605_glu_lowLac_1_MMStack.ome.tif`` and not
``20190605_glu_lowLac_1_MMStack_1.ome.tif``. The ``ome.tiff`` files are not valid ome.tiff.
This means that when the file is imported into OMERO, we end up with images with exactly the same name
leading to error when applying the annotation.
To fix the naming issue, run [fix_image_name.py](scripts/fix_image_name.py) on the dataset 2019 containing the raw data e.g. ``2019_raw``. The index of the image is added to the name e.g.
``20190605_glu_lowLac_1_MMStack.ome.tif`` becomes ``20190605_glu_lowLac_1_MMStack_1.ome.tif``.


If a new name is used, [idr0091-experimentA-filePaths.tsv](experimentA/idr0091-experimentA-filePaths.tsv)


After import, run the script [roi_generator.py](scripts/pattern_file_generator.py) to
create the ROIs.

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