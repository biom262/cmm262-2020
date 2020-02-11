from .concatenate_vcf_gzs_using_bcftools_concat import (
    concatenate_vcf_gzs_using_bcftools_concat,
)
from .get_variants_from_bam_using_freebayes import get_variants_from_bam_using_freebayes
from .multiprocess import multiprocess


def get_variants_from_bam_using_freebayes_and_multiprocess(
    bam_file_path,
    fasta_file_path,
    regions,
    n_job=1,
    output_vcf_file_path=None,
    overwrite=False,
):

    return concatenate_vcf_gzs_using_bcftools_concat(
        multiprocess(
            get_variants_from_bam_using_freebayes,
            (
                (bam_file_path, fasta_file_path, region, 1, None, overwrite)
                for region in regions
            ),
            n_job=n_job,
        ),
        remove_input_vcf_gz_file_paths_and_their_indices=True,
        n_job=n_job,
        output_vcf_file_path=output_vcf_file_path,
        overwrite=overwrite,
    )
