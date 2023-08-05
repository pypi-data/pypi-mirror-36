# -*- coding: utf-8 -*-
"""
Checks Polarion docstrings.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from collections import namedtuple

from pkg_resources import DistributionNotFound, get_distribution
from polarion_docstrings import configuration, parser

DocstringsError = namedtuple("DocstringsError", "lineno column message func")
FieldRecord = namedtuple("FieldRecord", "lineno column field")


def _validate(docstring_dict, key, valid_values):
    record = docstring_dict.get(key)
    if record is not None:
        return record.value in valid_values[key]
    return True


def _get_unknown_fields(docstring_dict, known_fields):
    unknown = [
        FieldRecord(docstring_dict[key].lineno, docstring_dict[key].column, key)
        for key in docstring_dict
        if key not in known_fields
    ]
    return unknown


def _get_invalid_fields(docstring_dict, valid_values):
    results = {key: _validate(docstring_dict, key, valid_values) for key in valid_values}
    invalid = [
        FieldRecord(docstring_dict[key].lineno, docstring_dict[key].column, key)
        for key, result in results.items()
        if not result
    ]
    return invalid


def _get_missing_fields(docstring_dict, required_keys):
    missing = [key for key in required_keys if key not in docstring_dict]
    return missing


def _get_markers_fields(docstring_dict, marker_fields):
    markers = [
        FieldRecord(docstring_dict[key].lineno, docstring_dict[key].column, key)
        for key in marker_fields
        if key in docstring_dict
    ]
    return markers


def validate_docstring(docstring_dict, config):
    """Returns tuple with lists of problematic fields."""
    cfg_docstrings = config["docstrings"]
    unknown = _get_unknown_fields(docstring_dict, cfg_docstrings["known_fields"])
    invalid = _get_invalid_fields(docstring_dict, cfg_docstrings["valid_values"])
    missing = _get_missing_fields(docstring_dict, cfg_docstrings["required_fields"])
    markers = _get_markers_fields(docstring_dict, cfg_docstrings["marker_fields"])
    return unknown, invalid, missing, markers


def get_fields_errors(validated_docstring, docstring_dict, marker_fields, lineno=0, column=0):
    """Produces fields errors for the flake8 checker."""
    errors = []
    func = polarion_checks492
    unknown, invalid, missing, markers = validated_docstring

    for num, col, field in unknown:
        errors.append(
            DocstringsError(lineno + num, col, 'P666 Unknown field "{}"'.format(field), func)
        )
    for num, col, field in invalid:
        errors.append(
            DocstringsError(
                lineno + num,
                col,
                'P667 Invalid value "{}" of the "{}" field'.format(
                    docstring_dict[field].value, field
                ),
                func,
            )
        )
    for num, col, field in markers:
        errors.append(
            DocstringsError(
                lineno + num,
                col,
                'P668 Field "{}" should be handled by the "{}" marker'.format(
                    field, marker_fields[field]
                ),
                func,
            )
        )
    for field in missing:
        errors.append(
            DocstringsError(lineno, column, 'P669 Missing required field "{}"'.format(field), func)
        )

    if errors:
        errors = sorted(errors, key=lambda tup: tup[0])
    return errors


def print_errors(errors):
    """Prints errors without using flake8."""
    for err in errors:
        print("line: {}:{}: {}".format(err.lineno, err.column, err.message), file=sys.stderr)


def check_docstrings(docstrings, config):
    """Runs checks on each docstring."""
    errors = []
    for record in docstrings:
        if record.value:
            valdoc = validate_docstring(record.value, config)
            errors.extend(
                get_fields_errors(
                    valdoc,
                    record.value,
                    config["docstrings"]["marker_fields"],
                    record.lineno,
                    record.column,
                )
            )
        else:
            errors.append(
                DocstringsError(
                    record.lineno,
                    record.column,
                    'P665 Missing "Polarion" section',
                    polarion_checks492,
                )
            )
    return errors


def run_checks(tree, filename, config):
    """Checks docstrings in python source file."""
    docstrings = parser.get_docstrings_in_file(tree, filename)
    errors = check_docstrings(docstrings, config)
    return errors


def polarion_checks492(tree, filename):
    """The flake8 entry point."""
    abs_filename = os.path.abspath(filename)
    __, tail = os.path.split(abs_filename)
    config = configuration.get_config()
    # check only test files under cfme/tests
    if config["tests_relative_path"] not in abs_filename or tail.find("test_") != 0:
        return []  # must be iterable
    return run_checks(tree, filename, config)


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "0.0"

polarion_checks492.name = "polarion_checks"
polarion_checks492.version = __version__
