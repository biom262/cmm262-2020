def split_codons(nucleotide_sequence, reading_frame_offset=0):

    codons = []

    for i in range(int((len(nucleotide_sequence) - reading_frame_offset) / 3)):

        codons.append(
            nucleotide_sequence[
                i * 3 + reading_frame_offset : (i + 1) * 3 + reading_frame_offset
            ]
        )

    return codons
