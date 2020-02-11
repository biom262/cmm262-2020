from .count_vcf_gz_rows import count_vcf_gz_rows


def is_valid_vcf_gz(vcf_gz_file_path):

    counts = count_vcf_gz_rows(vcf_gz_file_path, format_fields_to_count=("GT",))

    return counts["n"] == counts["GT"]
