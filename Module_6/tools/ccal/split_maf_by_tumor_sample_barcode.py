from pandas import read_csv

from .establish_path import establish_path


def split_maf_by_tumor_sample_barcode(maf_file_path):

    maf_df = read_csv(maf_file_path, encoding="iso-8859-1", comment="#", sep="\t")

    for i, maf_df_ in maf_df.groupby("Tumor_Sample_Barcode"):

        output_directory_path = "{}.split_maf_by_tumor_sample_barcode".format(
            maf_file_path
        )

        establish_path(output_directory_path, "directory")

        maf_df_.to_csv("{}/{}.maf".format(output_directory_path, i), sep="\t", index=0)
