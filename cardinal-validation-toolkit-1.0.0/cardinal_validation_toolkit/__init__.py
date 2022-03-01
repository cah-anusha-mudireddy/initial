import csv
import io
import re
from os import listdir
from os.path import basename, isdir, isfile
from typing import Iterator, List, NamedTuple, Optional, TextIO

from fastjsonschema import JsonSchemaDefinitionException, JsonSchemaValueException

from .schemas import json_validator


# {practice}-{type}-{version}-{year}-{month}-{date}-{hour}:{minute}:{second}.txt
FILE_NAME_REGEX = re.compile(r"\w*-\w*-\w*-\d+-\d+-\d+-\d+:\d+:\d+\.txt")
BOOL_REGEX = re.compile(r"^\s*[ty1-9]", re.RegexFlag.IGNORECASE)


def remove_prefix(body: str, prefix: str) -> str:
    return body[len(prefix):] if body.startswith(prefix) else body


def infer_file_type_version(file_path: str) -> (str, str):
    return tuple(basename(file_path).split("-")[1:3])


class CardinalDialect(csv.Dialect):
    delimiter = "|"
    quotechar = '"'
    doublequote = True


class LineError(NamedTuple):
    line_number: int
    column_number: int
    column_name: str
    message: str


class FileResult(NamedTuple):
    file_path: str
    file_type: Optional[str]
    schema_version: Optional[str]
    file_error: Optional[str]
    line_errors: Iterator[LineError]


def validate_text(file_type: str, schema_version: str, text_io: TextIO) -> Iterator[LineError]:
    validate = json_validator(file_type, schema_version)
    reader = csv.DictReader(text_io, dialect=CardinalDialect())

    for line_number, obj in enumerate(reader, 1):
        try:
            validate(obj)
        except JsonSchemaValueException as e:
            column_number = reader.fieldnames.index(e.name)
            message = remove_prefix(e.message, "data.")
            yield LineError(line_number, column_number, e.name, message)


def validate_file(file_path: str) -> FileResult:
    try:
        with io.open(file_path, encoding="utf-8") as text_io:
            file_type, schema_version = infer_file_type_version(file_path)
            try:
                line_errors = validate_text(file_type, schema_version, text_io)
                yield FileResult(file_path, file_type, schema_version, None, line_errors)
            except JsonSchemaDefinitionException:
                yield FileResult(file_path, file_type, schema_version, "Schema invalid or not found", [])
    except FileNotFoundError:
        yield FileResult(file_path, None, None, "File not found", [])


def validate_dir(dir_path: str, recursive: bool = False) -> Iterator[FileResult]:
    for item_path in listdir(dir_path):
        if isfile(item_path) and FILE_NAME_REGEX.match(basename(item_path)):
            yield validate_file(item_path)
        elif isdir(item_path) and recursive:
            yield from validate_dir(item_path)


def validate_path(item_path: str, recursive: bool = False) -> Iterator[FileResult]:
    """
    Throws a FileNotFoundError if item_path does not exist or cannot be accessed.
    """
    if isfile(item_path):
        yield validate_file(item_path)
    elif isdir(item_path):
        yield from validate_dir(item_path, recursive)
    else:
        raise FileNotFoundError(f"path '{item_path}' cannot be accessed")


def collect(results: Iterator[FileResult]) -> List[FileResult]:
    """
    Since the validate methods normally yield lazy iterators, they don't start validating files until iterated.
    This collect function will run all of those iterators and collect the results into a concrete list.
    """
    return [
        FileResult(r.file_path, r.file_type, r.schema_version, r.file_error, list(r.line_errors))
        for r in results
    ]
