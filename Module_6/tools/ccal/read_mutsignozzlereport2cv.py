from tarfile import open as tarfile_open

from pandas import read_csv


def read_mutsignozzlereport2cv(tar_gz_file_path, genes):

    with tarfile_open(tar_gz_file_path) as tar_gz_file:

        n = read_csv(
            tar_gz_file.extractfile(
                tuple(
                    file
                    for file in tar_gz_file
                    if file.name.endswith("patient_counts_and_rates.txt")
                )[0]
            ),
            sep="\t",
            index_col=1,
        ).shape[0]

        maf = read_csv(
            tar_gz_file.extractfile(
                tuple(
                    file
                    for file in tar_gz_file
                    if file.name.endswith("final_analysis_set.maf")
                )[0]
            ),
            encoding="iso-8859-1",
            sep="\t",
        )

        gene_group = maf.groupby("Hugo_Symbol")

        df = read_csv(
            tar_gz_file.extractfile(
                tuple(
                    file for file in tar_gz_file if file.name.endswith("sig_genes.txt")
                )[0]
            ),
            sep="\t",
            index_col=1,
        )

        gene_q_value = df["q"].reindex(index=genes).to_dict()

    gene_variant_classification = {}

    gene_variant_type = {}

    gene_variant_frequency = {}

    for gene in genes:

        if gene in gene_group.groups:

            df = gene_group.get_group(gene)

            gene_variant_classification[gene] = (
                df["Variant_Classification"].value_counts().to_dict()
            )

            gene_variant_type[gene] = df["Variant_Type"].value_counts().to_dict()

            gene_variant_frequency[gene] = (
                df["Tumor_Sample_Barcode"].dropna().unique().size / n
            )

        else:

            gene_variant_classification[gene] = {}

            gene_variant_type[gene] = {}

            gene_variant_frequency[gene] = 0

    return (
        n,
        gene_variant_classification,
        gene_variant_type,
        gene_q_value,
        gene_variant_frequency,
    )
