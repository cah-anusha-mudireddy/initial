import importlib_resources as resources
import json
from functools import lru_cache
from typing import Callable

from fastjsonschema import compile


@lru_cache()
def json_validator(file_type: str, schema_version: str) -> Callable[[any], any]:
    schema_dir = resources.files("cardinal_validation_toolkit.schemas")
    file = schema_dir / schema_version / f"{file_type}.schema.json"
    return compile(json.loads(file.read_text()))
