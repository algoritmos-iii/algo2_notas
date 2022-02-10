import itertools
from typing import Iterable
from gspread.utils import rowcol_to_a1


def _get_groups_indexes(column) -> tuple:
    """
    Indexes returned are 0-indexed.
    Assumes that first and last elements are not empty.
    """

    first_indexes = [0]
    last_indexes = []

    for index, elem in enumerate(column):
        if index > 0 and elem and not column[index - 1]:
            first_indexes.append(index)

        if index < len(column) - 1 and elem and not column[index + 1]:
            last_indexes.append(index)

    last_indexes.append(len(column) - 1)

    return tuple(zip(first_indexes, last_indexes))


def process_feedbacks(dataset: Iterable):
    """
    Processes feedback sheets "Devoluciones" and "Devoluciones Examenes".
    Synthetic fields:
    * "identifier": the group or padron of the feedback
    * "activity_name": the name of the exercise or exam
    * "email_sent_cell": the cell where the "EMAIL_SENT" field is located in
    A1 notation
    """

    [headers_col, *data_cols] = dataset
    [_, *data_groups] = _get_groups_indexes(headers_col)

    output = []

    for column, column_data in enumerate(data_cols):
        identifier = column_data[0]

        for group_idx in data_groups:
            output.append(
                {
                    "identifier": identifier,
                    "activity_name": headers_col[group_idx[0]],
                    "email_sent_cell": rowcol_to_a1(
                        col=column + 2,
                        row=group_idx[1] + 1,
                    ),
                    **dict(
                        itertools.zip_longest(
                            headers_col[group_idx[0] + 1 : group_idx[1] + 1],
                            [
                                field.strip()
                                for field in column_data[
                                    group_idx[0] + 1 : group_idx[1] + 1
                                ]
                            ],
                            fillvalue="",
                        ),
                    ),
                }
            )

    return output


def process_papers(dataset: Iterable):
    [headers_col, *data_cols] = dataset
    [_, *data_groups] = _get_groups_indexes(headers_col)

    output = []

    for col in data_cols:
        identifier = col[0]

        for group_idx in data_groups:
            output.append(
                {
                    "identifier": identifier,
                    **dict(
                        itertools.zip_longest(
                            headers_col[group_idx[0] : group_idx[1] + 1],
                            [
                                field.strip()
                                for field in col[group_idx[0] : group_idx[1] + 1]
                            ],
                            fillvalue="",
                        ),
                    ),
                }
            )

    return output


def process_students(dataset: Iterable):
    headers, *data = list(itertools.zip_longest(*dataset, fillvalue=None))
    return [dict(zip(headers, student)) for student in data]


def process_groups(dataset: Iterable):
    headers, *data = list(itertools.zip_longest(*dataset, fillvalue=None))
    return [dict(zip(headers, group)) for group in data]
