def clean_git_url(git_url):

    if git_url.endswith("/"):

        git_url = git_url[:-1]

    if git_url.endswith(".git"):

        git_url = git_url[:-4]

    return git_url
