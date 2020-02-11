from .add_conda_to_path import add_conda_to_path
from .conda_is_installed import conda_is_installed
from .download import download
from .get_machine import get_machine
from .run_command import run_command


def install_and_activate_conda(
    conda_directory_path, pip_installs=None, conda_installs=None
):

    if not conda_is_installed(conda_directory_path):

        conda_script_file_name_template = "Miniconda3-latest-{}-x86_64.sh"

        machine = get_machine()

        if "Darwin" in machine:

            str_ = "MacOSX"

        elif "Linux" in machine:

            str_ = "Linux"

        else:

            raise ValueError("Unknown machine: {}.".format(machine))

        conda_script_file_name = conda_script_file_name_template.format(str_)

        tmp_directory_path = "{}/{}".format("/", "tmp")

        download(
            "https://repo.continuum.io/miniconda/{}".format(conda_script_file_name),
            tmp_directory_path,
        )

        run_command(
            "bash {}/{} -b -p {}".format(
                tmp_directory_path, conda_script_file_name, conda_directory_path
            ),
            print_command=True,
        )

    add_conda_to_path(conda_directory_path)

    if pip_installs is not None:

        run_command("pip install {}".format(" ".join(pip_installs)), print_command=True)

    if conda_installs is not None:

        for channel, packages in conda_installs.items():

            run_command(
                "conda install --channel {} --yes {}".format(
                    channel, " ".join(packages)
                ),
                print_command=True,
            )
