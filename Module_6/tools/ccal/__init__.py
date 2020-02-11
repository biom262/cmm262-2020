from os.path import abspath

VERSION = "0.9.4"
print("CCAL version {} @ {}".format(VERSION, abspath(__file__)))
from .ALMOST_ZERO import ALMOST_ZERO
from .BAD_VARIANT_IDS import BAD_VARIANT_IDS
from .CODON_TO_AMINO_ACID import CODON_TO_AMINO_ACID
from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .COLOR_RUBY_EMERALD import COLOR_RUBY_EMERALD
from .COLOR_WHITE_BLACK import COLOR_WHITE_BLACK
from .COLOR_WHITE_BROWN import COLOR_WHITE_BROWN
from .DATA_DIRECTORY_PATH import DATA_DIRECTORY_PATH
# from .FeatureHDF5 import FeatureHDF5
# from .GPSMap import GPSMap
# from .Genome import Genome
from .VARIANT_CLASSIFICATION_MUTSIG_EFFECT import VARIANT_CLASSIFICATION_MUTSIG_EFFECT
from .VARIANT_EFFECTS import VARIANT_EFFECTS
from .VCF_ANN_FIELDS import VCF_ANN_FIELDS
from .VCF_COLUMNS import VCF_COLUMNS
# from .VariantHDF5 import VariantHDF5
from ._anneal_node_and_element_positions import _anneal_node_and_element_positions
from ._check_fastq_gzs import _check_fastq_gzs
from ._check_node_x_element import _check_node_x_element
from ._check_w_or_h import _check_w_or_h
from ._cluster_clustering_x_element_and_compute_ccc import (
    _cluster_clustering_x_element_and_compute_ccc,
)
from ._compute_context_indices import _compute_context_indices
from ._compute_norm import _compute_norm
from ._count import _count
from ._describe_vcf_df import _describe_vcf_df
from ._fit_skew_t_pdfs import _fit_skew_t_pdfs
from ._get_coclustering_portion import _get_coclustering_portion
from ._get_target_grid_indices import _get_target_grid_indices
from ._get_triangulation_edges import _get_triangulation_edges
from ._gzip_compress import _gzip_compress
from ._identify_what_to_count import _identify_what_to_count
from ._ignore_bad_and_compute_euclidean_distance_between_2_1d_arrays import (
    _ignore_bad_and_compute_euclidean_distance_between_2_1d_arrays,
)
from ._make_annotations import _make_annotations
from ._make_clean_vcf_df import _make_clean_vcf_df
from ._make_context_matrix import _make_context_matrix
from ._make_element_x_dimension import _make_element_x_dimension
from ._make_grid_values_and_categorical_labels import (
    _make_grid_values_and_categorical_labels,
)
from ._make_variant_dict_consistent import _make_variant_dict_consistent
from ._match import _match
from ._match_randomly_sampled_target_and_data_to_compute_margin_of_errors import (
    _match_randomly_sampled_target_and_data_to_compute_margin_of_errors,
)
from ._match_target_and_data import _match_target_and_data
from ._normalize_nd_array import _normalize_nd_array
from ._permute_target_and_match_target_and_data import (
    _permute_target_and_match_target_and_data,
)
from ._plot_2d import _plot_2d
from ._plot_gps_map import _plot_gps_map
from ._plot_mountain import _plot_mountain
from ._print_and_run_command import _print_and_run_command
from ._process_target_or_data_for_plotting import _process_target_or_data_for_plotting
from ._single_sample_gseas import _single_sample_gseas
from ._ssGSEA import _ssGSEA
from ._update_H_by_multiplicative_update import _update_H_by_multiplicative_update
from ._update_W_by_multiplicative_update import _update_W_by_multiplicative_update
from .add_conda_to_path import add_conda_to_path
from .align_fastq_gzs_using_bwa_mem import align_fastq_gzs_using_bwa_mem
from .align_fastq_gzs_using_hisat2 import align_fastq_gzs_using_hisat2
from .annotate_vcf_gz_using_bcftools_annotate import (
    annotate_vcf_gz_using_bcftools_annotate,
)
from .annotate_vcf_gz_using_snpeff import annotate_vcf_gz_using_snpeff
from .apply_function_on_2_1d_arrays import apply_function_on_2_1d_arrays
from .apply_function_on_2_2d_arrays_slices import apply_function_on_2_2d_arrays_slices
from .bgzip_and_tabix import bgzip_and_tabix
from .cast_series_to_builtins import cast_series_to_builtins
from .cast_str_to_builtins import cast_str_to_builtins
from .check_bam_using_samtools_flagstat import check_bam_using_samtools_flagstat
from .check_fastq_gzs_using_fastqc import check_fastq_gzs_using_fastqc
from .check_nd_array_for_bad import check_nd_array_for_bad
from .clean_and_write_df_to_tsv import clean_and_write_df_to_tsv
from .clean_git_url import clean_git_url
from .clean_name import clean_name
from .clean_path import clean_path
from .clip_nd_array_by_standard_deviation import clip_nd_array_by_standard_deviation
from .cluster_2d_array_slices import cluster_2d_array_slices
from .compute_bandwidths import compute_bandwidths
from .compute_context import compute_context
from .compute_correlation_distance import compute_correlation_distance
from .compute_empirical_p_value import compute_empirical_p_value
from .compute_empirical_p_values_and_fdrs import compute_empirical_p_values_and_fdrs
from .compute_entropy import compute_entropy
from .compute_information_coefficient import compute_information_coefficient
from .compute_information_distance import compute_information_distance
from .compute_joint_probability import compute_joint_probability
from .compute_kullback_leibler_divergence import compute_kullback_leibler_divergence
# from .compute_mutational_signature_enrichment import (
#     compute_mutational_signature_enrichment,
# )
from .compute_nd_array_margin_of_error import compute_nd_array_margin_of_error
from .compute_posterior_probability import compute_posterior_probability
from .concatenate_vcf_gzs_using_bcftools_concat import (
    concatenate_vcf_gzs_using_bcftools_concat,
)
from .conda_is_installed import conda_is_installed
from .copy_path import copy_path
from .correlate import correlate
from .count_gene_impacts_from_variant_dicts import count_gene_impacts_from_variant_dicts
from .count_transcripts_using_kallisto_quant import (
    count_transcripts_using_kallisto_quant,
)
from .count_vcf_gz_rows import count_vcf_gz_rows
from .create_gitkeep import create_gitkeep
from .cross_validate import cross_validate
# from .download import download
# from .download_and_parse_geo_data import download_and_parse_geo_data
# from .download_clinvar_vcf_gz import download_clinvar_vcf_gz
from .drop_df_slice import drop_df_slice
from .drop_df_slice_greedily import drop_df_slice_greedily
from .dump_gps_map import dump_gps_map
# from .echo_or_print import echo_or_print
from .establish_fai_index import establish_fai_index
from .establish_path import establish_path
from .estimate_kernel_density import estimate_kernel_density
# from .exit_ import exit_
from .faidx_fasta import faidx_fasta
from .filter_vcf_gz_using_bcftools_view import filter_vcf_gz_using_bcftools_view
from .fit_skew_t_pdf import fit_skew_t_pdf
from .fit_skew_t_pdfs import fit_skew_t_pdfs
from .flatten_nested_iterable import flatten_nested_iterable
from .get_1d_array_unique_objects_in_order import get_1d_array_unique_objects_in_order
from .get_allelic_frequencies import get_allelic_frequencies
from .get_chromosome_size_from_fasta_gz import get_chromosome_size_from_fasta_gz
from .get_colormap_colors import get_colormap_colors
from .get_conda_environments import get_conda_environments
from .get_conda_prefix import get_conda_prefix
from .get_function_name import get_function_name
from .get_genotype import get_genotype
from .get_gff3_attribute import get_gff3_attribute
from .get_git_versions import get_git_versions
from .get_installed_pip_libraries import get_installed_pip_libraries
from .get_intersections_between_2_1d_arrays import get_intersections_between_2_1d_arrays
from .get_machine import get_machine
from .get_maf_variant_classification import get_maf_variant_classification
from .get_now import get_now
from .get_object_reference import get_object_reference
from .get_open_port import get_open_port
from .get_population_allelic_frequencies import get_population_allelic_frequencies
from .get_sequence_from_fasta_gz import get_sequence_from_fasta_gz
from .get_shell_environment import get_shell_environment
from .get_unique_iterable_objects_in_order import get_unique_iterable_objects_in_order
from .get_variant_start_and_end_positions import get_variant_start_and_end_positions
from .get_variant_type import get_variant_type
from .get_variants_from_bam_using_freebayes import get_variants_from_bam_using_freebayes
from .get_variants_from_bam_using_freebayes_and_multiprocess import (
    get_variants_from_bam_using_freebayes_and_multiprocess,
)
from .get_variants_from_bam_using_strelka import get_variants_from_bam_using_strelka
# from .get_variants_from_vcf_gz import get_variants_from_vcf_gz
from .get_vcf_info import get_vcf_info
from .get_vcf_info_ann import get_vcf_info_ann
from .get_vcf_sample_format import get_vcf_sample_format
from .get_volume_name import get_volume_name
from .group_and_apply_function_on_each_group_in_iterable import (
    group_and_apply_function_on_each_group_in_iterable,
)
from .group_iterable import group_iterable
from .gsea import gsea
from .gzip_compress_file import gzip_compress_file
# from .gzip_decompress_and_bgzip_compress_file import (
#     gzip_decompress_and_bgzip_compress_file,
# )
from .gzip_decompress_file import gzip_decompress_file
from .have_program import have_program
from .hierarchical_consensus_cluster import hierarchical_consensus_cluster
from .hierarchical_consensus_cluster_with_ks import (
    hierarchical_consensus_cluster_with_ks,
)
# from .in_git_repository import in_git_repository
from .index_bam_using_samtools_index import index_bam_using_samtools_index
from .index_gff3_df_by_name import index_gff3_df_by_name
from .infer import infer
from .infer_assuming_independence import infer_assuming_independence
from .initialize_logger import initialize_logger
# from .install_and_activate_conda import install_and_activate_conda
from .install_python_libraries import install_python_libraries
from .is_inframe import is_inframe
from .is_valid_vcf_gz import is_valid_vcf_gz
from .load_gps_map import load_gps_map
from .log_and_return_response import log_and_return_response
from .log_nd_array import log_nd_array
from .make_categorical_colors import make_categorical_colors
from .make_colorscale import make_colorscale
from .make_colorscale_from_colors import make_colorscale_from_colors
from .make_comparison_panel import make_comparison_panel
from .make_context_matrix import make_context_matrix
from .make_coordinates_for_reflection import make_coordinates_for_reflection
from .make_file_name_from_str import make_file_name_from_str
from .make_maf_from_vcf import make_maf_from_vcf
from .make_match_panel import make_match_panel
from .make_match_panels import make_match_panels
from .make_membership_df_from_categorical_series import (
    make_membership_df_from_categorical_series,
)
from .make_mesh_grid_coordinates_per_axis import make_mesh_grid_coordinates_per_axis
from .make_object_int_mapping import make_object_int_mapping
from .make_random_color import make_random_color
# from .make_reference_genome import make_reference_genome
from .make_summary_match_panel import make_summary_match_panel
from .make_volume_dict import make_volume_dict
from .map_cell_line_names import map_cell_line_names
from .mark_duplicates_in_bam_using_picard_markduplicates import (
    mark_duplicates_in_bam_using_picard_markduplicates,
)
from .mds import mds
from .merge_dicts_with_callable import merge_dicts_with_callable
from .mf_by_multiplicative_update import mf_by_multiplicative_update
from .mf_consensus_cluster import mf_consensus_cluster
from .mf_consensus_cluster_with_ks import mf_consensus_cluster_with_ks
from .mount_volume import mount_volume
from .multiprocess import multiprocess
from .nd_array_is_sorted import nd_array_is_sorted
from .nmf_by_multiple_V_and_H import nmf_by_multiple_V_and_H
from .nmf_by_sklearn import nmf_by_sklearn
from .normalize_contig import normalize_contig
from .normalize_df import normalize_df
from .normalize_nd_array import normalize_nd_array
from .parse_vcf_row_and_make_variant_dict import parse_vcf_row_and_make_variant_dict
from .plot_and_save import plot_and_save
from .plot_bar import plot_bar
from .plot_bayesian_nomogram import plot_bayesian_nomogram
from .plot_bubble_map import plot_bubble_map
from .plot_color_text import plot_color_text
from .plot_context import plot_context
from .plot_distributions import plot_distributions
from .plot_heat_map import plot_heat_map
from .plot_pie import plot_pie
from .plot_points import plot_points
from .plot_table import plot_table
from .plot_violin_or_box import plot_violin_or_box
from .process_feature_x_sample import process_feature_x_sample
from .read_copynumber_gistic2 import read_copynumber_gistic2
from .read_correlate_copynumber_vs_mrnaseq import read_correlate_copynumber_vs_mrnaseq
from .read_gct import read_gct
from .read_gff3_gz import read_gff3_gz
from .read_gmt import read_gmt
from .read_gmts import read_gmts
from .read_json import read_json
from .read_matrix_market import read_matrix_market
from .read_mutsignozzlereport2cv import read_mutsignozzlereport2cv
from .read_vcf_gz_and_make_vcf_dict import read_vcf_gz_and_make_vcf_dict
from .read_where_and_map_column_names import read_where_and_map_column_names
from .reboot_machine import reboot_machine
from .remove_path import remove_path
from .remove_paths import remove_paths
from .rename_chromosome_of_vcf_gz_using_bcftools_annotate import (
    rename_chromosome_of_vcf_gz_using_bcftools_annotate,
)
from .replace_bad_objects_in_iterable import replace_bad_objects_in_iterable
from .rescale_x_y_coordiantes_in_polar_coordiante import (
    rescale_x_y_coordiantes_in_polar_coordiante,
)
from .reverse_complement_dna_sequence import reverse_complement_dna_sequence
from .reverse_transcribe_rna_sequence import reverse_transcribe_rna_sequence
from .run_command import run_command
# from .run_command_and_monitor import run_command_and_monitor
from .sample_series_randomly_per_value import sample_series_randomly_per_value
from .select_gene_symbol import select_gene_symbol
from .select_series_indices import select_series_indices
from .select_tcga_sample_by_sample_type_and_group import (
    select_tcga_sample_by_sample_type_and_group,
)
from .shuffle_each_2d_array_slice import shuffle_each_2d_array_slice
from .shutdown_machine import shutdown_machine
from .simulate_sequences_using_dwgsim import simulate_sequences_using_dwgsim
from .single_sample_gsea import single_sample_gsea
from .single_sample_gseas import single_sample_gseas
from .core_GSEA import core_GSEA
from .ssGSEA import ssGSEA
from .solve_ax_equal_b import solve_ax_equal_b
from .solve_for_H import solve_for_H
from .sort_and_index_bam_using_samtools_sort_and_index import (
    sort_and_index_bam_using_samtools_sort_and_index,
)
from .split_codons import split_codons
from .split_df import split_df
from .split_maf_by_tumor_sample_barcode import split_maf_by_tumor_sample_barcode
from .split_str_ignoring_inside_quotes import split_str_ignoring_inside_quotes
from .str_is_version import str_is_version
from .summarize_feature_x_sample import summarize_feature_x_sample
from .title_str import title_str
from .train_and_classify import train_and_classify
from .train_and_regress import train_and_regress
from .transcribe_dna_sequence import transcribe_dna_sequence
from .translate_nucleotide_sequence import translate_nucleotide_sequence
from .trim_fastq_gzs_using_skewer import trim_fastq_gzs_using_skewer
from .unmount_volume import unmount_volume
from .untitle_str import untitle_str
from .update_variant_dict import update_variant_dict
from .write_dict import write_dict
from .write_gct import write_gct
from .write_gmt import write_gmt
from .write_json import write_json
