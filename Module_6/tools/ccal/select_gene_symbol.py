from os.path import dirname

from numpy import asarray
from pandas import isna, read_csv


def select_gene_symbol(
    gene_family_name_to_remove=(
        "18S ribosomal RNAs",
        "28S ribosomal RNAs",
        "45S pre-ribosomal RNAs",
        "5.8S ribosomal RNAs",
        "5S ribosomal RNAs",
        "Cytoplasmic transfer RNAs",
        "Long non-coding RNAs (published)",
        "MicroRNAs",
        "Mitochondrially encoded ribosomal RNAs",
        "Mitochondrially encoded tRNAs",
        "Nuclear-encoded mitochondrial transfer RNAs",
        "Piwi-interacting RNA clusters",
        "Ribosomal 45S RNA clusters",
        "Ribosomal 45S rRNA genes outside of clusters",
        "RNAs, 7SL, cytoplasmic",
        "RNAs, Ro-associated Y",
        "Small Cajal body-specific RNAs",
        "Small NF90 (ILF3) associated RNAs",
        "Small nuclear RNAs",
        "Small nucleolar RNAs, C/D box",
        "Small nucleolar RNAs, H/ACA box",
        "Vault RNAs",
        "L ribosomal proteins",
        "Mitochondrial ribosomal proteins",
        "S ribosomal proteins",
        "Mitochondrial complex II: succinate dehydrogenase subunits",
        "Mitochondrial complex III: ubiquinol-cytochrome c reductase complex subunits",
        "Mitochondrial complex IV: cytochrome c oxidase subunits",
        "Mitochondrial complex V: ATP synthase subunits",
        "NADH:ubiquinone oxidoreductase core subunits",
        "NADH:ubiquinone oxidoreductase supernumerary subunits",
    ),
    locus_type_to_keep=("gene with protein product",),
):

    hgnc = read_csv(
        "{}/../data/hgnc.tsv".format(dirname(__file__)), sep="\t", index_col=0
    )

    removed_by_gene_family_name = asarray(
        tuple(
            not isna(str_)
            and any(removing_str in str_ for removing_str in gene_family_name_to_remove)
            for str_ in hgnc["Gene Family Name"]
        )
    )

    print(
        "Removing {}/{} by gene family name ...".format(
            removed_by_gene_family_name.sum(), removed_by_gene_family_name.size
        )
    )

    kept_by_locus_type = asarray(
        tuple(
            not isna(str_)
            and any(keeping_str in str_ for keeping_str in locus_type_to_keep)
            for str_ in hgnc["Locus Type"]
        )
    )

    print(
        "Keeping {}/{} by locus type ...".format(
            kept_by_locus_type.sum(), kept_by_locus_type.size
        )
    )

    remove = removed_by_gene_family_name | ~kept_by_locus_type

    print("Removing {} ...".format(remove.sum()))

    for column_name in ("Gene Family Name", "Locus Type"):

        df = hgnc.loc[remove, column_name].value_counts().to_frame()

        df.index.name = column_name

        df.columns = ("N Removed",)

    gene_symbols = (
        hgnc.loc[~remove, ["Approved Symbol", "Previous Symbols"]]
        .unstack()
        .dropna()
        .unique()
        .tolist()
    )

    print("Selected {} gene symbols.".format(len(gene_symbols)))

    return gene_symbols
