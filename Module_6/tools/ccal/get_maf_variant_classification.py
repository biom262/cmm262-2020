from warnings import warn

from .get_variant_type import get_variant_type
from .is_inframe import is_inframe


def get_maf_variant_classification(effect, ref, alt):

    variant_type = get_variant_type(ref, alt)

    inframe = is_inframe(ref, alt)

    if effect in (
        "transcript_ablation",
        "exon_loss_variant",
        "splice_acceptor_variant",
        "splice_donor_variant",
    ):

        variant_classification = "Splice_Site"

    elif effect in ("stop_gained",):

        variant_classification = "Nonsense_Mutation"

    elif variant_type == "INS" and (
        effect in ("frameshift_variant",)
        or (
            not inframe
            and effect in ("protein_protein_contact", "protein_altering_variant")
        )
    ):

        variant_classification = "Frame_Shift_Ins"

    elif variant_type == "DEL" and (
        effect in ("frameshift_variant",)
        or (
            not inframe
            and effect in ("protein_protein_contact", "protein_altering_variant")
        )
    ):

        variant_classification = "Frame_Shift_Del"

    elif effect in ("stop_lost",):

        variant_classification = "Nonstop_Mutation"

    elif effect in ("start_lost", "initiator_codon_variant"):

        variant_classification = "Translation_Start_Site"

    elif (
        variant_type == "INS"
        and inframe
        and effect
        in (
            "protein_protein_contact",
            "disruptive_inframe_insertion",
            "inframe_insertion",
            "protein_altering_variant",
        )
    ):

        variant_classification = "In_Frame_Ins"

    elif (
        variant_type == "DEL"
        and inframe
        and effect
        in (
            "protein_protein_contact",
            "disruptive_inframe_deletion",
            "inframe_deletion",
            "protein_altering_variant",
        )
    ):

        variant_classification = "In_Frame_Del"

    elif effect in (
        "transcript_variant",
        "conservative_missense_variant",
        "rare_amino_acid_variant",
        "missense_variant",
        "coding_sequence_variant",
    ) or (
        variant_type not in ("INS", "DEL") and effect in ("protein_protein_contact",)
    ):

        variant_classification = "Missense_Mutation"

    elif effect in (
        "transcript_amplification",
        "splice_region_variant",
        "intragenic_variant",
        "conserved_intron_variant",
        "intron_variant",
        "INTRAGENIC",
    ):

        variant_classification = "Intron"

    elif effect in (
        "incomplete_terminal_codon_variant",
        "start_retained_variant",
        "stop_retained_variant",
        "synonymous_variant",
        "NMD_transcript_variant",
    ):

        variant_classification = "Silent"

    elif effect in (
        "exon_variant",
        "mature_miRNA_variant",
        "non_coding_exon_variant",
        "non_coding_transcript_exon_variant",
        "non_coding_transcript_variant",
        "nc_transcript_variant",
    ):

        variant_classification = "RNA"

    elif effect in (
        "5_prime_UTR_variant",
        "5_prime_UTR_premature_start_codon_gain_variant",
    ):

        variant_classification = "5'UTR"

    elif effect in ("3_prime_UTR_variant",):

        variant_classification = "3'UTR"

    elif effect in (
        "TF_binding_site_ablation",
        "TFBS_ablation",
        "TF_binding_site_amplification",
        "TFBS_amplification",
        "TF_binding_site_variant",
        "TFBS_variant",
        "regulatory_region_ablation",
        "regulatory_region_amplification",
        "regulatory_region_variant",
        "regulatory_region",
        "feature_elongation",
        "feature_truncation",
        "conserved_intergenic_variant",
        "intergenic_variant",
        "intergenic_region",
    ):

        variant_classification = "IGR"

    elif effect in ("upstream_gene_variant",):

        variant_classification = "5'Flank"

    elif effect in ("downstream_gene_variant",):

        variant_classification = "3'Flank"

    elif effect in ("sequence_feature",):

        variant_classification = "Targeted_Region"

    else:

        warn(
            "No variant classification for: effect={} & variant_type={} & inframe={}.".format(
                effect, variant_type, inframe
            )
        )

        variant_classification = "Targeted_Region"

    return variant_classification
