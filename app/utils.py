import dataclasses
import datetime
import hashlib
import json
import math
import re
import secrets
import uuid
from bisect import bisect_left
from collections.abc import Collection
from enum import Enum
from pathlib import Path
from typing import Any, List, Type

from pydantic import BaseModel

from app.logs import logger

# * NOTE that this file should not have any non-standard dependencies

HERE = Path(__file__).parent


def is_json_serializable(value: Any) -> bool:
    """Returns True if the value is JSON serializable."""
    try:
        json.dumps(value)
        return True
    except:
        return False


def serialize_value(value: Any) -> Any:
    """Recursively converts non-native Python types to JSON serializable ones."""
    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]
    elif isinstance(value, dict):
        return {key: serialize_value(val) for key, val in value.items()}
    elif isinstance(value, BaseModel):
        return pydantic_model_to_dict(value)
    elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):  # type: ignore
        return value.isoformat()
    elif isinstance(value, Enum):
        return value.value
    elif isinstance(value, uuid.UUID):
        return str(value)
    elif not is_json_serializable(value):
        logger.warning(f'Value {value} is not JSON serializable, converting to string')
        return str(value)
    else:
        return value

def pydantic_model_to_dict(model: BaseModel, ignore: List[str] = []) -> dict:
    """Converts a Pydantic model to a dictionary, optionally ignoring specified keys."""
    data = model.dict()
    if ignore:
        data = {key: val for key, val in data.items() if key not in ignore}

    # Recursively serialize any nested models
    for key, val in data.items():
        if isinstance(val, BaseModel):
            data[key] = pydantic_model_to_dict(val, ignore)

    data = serialize_value(data)
    return data


def get_current_time_utc():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def get_current_time_utc_human_readable():
    return get_current_time_utc().strftime('%Y-%m-%d %H:%M:%S')


def generate_hex7_id():
    """ Generates a random hex string of hex length 7 (14 characters) """
    return secrets.token_hex(7)


def find_closest_ge(num_list: list[int | float], target: int | float) -> int | float | None:
    """ Returns the closest number greater than or equal to target in num_list """
    num_list.sort()
    index = bisect_left(num_list, target)
    if index != len(num_list):
        return num_list[index]
    else:
        return None


def words_in(s: str):
    """ counts space separated words in string

    Args:
        s (str): string to count words of

    Returns:
        int: number of words in s split my spaces
    """
    return len(s.split(' '))


# * Unquote from Chalice


_hexdig = '0123456789ABCDEFabcdef'
_hextobyte = None


def unquote_to_bytes(string):
    """unquote_to_bytes('abc%20def') -> b'abc def'."""
    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        # Is it a string-like object?
        string.split
        return b''
    if isinstance(string, str):
        string = string.encode('utf-8')
    bits = string.split(b'%')
    if len(bits) == 1:
        return string
    res = [bits[0]]
    append = res.append
    # Delay the initialization of the table to not waste memory
    # if the function is never called
    global _hextobyte
    if _hextobyte is None:
        _hextobyte = {(a + b).encode(): bytes.fromhex(a + b)
                      for a in _hexdig for b in _hexdig}
    for item in bits[1:]:
        try:
            append(_hextobyte[item[:2]])
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)
    return b''.join(res)


_asciire = re.compile('([\x00-\x7f]+)')


def unquote(string, encoding='utf-8', errors='replace'):
    """Replace %xx escapes by their single-character equivalent. The optional
    encoding and errors parameters specify how to decode percent-encoded
    sequences into Unicode characters, as accepted by the bytes.decode()
    method.
    By default, percent-encoded sequences are decoded with UTF-8, and invalid
    sequences are replaced by a placeholder character.

    unquote('abc%20def') -> 'abc def'.
    """
    if isinstance(string, bytes):
        return unquote_to_bytes(string).decode(encoding, errors)
    if '%' not in string:
        string.split
        return string
    if encoding is None:
        encoding = 'utf-8'
    if errors is None:
        errors = 'replace'
    bits = _asciire.split(string)
    res = [bits[0]]
    append = res.append
    for i in range(1, len(bits), 2):
        append(unquote_to_bytes(bits[i]).decode(encoding, errors))
        append(bits[i + 1])
    return ''.join(res)


