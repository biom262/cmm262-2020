from pandas import DataFrame, read_csv

from .get_maf_variant_classification import get_maf_variant_classification
from .get_variant_start_and_end_positions import get_variant_start_and_end_positions
from .get_variant_type import get_variant_type
from .get_vcf_info_ann import get_vcf_info_ann
from .read_vcf_gz_and_make_vcf_dict import read_vcf_gz_and_make_vcf_dict


def make_maf_from_vcf(
    vcf_file_path, ensg_entrez, sample_name="Sample", maf_file_path=None
):

    vcf_df = read_vcf_gz_and_make_vcf_dict(vcf_file_path, simplify=False)["vcf_df"]

    maf_df = DataFrame(
        index=vcf_df.index,
        columns=(
            "Hugo_Symbol",
            "Entrez_Gene_Id",
            "Center",
            "NCBI_Build",
            "Chromosome",
            "Start_Position",
            "End_Position",
            "Strand",
            "Variant_Classification",
            "Variant_Type",
            "Reference_Allele",
            "Tumor_Seq_Allele1",
            "Tumor_Seq_Allele2",
            "dbSNP_RS",
            "dbSNP_Val_Status",
            "Tumor_Sample_Barcode",
            "Matched_Norm_Sample_Barcode",
            "Matched_Norm_Seq_Allele1",
            "Matched_Norm_Seq_Allele2",
            "Tumor_Validation_Allele1",
            "Tumor_Validation_Allele2",
            "Match_Norm_Validation_Allele1",
            "Match_Norm_Validation_Allele2",
            "Verification_Status",
            "Validation_Status",
            "Mutation_Status",
            "Sequencing_Phase",
            "Sequence_Source",
            "Validation_Method",
            "Score",
            "BAM_File",
            "Sequencer",
            "Tumor_Sample_UUID",
            "Matched_Norm_Sample_UUID",
        ),
    )

    ensg_entrez_dict = read_csv(
        ensg_entrez, sep="\t", index_col=0, squeeze=True
    ).to_dict()

    print("Iterating through .vcf file DataFrame rows ...")

    n = vcf_df.shape[0]

    n_per_print = max(1, n // 10)

    for i, row in vcf_df.iterrows():

        if i % n_per_print == 0:

            print("\t{}/{} ...".format(i + 1, n))

        chrom, pos, id_, ref, alt, info = row[[0, 1, 2, 3, 4, 7]]

        gene_name = get_vcf_info_ann(info, "gene_name")[0]

        gene_id = get_vcf_info_ann(info, "gene_id")[0]

        entrez_gene_id = ensg_entrez_dict.get(gene_id)

        effect = get_vcf_info_ann(info, "effect")[0]

        variant_classification = get_maf_variant_classification(effect, ref, alt)

        start_position, end_position = get_variant_start_and_end_positions(
            int(pos), ref, alt
        )

        variant_type = get_variant_type(ref, alt)

        maf_df.loc[
            i,
            [
                "Hugo_Symbol",
                "Entrez_Gene_Id",
                "Chromosome",
                "Start_Position",
                "End_Position",
                "Variant_Classification",
                "Variant_Type",
                "dbSNP_RS",
                "Reference_Allele",
                "Tumor_Seq_Allele1",
            ],
        ] = (
            gene_name,
            entrez_gene_id,
            chrom,
            start_position,
            end_position,
            variant_classification,
            variant_type,
            id_,
            ref,
            alt,
        )

    maf_df["Strand"] = "+"

    maf_df[
        [
            "Tumor_Sample_Barcode",
            "Matched_Norm_Sample_Barcode",
            "Tumor_Sample_UUID",
            "Matched_Norm_Sample_UUID",
        ]
    ] = sample_name

    if maf_file_path is not None:

        maf_df.to_csv(maf_file_path, sep="\t", index=None)

    return maf_df
