from os.path import isdir

from ._print_and_run_command import _print_and_run_command


def get_variants_from_bam_using_strelka(
    bam_file_path, fasta_file_path, output_directory_path, n_job=1, overwrite=False
):

    if isdir(output_directory_path):

        if overwrite:

            _print_and_run_command(
                "rm --recursive --force {}".format(output_directory_path)
            )

        else:

            raise FileExistsError(output_directory_path)

    bash_file_path = "/tmp/strelka.sh"

    with open(bash_file_path, "w") as bash_file:

        bash_file.write("source activate sequencing_process_python2.7 &&\n")

        bash_file.write(
            "configureStrelkaGermlineWorkflow.py --bam {} --referenceFasta {} --runDir {} &&\n".format(
                bam_file_path, fasta_file_path, output_directory_path
            )
        )

        bash_file.write(
            "{}/runWorkflow.py --mode local --jobs {}\n".format(
                output_directory_path, n_job
            )
        )

    _print_and_run_command("bash {}".format(bash_file_path))

    stats_file_path = "{}/results/stats/runStats.tsv".format(output_directory_path)

    print("{}:".format(stats_file_path))

    with open(stats_file_path) as stats_file:

        print(stats_file.read())

    return "{}/results/variants/variants.vcf.gz".format(output_directory_path)
