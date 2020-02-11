import ssl
from os import getcwd
from urllib.request import urlretrieve

from .echo_or_print import echo_or_print


def download(url, directory_path=getcwd()):

    file_name = url.split(sep="/")[-1].split(sep="?")[0]

    file_path = "{}/{}".format(directory_path, file_name)

    echo_or_print("Downloading {} =(into)=> {} ...".format(url, file_path))

    ssl._create_default_https_context = ssl._create_unverified_context

    urlretrieve(url, file_path)

    return file_path
