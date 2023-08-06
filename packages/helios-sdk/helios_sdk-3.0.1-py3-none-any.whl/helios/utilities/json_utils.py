"""Helper functions for JSON objects."""
import json


def read_json_file(json_file, **kwargs):
    """
    Read a json file.

    Args:
        json_file (str): Full path to JSON file.
        **kwargs: Any keyword argument from the json.load method.
    Returns:
        dict: JSON formatted dictionary.

    """
    with open(json_file, 'r') as f:
        return json.load(f, **kwargs)


def read_json_string(json_string, **kwargs):
    """
    Convert JSON formatted string to JSON.

    Args:
        json_string (str): JSON formatted string.
        **kwargs: Any keyword argument from the json.loads method.
    Returns:
        dict: JSON formatted dictionary.

    """
    return json.loads(json_string, **kwargs)


def write_json(json_dict, file_name, **kwargs):
    """
    Write JSON dictionary to file.

    Args:
        json_dict (dict): JSON formatted dictionary.
        file_name (str): Output file name.
        **kwargs: Any keyword argument from the json.dump method.
    Returns:
        None

    """
    with open(file_name, 'w+') as output_file:
        json.dump(json_dict, output_file, **kwargs)


def merge_json(data, keys):
    """
    Merge JSON fields into a single list.

    Keys can either be a single string or a list of strings signifying a chain
    of "keys" into the dictionary.

    Args:
        data (list): Dictionary to merge data from.
        keys (str or sequence of strs): A chain of keys into the dictionary
            to get to the field that will be merged.
    Returns:
        list: Merged values.

    """
    if not isinstance(keys, list):
        keys = [keys]
    for k in keys:
        data = _merge_digger(data, k)
    return data


def _merge_digger(data, key):
    merged_list = []
    if not isinstance(data, list):
        data = [data]
    for json_slice in data:
        temp = json_slice[key]
        if not isinstance(temp, list):
            temp = [temp]
        merged_list.extend(temp)
    return merged_list
