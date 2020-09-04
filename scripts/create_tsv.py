import datetime
import glob
import os
import sys

base_path = "/uod/idr/filesets/idr0091-julou-lacinduction/"
generation_path = "/tmp/idr0091-julou-lacinduction/"
path = "/uod/idr/metadata/idr0091-julou-lacinduction/"
file_name = "idr0091-experimentA-filePaths.tsv"
base_dataset = "Project:name:idr0091-julou-lacinduction/experimentA/Dataset:name:"
metadata_pattern = "/*metadata.txt"

def write_to_file(subdir, pattern, name_extension):
    values = subdir.split("/")
    n = values[len(values)-1]
    dataset = base_dataset + n[:4] + "_" + name_extension
    fnames = sorted(glob.glob(pattern))
    text = "_metadata.txt"
    with open(os.path.join(generation_path, file_name), "a") as f:
        for file in fnames:
            file_path = os.path.abspath(file)
            n = os.path.basename(file)
            if text in n:
                n = n.replace(text, ".ome.tif")
            f.write(dataset + "\t%s\t%s" % (file_path, n))
            f.write("\n")
    if len(fnames) == 0 and metadata_pattern in pattern:
        write_to_file(subdir, subdir + "/*MMStack.ome.tif", name_extension)



def generate_tsv(directory, name_extension, pattern):
    date = str(datetime.date.today()).replace("-", "")
    date = str(20200817)
    pattern_location = path + date + "-pattern/"
    path_location = path + date + "-pattern/"
    fnames = sorted(os.listdir(pattern_location))
    for subdir, dirs, files in os.walk(directory):
        if subdir == directory:
            continue
        values = subdir.split("/")
        n = values[len(values)-1]
        dataset = base_dataset + n[:4] + "_" + name_extension
        name = values[len(values)-1] + ".pattern"
        if name in fnames:
            file_path = path_location + name
            with open(os.path.join(generation_path, file_name), "a") as f:
                f.write(dataset + "\t%s\t%s" % (file_path, name))
                f.write("\n")
        else:
            write_to_file(subdir, subdir + pattern, name_extension)


def main(argv):
    directory = argv[0]
    name = argv[1]  # either pre-processed or raw
    pattern = metadata_pattern
    if len(argv) > 2:
        if argv[2] in "tif":
            pattern = "/*.tif"
    generate_tsv(directory, name, pattern)

if __name__ == "__main__":
    main(sys.argv[1:])