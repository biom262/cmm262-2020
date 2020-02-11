from .get_vcf_sample_format import get_vcf_sample_format


def _describe_vcf_df(vcf_df):

    print("\nCHROM value counts:")

    print(vcf_df["CHROM"].value_counts())

    print("\nREF value counts:")

    print(vcf_df["REF"].value_counts())

    print("\nALT value counts:")

    print(vcf_df["ALT"].value_counts())

    print("\nQUAL description:")

    qual = vcf_df["QUAL"]

    qual = qual[qual.astype(str) != "."]

    print(qual.astype(float).describe())

    for sample in vcf_df.columns[9:]:

        print("\n{} GT value counts:".format(sample))

        try:

            print(
                vcf_df.apply(
                    lambda row: get_vcf_sample_format(row["FORMAT"], row[sample], "GT"),
                    axis=1,
                ).value_counts()
            )

        except ValueError:

            pass

        print("\n{} DP description:".format(sample))

        try:

            print(
                vcf_df.apply(
                    lambda row: get_vcf_sample_format(row["FORMAT"], row[sample], "DP"),
                    axis=1,
                )
                .astype(int)
                .describe()
            )

        except ValueError:

            pass
