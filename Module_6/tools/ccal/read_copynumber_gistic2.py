from tarfile import open as tarfile_open

from pandas import read_csv


def read_copynumber_gistic2(tar_gz_file_path, genes):

    with tarfile_open(tar_gz_file_path) as tar_gz_file:

        n = read_csv(
            tar_gz_file.extractfile(
                tuple(
                    file
                    for file in tar_gz_file
                    if file.name.endswith("arraylistfile.txt")
                )[0]
            ),
            sep="\t",
        ).shape[0]

        df = read_csv(
            tar_gz_file.extractfile(
                tuple(
                    file
                    for file in tar_gz_file
                    if file.name.endswith("amp_genes.conf_99.txt")
                )[0]
            ),
            sep="\t",
            index_col=0,
        ).dropna(how="all", axis=1)

        cytoband_amp_q_value = df.iloc[0, :].to_dict()

        cytoband_amp_genes = df.apply(
            lambda column: set(column.iloc[3:].dropna())
        ).to_dict()

        df = read_csv(
            tar_gz_file.extractfile(
                tuple(
                    file
                    for file in tar_gz_file
                    if file.name.endswith("del_genes.conf_99.txt")
                )[0]
            ),
            sep="\t",
            index_col=0,
        ).dropna(how="all", axis=1)

        cytoband_del_q_value = df.iloc[0, :].to_dict()

        cytoband_del_genes = df.apply(
            lambda column: set(column.iloc[3:].dropna())
        ).to_dict()

    gene_cna = {}

    gene_cytoband = {}

    gene_q_value = {}

    for gene in genes:

        for cytoband_cna, cytoband_q_value, cytoband_genes in (
            ("AMP", cytoband_amp_q_value, cytoband_amp_genes),
            ("DEL", cytoband_del_q_value, cytoband_del_genes),
        ):

            for cytoband, genes_ in cytoband_genes.items():

                if gene in genes_:

                    q_value = cytoband_q_value[cytoband]

                    if gene not in gene_q_value or q_value < gene_q_value[gene]:

                        gene_cna[gene] = cytoband_cna

                        gene_cytoband[gene] = cytoband

                        gene_q_value[gene] = q_value

    return n, gene_cna, gene_cytoband, gene_q_value
