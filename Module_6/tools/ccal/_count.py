import copy
import re
from warnings import warn

from pandas import read_csv

from .normalize_contig import normalize_contig


def _count(
    mutation_file_path,
    fasta_handle,
    span,
    signature_component_dict,
    signature_component_differing_dict,
    signature_component_before_dict,
    signature_component_before_differing_dict,
    contig_format,
    contig_intervals,
):

    if mutation_file_path.endswith((".vcf", ".vcf.gz")):

        column_indices = [0, 1, 3, 4]

    elif mutation_file_path.endswith((".maf", ".maf.txt")):

        column_indices = [4, 5, 10, 12]

    df = read_csv(
        mutation_file_path, encoding="iso-8859-1", comment="#", sep="\t"
    ).iloc[:, column_indices]

    signature_component_dict_ = copy.deepcopy(signature_component_dict)

    signature_component_differing_dict_ = copy.deepcopy(
        signature_component_differing_dict
    )

    signature_component_before_dict_ = copy.deepcopy(signature_component_before_dict)

    signature_component_before_differing_dict_ = copy.deepcopy(
        signature_component_before_differing_dict
    )

    n_mutation_in_region = 0

    n_mutation_analyzed = 0

    n_spanning_base = 0

    for i, (chr_, pos, ref, alt) in df.iterrows():

        chr_ = normalize_contig(chr_, contig_format)

        pos = int(pos) - 1

        if contig_intervals is not None:

            start_end = contig_intervals.get(chr_)

            if start_end is None or not any(
                start <= pos <= end for start, end in start_end
            ):

                warn("Not in the contig_intervals: {}:{}.".format(chr_, pos))

                continue

        n_mutation_in_region += 1

        if chr_ not in fasta_handle.keys():

            warn("Not in the reference sequence: {}.".format(chr_))

            continue

        if not len(ref) == len(alt) == 1 or "-" in (ref, alt):

            warn("Not SNV: {} ==> {}.".format(ref, alt))

            continue

        if ref != fasta_handle[chr_][pos].seq:

            warn(
                "Mismatch reference sequence: {}:{} {} != ({}){}({}).".format(
                    chr_, pos, ref, *fasta_handle[chr_][pos - 1 : pos + 2].seq
                )
            )

            continue

        start_pos = max(0, pos - span)

        end_pos = pos + span

        span_seq = fasta_handle[chr_][start_pos : end_pos + 1].seq

        span_seq = span_seq.strip("N")

        if re.findall("[^AaCcGgTt]", span_seq):

            warn(
                "{} (centered on {}:{}) contains at least 1 nucleotide that is not AaCcGgTt.".format(
                    span_seq, chr_, pos
                )
            )

            continue

        n_mutation_analyzed += 1

        n_spanning_base += len(span_seq)

        for signature_component, dict_ in signature_component_dict_.items():

            signature_component_before_sequence = dict_.get("before_sequence")

            signature_component_after_sequence = dict_.get("after_sequence")

            if (
                signature_component_before_sequence
                == fasta_handle[chr_][pos - 1 : pos + 2].seq
                and alt == signature_component_after_sequence[1]
            ):

                dict_["n"] += 1

        for (
            signature_component_differing,
            dict_,
        ) in signature_component_differing_dict_.items():

            if ref == dict_.get("before_sequence") and alt == dict_.get(
                "after_sequence"
            ):

                dict_["n"] += 1

        for signature_component_before in signature_component_before_dict_:

            signature_component_before_dict_[signature_component_before][
                "n"
            ] += span_seq.count(signature_component_before)

        for (
            signature_component_before_differing
        ) in signature_component_before_differing_dict_:

            signature_component_before_differing_dict_[
                signature_component_before_differing
            ]["n"] += span_seq.count(signature_component_before_differing)

    counts = {
        "N Entry in Mutation File": i + 1,
        "N Mutation in Region": n_mutation_in_region,
        "N Mutation Analyzed": n_mutation_analyzed,
        "N Spanning Base": n_spanning_base,
    }

    counts.update(
        {
            signature_component: dict_["n"]
            for signature_component, dict_ in signature_component_dict_.items()
        }
    )

    counts.update(
        {
            signature_component_differing: dict_["n"]
            for signature_component_differing, dict_ in signature_component_differing_dict_.items()
        }
    )

    counts.update(
        {
            signature_component_before: dict_["n"]
            for signature_component_before, dict_ in signature_component_before_dict_.items()
        }
    )

    counts.update(
        {
            signature_component_before_differing: dict_["n"]
            for signature_component_before_differing, dict_ in signature_component_before_differing_dict_.items()
        }
    )

    return counts
