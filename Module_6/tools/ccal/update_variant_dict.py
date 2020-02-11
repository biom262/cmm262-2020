from .get_allelic_frequencies import get_allelic_frequencies
from .get_genotype import get_genotype
from .get_maf_variant_classification import get_maf_variant_classification
from .get_population_allelic_frequencies import get_population_allelic_frequencies
from .get_variant_start_and_end_positions import get_variant_start_and_end_positions
from .get_variant_type import get_variant_type


def update_variant_dict(variant_dict):

    ref = variant_dict["REF"]

    alt = variant_dict["ALT"]

    variant_dict["variant_type"] = get_variant_type(ref, alt)

    start_position, end_position = get_variant_start_and_end_positions(
        int(variant_dict["POS"]), ref, alt
    )

    variant_dict["start_position"] = start_position

    variant_dict["end_position"] = end_position

    caf = variant_dict.get("CAF")

    if caf:

        variant_dict[
            "population_allelic_frequencies"
        ] = get_population_allelic_frequencies(caf)

    for ann_dict in variant_dict["ANN"].values():

        ann_dict["variant_classification"] = get_maf_variant_classification(
            ann_dict["effect"], ref, alt
        )

    for sample_dict in variant_dict["sample"].values():

        if "GT" in sample_dict:

            sample_dict["genotype"] = get_genotype(ref, alt, sample_dict["GT"])

        if "AD" in sample_dict and "DP" in sample_dict:

            sample_dict["allelic_frequency"] = get_allelic_frequencies(
                sample_dict["AD"], sample_dict["DP"]
            )
