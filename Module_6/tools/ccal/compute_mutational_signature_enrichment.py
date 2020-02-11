from pprint import pprint

from pandas import DataFrame
from pyfaidx import Fasta

from ._count import _count
from ._identify_what_to_count import _identify_what_to_count


def compute_mutational_signature_enrichment(
    mutation_file_paths,
    reference_file_path,
    upper_fasta=True,
    span=20,
    contig_format="",
    contig_intervals=None,
):

    signature_component_weight = {
        "TCA ==> TGA": 1,
        "TCA ==> TTA": 1,
        "TCT ==> TGT": 1,
        "TCT ==> TTT": 1,
        "TGA ==> TCA": 1,
        "TGA ==> TAA": 1,
        "AGA ==> ACA": 1,
        "AGA ==> AAA": 1,
    }

    signature_component_dict, signature_component_differing_dict, signature_component_before_dict, signature_component_before_differing_dict = _identify_what_to_count(
        signature_component_weight
    )

    print("signature_component_dict:")

    pprint(signature_component_dict)

    print("signature_component_differing_dict:")

    pprint(signature_component_differing_dict)

    print("signature_component_before_dict:")

    pprint(signature_component_before_dict)

    print("signature_component_before_differing_dict:")

    pprint(signature_component_before_differing_dict)

    samples = {}

    n_sample = len(mutation_file_paths)

    fasta_handle = Fasta(reference_file_path, sequence_always_upper=upper_fasta)

    print("Reference sequence:")

    pprint(fasta_handle.keys())

    for i, mutation_file_path in enumerate(mutation_file_paths):

        sample = mutation_file_path.split("/")[-1]

        if sample in samples:

            raise ValueError("{} duplicated.".format(sample))

        print("({}/{}) {} ...".format(i + 1, n_sample, sample))

        samples[sample] = _count(
            mutation_file_path,
            fasta_handle,
            span,
            signature_component_dict,
            signature_component_differing_dict,
            signature_component_before_dict,
            signature_component_before_differing_dict,
            contig_format,
            contig_intervals,
        )

    df = DataFrame(samples)

    df.columns.name = "Sample"

    df.loc["TCW"] = df.loc[["TCA", "TCT"]].sum()

    df.loc["TCW ==> TGW"] = df.loc[["TCA ==> TGA", "TCT ==> TGT"]].sum()

    df.loc["TCW ==> TTW"] = df.loc[["TCA ==> TTA", "TCT ==> TTT"]].sum()

    df.loc["WGA"] = df.loc[["AGA", "TGA"]].sum()

    df.loc["WGA ==> WCA"] = df.loc[["AGA ==> ACA", "TGA ==> TCA"]].sum()

    df.loc["WGA ==> WAA"] = df.loc[["AGA ==> AAA", "TGA ==> TAA"]].sum()

    signature_component_weight = (
        df.loc[signature_component_dict.keys()]
        .apply(
            lambda series: series * signature_component_dict[series.name]["weight"],
            axis=1,
        )
        .sum()
    )

    signature_component_differing_weight = (
        df.loc[signature_component_differing_dict.keys()]
        .apply(
            lambda series: series
            * signature_component_differing_dict[series.name]["weight"],
            axis=1,
        )
        .sum()
    )

    signature_component_before_weight = (
        df.loc[signature_component_before_dict.keys()]
        .apply(
            lambda series: series
            * signature_component_before_dict[series.name]["weight"],
            axis=1,
        )
        .sum()
    )

    signature_component_before_differing_weight = (
        df.loc[signature_component_before_differing_dict.keys()]
        .apply(
            lambda series: series
            * signature_component_before_differing_dict[series.name]["weight"],
            axis=1,
        )
        .sum()
    )

    mutational_signature_enrichment = (
        signature_component_weight / signature_component_before_weight
    ) / (
        signature_component_differing_weight
        / signature_component_before_differing_weight
    )

    df.loc[
        "Mutational Signature Enrichment"
    ] = mutational_signature_enrichment  # .fillna(value=0)

    return df
