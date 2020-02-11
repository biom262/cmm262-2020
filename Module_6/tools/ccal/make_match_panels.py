from os.path import isfile

from pandas import read_csv

from .establish_path import establish_path
from .make_file_name_from_str import make_file_name_from_str
from .make_match_panel import make_match_panel


def make_match_panels(
    target_x_sample,
    data_dicts,
    drop_negative_target=False,
    directory_path=None,
    plotly_directory_path=None,
    read_score_moe_p_value_fdr=False,
    **make_match_panel_kwargs,
):

    for target_name, target_values in target_x_sample.iterrows():

        if drop_negative_target:

            target_values = target_values[target_values != -1]

        for data_name, data_dict in data_dicts.items():

            suffix = "{}/{}".format(target_name, make_file_name_from_str(data_name))

            print("Making match panel for {} ...".format(suffix))

            score_moe_p_value_fdr = None

            if directory_path is None:

                file_path_prefix = None

            else:

                file_path_prefix = "{}/{}".format(directory_path, suffix)

                establish_path(file_path_prefix, "file")

                score_moe_p_value_fdr_file_path = "{}.tsv".format(file_path_prefix)

                if read_score_moe_p_value_fdr and isfile(
                    score_moe_p_value_fdr_file_path
                ):

                    print(
                        "Reading score_moe_p_value_fdr from {} ...".format(
                            score_moe_p_value_fdr_file_path
                        )
                    )

                    score_moe_p_value_fdr = read_csv(
                        score_moe_p_value_fdr_file_path, sep="\t", index_col=0
                    )

            if plotly_directory_path is None:

                plotly_html_file_path_prefix = None

            else:

                plotly_html_file_path_prefix = "{}/{}".format(
                    plotly_directory_path, suffix
                )

            make_match_panel(
                target_values,
                data_dict["df"],
                score_moe_p_value_fdr=score_moe_p_value_fdr,
                data_type=data_dict["type"],
                title=suffix.replace("/", "<br>"),
                file_path_prefix=file_path_prefix,
                plotly_html_file_path_prefix=plotly_html_file_path_prefix,
                **make_match_panel_kwargs,
            )