def unquote_plus(string, encoding='utf-8', errors='replace'):
    """Like unquote(), but also replace plus signs by spaces, as required for
    unquoting HTML form values.

    unquote_plus('%7e/abc+def') -> '~/abc def'
    """
    string = string.replace('+', ' ')
    return unquote(string, encoding, errors)

# * -- Tokenizer Math --
# https://stackoverflow.com/questions/72294775/how-do-i-know-how-much-tokens-a-gpt-3-request-used


def tokens_in_string(string: str):
    """ Approximates the number of tokens in a string """
    return max(0, int((len(string))*math.exp(-1)))


def nchars_leq_ntokens_approx(maxTokens):
    """ Approximates the number of characters that will be <= maxTokens """
    sqrt_margin = 0.5
    lin_margin = 1.010175047  # = e - 1.001 - sqrt(1 - sqrt_margin) #ensures return 1 when maxTokens=1
    return max(0, int(maxTokens*math.exp(1) - lin_margin - math.sqrt(max(0, maxTokens - sqrt_margin))))


def truncate_string_to_tokens(string, maxTokens):
    """ Returns the string truncated to the number of tokens specified """
    # So the output string is very likely to have <= maxTokens, no guarantees though.
    char_index = min(len(string), nchars_leq_ntokens_approx(maxTokens))
    return string[:char_index]

#  -- Deterministic Hashing --


"""
https://death.andgravity.com/stable-hashing
Generate stable hashes for Python data objects.
Contains no business logic.
The hashes should be stable across interpreter implementations and versions.
Supports dataclass instances, datetimes, and JSON-serializable objects.
Empty dataclass fields are ignored, to allow adding new fields without
the hash changing. Empty means one of: None, '', (), [], or {}.
The dataclass type is ignored: two instances of different types
will have the same hash if they have the same attribute/value pairs.
https://github.com/lemon24/reader/blob/1efcd38c78f70dcc4e0d279e0fa2a0276749111e/src/reader/_hash_utils.py
"""

# The first byte of the hash contains its version,
# to allow upgrading the implementation without changing existing hashes.
# (In practice, it's likely we'll just let the hash change and update
# the affected objects again; nevertheless, it's good to have the option.)
#
# A previous version recommended using a check_hash(thing, hash) -> bool
# function instead of direct equality checking; it was removed because
# it did not allow objects to cache the hash.

_VERSION = 0
_EXCLUDE = '_hash_exclude_'


def get_hash(thing: object) -> bytes:
    prefix = _VERSION.to_bytes(1, 'big')
    digest = hashlib.md5(_json_dumps(thing).encode('utf-8')).digest()
    return prefix + digest[:-1]


def _json_dumps(thing: object) -> str:
    return json.dumps(
        thing,
        default=_json_default,
        # force formatting-related options to known values
        ensure_ascii=False,
        sort_keys=True,
        indent=None,
        separators=(',', ':'),
    )


def _json_default(thing: object) -> any:  # type: ignore
    try:
        return _dataclass_dict(thing)
    except TypeError:
        pass
    if isinstance(thing, datetime.datetime):
        return thing.isoformat(timespec='microseconds')
    raise TypeError(f"Object of type {type(thing).__name__} is not JSON serializable")


def _dataclass_dict(thing: object) -> dict[str, any]:  # type: ignore
    # we could have used dataclasses.asdict()
    # with a dict_factory that drops empty values,
    # but asdict() is recursive and we need to intercept and check
    # the _hash_exclude_ of nested dataclasses;
    # this way, json.dumps() does the recursion instead of asdict()

    # raises TypeError for non-dataclasses
    fields = dataclasses.fields(thing)  # type: ignore
    # ... but doesn't for dataclass *types*
    if isinstance(thing, type):
        raise TypeError("got type, expected instance")

    exclude = getattr(thing, _EXCLUDE, ())

    rv = {}
    for field in fields:
        if field.name in exclude:
            continue

        value = getattr(thing, field.name)
        if value is None or not value and isinstance(value, Collection):
            continue

        rv[field.name] = value

    return rv
