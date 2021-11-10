#! /usr/bin/env python3

import io
from enum import Enum
from typing import Callable, Sequence, Any, Optional, Type

from outputters import MyErrorHandler
from xmlproc.xmlproc import XMLProcessor


class Result(Enum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    UNRESOLVED = 'UNRESOLVED'


def ddmin(test: Callable[..., Result], inp: Sequence, *test_args: Any) -> Sequence:
    """Reduce the input inp, using the outcome of test(fun, inp)."""
    assert test(inp, *test_args) != Result.PASS

    n = 2  # Initial granularity
    while len(inp) >= 2:
        start = 0
        subset_length = int(len(inp) / n)
        some_complement_is_failing = False

        while start < len(inp):
            complement = (inp[:int(start)] + inp[int(start + subset_length):])

            if test(complement, *test_args) == Result.FAIL:
                inp = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(inp):
                break
            n = min(n * 2, len(inp))

    return inp


def test(inp: Sequence, fun: Callable[..., Result], expected_exc: Optional[Type] = None) -> Result:
    """Runs fun(imp) and determines whether the target failure still occurs."""

    detail = ""
    try:
        fun(inp)
        outcome = Result.PASS
    except Exception as e:
        detail = f" ({type(e).__name__}: {str(e)})"
        if expected_exc is None:
            outcome = Result.FAIL
        elif type(e) == type(expected_exc) and str(e) == str(expected_exc):
            outcome = Result.FAIL
        else:
            outcome = Result.UNRESOLVED

    print(f"{fun.__name__}({repr(inp)}): {outcome}{detail}\n\n")
    return outcome


class ParseException(Exception):
    def __init__(self, errors, warnings):
        self.errors = errors
        self.warnings = warnings

    def __str__(self):
        result = ""
        if self.errors:
            result += f"{len(self.errors)} errors:\n"
            result += "\n".join(self.errors)
        if self.warnings:
            result += f"{len(self.warnings)} warnings:\n"
            result += "\n".join(self.warnings)
        return result


def parse(xml: str):
    processor = XMLProcessor()

    handler = MyErrorHandler(processor)
    processor.set_error_handler(handler)

    with io.StringIO(xml) as file:
        processor.parse_resource(file)

    if handler.errors or handler.warnings:
        raise ParseException(handler.errors, handler.warnings)


with open("xmlproc/demo/urls.xml") as f:
    contents = f.read()
    reduced = ddmin(test, contents, parse)
    print(f"Reduced: {reduced}")
