import json
import os
import random
import string

from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.terminal import TerminalFormatter

from .common import *
from .exceptions import ClientException


def load_csv(path, delimiter=','):
    """Yield CSV rows.

    Usage:

    for row in load_csv('/path/to/file'):
        print(row)
    or
    list(load_csv('/path/to/file'))

    :param path: file path
    :param delimiter: CSV delimiter
    :return: row (from generator)
    """
    try:
        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                yield row
    except FileNotFoundError:
        raise ClientException("File not found: {}".format(path))


def load_json(path):
    """Load JSON file from path
    :param path: file path
    :return: dict
    """
    try:
        with open(path, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise ClientException("File not found: {}".format(path))


def chunk_number(num, thresh=10000):
    """
    Chunk a number into a list of numbers
    :param num: the number to chunk
    :param thresh: the maximum value of a chunk
    """
    while num:
        to_yield = min(num, thresh)
        yield to_yield
        num -= to_yield


def partition_payload(data, key, thresh):
    """
    Yield partitions of a payload.
    e.g. with a threshold of 2:

    { "dataElements": [1, 2, 3] }
    -->
    { "dataElements": [1, 2] }
       and
    { "dataElements": [3] }

    :param data: the payload
    :param key: the key of the dict to partition
    :param thresh: the maximum value of a chunk
    :yield: a partition of the payload
    """
    data = data[key]
    for i in range(0, len(data), thresh):
        yield {key: data[i:i + thresh]}


def search_auth_file(filename='dish.json'):
    """
    Search filename in
    - A) DHIS_HOME (env variable)
    - B) current user's home folder
    :param filename: the filename to search for
    :return: full path of filename
    """
    if 'DHIS_HOME' in os.environ:
        return os.path.join(os.environ['DHIS_HOME'], filename)
    else:
        home_path = os.path.expanduser(os.path.join('~'))
        for root, dirs, files in os.walk(home_path):
            if filename in files:
                return os.path.join(root, filename)
    raise ClientException("'{}' not found - searched in $DHIS_HOME and in home folder".format(filename))


def version_to_int(value):
    """
    Convert version info to integer
    :param value: the version received from system/info, e.g. "2.28"
    :return: integer from version, e.g. 28, None if it couldn't be parsed
    """
    # remove '-SNAPSHOT'
    value = value.replace('-SNAPSHOT', '')
    # remove '-RCx'
    if '-RC' in value:
        value = value.split('-RC', 1)[0]
    try:
        return int(value.split('.')[1])
    except (ValueError, IndexError):
        return


def create_uid():
    """
    Create DHIS2 UID matching to Regex
    ^[A-Za-z][A-Za-z0-9]{10}$
    :return: UID string
    """

    first = random.choice(string.ascii_letters)
    rest = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    return first + rest


def pretty_json(obj):
    """
    Print JSON with indentation and colours
    :param obj: the object to print - can be a dict or a string
    """
    if isinstance(obj, string_types):
        try:
            obj = json.loads(obj)
        except ValueError:
            raise ClientException("Not a json string")
    json_str = json.dumps(obj, sort_keys=True, indent=2)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))
