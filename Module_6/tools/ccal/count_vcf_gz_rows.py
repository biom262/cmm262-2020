from gzip import open as gzip_open

from .VCF_COLUMNS import VCF_COLUMNS


def count_vcf_gz_rows(
    vcf_gz_file_path, info_fields_to_count=None, format_fields_to_count=None
):

    fields = ()

    if info_fields_to_count is not None:

        fields += info_fields_to_count

    if format_fields_to_count is not None:

        fields += format_fields_to_count

    counts = {field: 0 for field in fields}

    print("Validating {} ...".format(vcf_gz_file_path))

    with gzip_open(vcf_gz_file_path) as vcf_gz_file:

        line = vcf_gz_file.readline().decode()

        while line.startswith("##"):

            line = vcf_gz_file.readline().decode()

        else:

            if not line.startswith("#CHROM"):

                raise ValueError(
                    "The line follwoing the meta-information lines ({}) is not the column header.".format(
                        line
                    )
                )

            elif len(line.split(sep="\t")) < 10:

                raise ValueError(
                    "Column header does not contain all of {} and at least 1 sample.".format(
                        ", ".join(VCF_COLUMNS), line
                    )
                )

            elif 10 < len(line.split(sep="\t")):

                raise NotImplementedError(
                    "There are 1< samples and multi-sample .vcf file is not supported yet."
                )

        for i, line in enumerate(vcf_gz_file):

            if i % 1e5 == 0:

                print("\t{:,} ...".format(i))

            line_split = line.decode().split(sep="\t")

            chrom, pos, id_, ref, alt, qual, filter_, info, format_, sample = line_split

            if info_fields_to_count is not None:

                info_fields = [
                    field_value.split(sep="=")[0] for field_value in info.split(sep=";")
                ]

                for field in info_fields_to_count:

                    if field in info_fields:

                        counts[field] += 1

            if format_fields_to_count is not None:

                format_fields = format_.split(sep=":")

                for field in format_fields_to_count:

                    if field in format_fields:

                        counts[field] += 1

    counts["n"] = i + 1

    return counts
