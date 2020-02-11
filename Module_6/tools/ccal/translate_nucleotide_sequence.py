from .CODON_TO_AMINO_ACID import CODON_TO_AMINO_ACID
from .reverse_complement_dna_sequence import reverse_complement_dna_sequence
from .split_codons import split_codons
from .transcribe_dna_sequence import transcribe_dna_sequence


def translate_nucleotide_sequence(
    nucleotide_sequence,
    nucleotide_type,
    reading_frame_offset=0,
    reading_frame_direction=1,
):

    if nucleotide_type == "DNA":

        if reading_frame_direction == -1:

            nucleotide_sequence = reverse_complement_dna_sequence(nucleotide_sequence)

        nucleotide_sequence = transcribe_dna_sequence(nucleotide_sequence)

    return "".join(
        CODON_TO_AMINO_ACID[codon]
        for codon in split_codons(
            nucleotide_sequence, reading_frame_offset=reading_frame_offset
        )
    )
