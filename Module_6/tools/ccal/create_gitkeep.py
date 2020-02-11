def create_gitkeep(directory_path):

    gitkeep_file_path = "{}/.gitkeep".format(directory_path)

    open(gitkeep_file_path, mode="w").close()

    print("Created {}.".format(gitkeep_file_path))
