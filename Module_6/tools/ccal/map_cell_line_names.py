from pandas import read_csv

from .DATA_DIRECTORY_PATH import DATA_DIRECTORY_PATH


def map_cell_line_names(cell_line_names):

    cell_line_name_best_cell_line_name = read_csv(
        "{}/cell_line_name_best_cell_line_name.tsv".format(DATA_DIRECTORY_PATH),
        sep="\t",
        index_col=0,
        squeeze=True,
    ).to_dict()

    best_cell_line_names = []

    cell_line_names_failed_to_map = set()

    for cell_line_name in cell_line_names:

        if cell_line_name in cell_line_name_best_cell_line_name:

            best_cell_line_names.append(
                cell_line_name_best_cell_line_name[cell_line_name]
            )

        else:

            best_cell_line_names.append(cell_line_name)

            cell_line_names_failed_to_map.add(cell_line_name)

    if 0 < len(cell_line_names_failed_to_map):

        print(
            "Cell line names failed to map: {}.".format(cell_line_names_failed_to_map)
        )

    return best_cell_line_names
