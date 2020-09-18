# idr0091-julou-lacinduction

## Steps post Import


Raw Files
---------

There are MicroManager ``ome.tif`` files without ``metadata.txt``.
Only "ome.tif" without a position will be imported e.g. ``20190605_glu_lowLac_1_MMStack.ome.tif`` and not
``20190605_glu_lowLac_1_MMStack_1.ome.tif``. The ``ome.tiff`` files are not valid ome.tiff.
This means that when the file is imported into OMERO, we end up with images with exactly the same name
leading to error when applying the annotation.
To fix the naming issue, run [fix_image_name.py](scripts/fix_image_name.py).


ROIs
----

After import, run the script [roi_generator.py](scripts/pattern_file_generator.py) to
create the ROIs.


## Import Status

### idr-pilot
| Task | Duration | Checked |
| :----: |:----:| :----:|
| Images| 36 hours | -- |
| Thumbnails | -- | -- |
| Annotations | -- | -- |

### idr-next
| Task | Duration | Checked |
| :----: |:----:| :----:|
| Images| -- | -- |
| Thumbnails | -- | -- |
| Annotations | -- | -- |