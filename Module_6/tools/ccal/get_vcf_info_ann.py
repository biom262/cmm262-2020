from .get_vcf_info import get_vcf_info
from .VCF_ANN_FIELDS import VCF_ANN_FIELDS


def get_vcf_info_ann(info, field, n_ann=None):

    ann = get_vcf_info(info, "ANN")

    if ann:

        field_index = VCF_ANN_FIELDS.index(field)

        return [ann_.split(sep="|")[field_index] for ann_ in ann.split(sep=",")[:n_ann]]

    else:

        return []
