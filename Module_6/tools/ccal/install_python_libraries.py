from .get_installed_pip_libraries import get_installed_pip_libraries
from .run_command import run_command


def install_python_libraries(libraries):

    libraries_installed = get_installed_pip_libraries()

    for library in libraries:

        if library not in libraries_installed:

            run_command("pip install {}".format(library), print_command=True)

        else:

            print("{} is already installed.".format(library))
