# Cardinal Validation Toolkit

[Repo](https://bitbucket.org/jvionatlanta/cardinal-validation-toolkit) - [Pipeline](https://dev.azure.com/jvion-technology/cardinal-validation-toolkit/_build?definitionId=52)

`cardinal-validation-toolkit` is a Python library for validating CSV data from Cardinal.

## Usage

### As a Library

```python
from typing import Iterator
from cardinal_validation_toolkit import FileResult, validate_path

results: Iterator[FileResult] = validate_path("/path/to/the/file.csv")
```

where `results` is an `Iterator[FileResult]`. Each `FileResult` has information about the validation of that file, including:

- `file_error: Optional[str]` - a description of the problem accessing or loading a schema for the file, or `None` if there was no such problem
- `line_errors: Iterator[LineError]` - a sequence of errors for individual invalid lines in this file
- `file_path: str` - full path to the file (or directory if a directory is given as path and there is an error accessing it)
- `file_type: Optional[str]` - type of file if that could be determined
- `schema_version: Optional[str]` - version of schema for file if that could be determined

Each `LineError` has information about a particular line that had a validation failure, with the properties:

- `line_number: int` - the first non-header line is line 1
- `column_number: int` - the first value on a line is column 1
- `column_name: str` - the name of the field that is in column `column_number`
- `message: str` - description of the validation failure 

Since the `validate_*` functions return lazy `Iterator`s, no validation is done until those `Iterator`s are looped over. The `collect` function can be used to force a `Iterator[FileResult]` into a `List[FileResult]` that has been fully executed (nested `Iterator[LineError]`s are also collected).

### As a Command-line Program

```shell
python -m cardinal_validation_toolkit --target-path /path/to/the/file.csv
# or
python -m cardinal_validation_toolkit --target-path /path/to/folder-containing-files --recursive
```

`--target-path` is required. It can be either a file or a directory.

For each file that gets processed, a log line is written to the console (`ERROR` log if there is a `file_error`) followed by any `LineError`s that come up in the processing of the file.

A summary of how many files were processed and how many failed is shown at the end.

`main` calls `exit(1)` if there are any validation errors.
