"""Logic for alerting the user on possibly problematic patterns in the data (e.g. high number of zeros , constant
values, high correlations)."""
from enum import Enum, unique
from typing import List, Union
import warnings
from contextlib import suppress
import re
from dateutil.parser import parse

import numpy as np

from pandas_profiling.correlations import perform_check_correlation
from pandas_profiling.config import config
from pandas_profiling.base import Variable


@unique
class MessageType(Enum):
    """Message Types"""

    CONST = 1
    """This variable has a constant value."""

    ZEROS = 2
    """This variable contains zeros."""

    HIGH_CORRELATION = 3
    """This variable is highly correlated."""

    RECODED = 4
    """This variable is correlated (categorical)."""

    HIGH_CARDINALITY = 5
    """This variable has a high cardinality."""

    UNSUPPORTED = 6
    """This variable is unsupported."""

    DUPLICATES = 7
    """This variable contains duplicates."""

    SKEWED = 8
    """This variable is highly skewed."""

    MISSING = 9
    """This variable contains missing values."""

    INFINITE = 10
    """This variable contains infinite values."""

    TYPE_DATE = 11
    """This variable is likely a datetime, but treated as categorical."""

    UNIQUE = 12


class Message(object):
    """A message object (type, values, column)."""

    def __init__(
        self,
        message_type: MessageType,
        values: dict,
        column_name: Union[str, None] = None,
        fields=None,
    ):
        if fields is None:
            fields = set()

        self.fields = fields
        self.message_type = message_type
        self.values = values
        self.column_name = column_name
        self.anchor_id = hash(column_name)


def check_table_messages(table: dict) -> List[Message]:
    """Checks the overall dataset for warnings.

    Args:
        table: Overall dataset statistics.

    Returns:
        A list of messages.
    """
    messages = []
    if warning_value(table["n_duplicates"]):
        messages.append(
            Message(
                message_type=MessageType.DUPLICATES,
                values=table,
                fields={"n_duplicates"},
            )
        )
    return messages


def check_variable_messages(col: str, description: dict) -> List[Message]:
    """Checks individual variables for warnings.

    Args:
        col: The column name that is checked.
        description: The series description.

    Returns:
        A list of messages.
    """
    messages = []

    # Missing
    if warning_value(description["p_missing"]):
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.MISSING,
                values=description,
                fields={"p_missing", "n_missing"},
            )
        )

    if description["type"] == Variable.S_TYPE_UNSUPPORTED:
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.UNSUPPORTED,
                values=description,
                fields={},
            )
        )
        return messages

    if description["distinct_count_with_nan"] <= 1:
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.CONST,
                values=description,
                fields={"n_unique"},
            )
        )

    if description["distinct_count_without_nan"] == description["n"]:
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.UNIQUE,
                values=description,
                fields={"n_unique", "p_unique"},
            )
        )

    # Infinite values
    if warning_value(description["p_infinite"]):
        messages.append(
            Message(
                column_name=col,
                message_type=MessageType.INFINITE,
                values=description,
                fields={"p_infinite", "n_infinite"},
            )
        )

    # Categorical
    if description["type"] in {Variable.TYPE_CAT}:
        if description["date_warning"]:
            messages.append(
                Message(column_name=col, message_type=MessageType.TYPE_DATE, values={})
            )

        # High cardinality
        if description["distinct_count"] > config["vars"]["cat"][
            "cardinality_threshold"
        ].get(int):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.HIGH_CARDINALITY,
                    values=description,
                    fields={"n_unique"},
                )
            )

    # Numerical
    if description["type"] in {Variable.TYPE_NUM}:
        # Skewness
        if warning_skewness(description["skewness"]):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.SKEWED,
                    values=description,
                    fields={"skewness"},
                )
            )
        # Zeros
        if warning_value(description["p_zeros"]):
            messages.append(
                Message(
                    column_name=col,
                    message_type=MessageType.ZEROS,
                    values=description,
                    fields={"n_zeros", "p_zeros"},
                )
            )

    return messages


def check_correlation_messages(correlations):
    messages = []

    for corr, matrix in correlations.items():
        if config["correlations"][corr]["warn_high_correlations"].get(bool):
            threshold = config["correlations"][corr]["threshold"].get(float)
            correlated_mapping = perform_check_correlation(matrix, threshold)
            if len(correlated_mapping) > 0:
                for k, v in correlated_mapping.items():
                    messages.append(
                        Message(
                            column_name=k,
                            message_type=MessageType.HIGH_CORRELATION,
                            values={"corr": corr, "fields": v},
                        )
                    )
    return messages


def warning_value(value: float) -> bool:
    return not np.isnan(value) and value > 0.01


def warning_skewness(v: float) -> bool:
    return not np.isnan(v) and (
        v < -config["vars"]["num"]["skewness_threshold"].get(int)
        or v > config["vars"]["num"]["skewness_threshold"].get(int)
    )


def _date_parser(date_string):
    pattern = re.compile(r"[.\-:]")
    pieces = re.split(pattern, date_string)

    if len(pieces) < 3:
        raise ValueError("Must have at least year, month and date passed")

    return parse(date_string)


def warning_type_date(series):
    with suppress(ValueError):
        with suppress(TypeError):
            series.apply(_date_parser)
            return True

    return False
