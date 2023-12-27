"""
Helper functions for emitting ADIF records.
https://www.adif.org
"""

def field(name, value):
    """
    Returns the ADIF encoding of one field of data
    """
    vlen = len(str(value))
    return f"<{name}:{vlen}>{value}"

def field_with_newline(name, value):
    return field(name, value) + "\n"

def qso(data):
    """
    data: one QSO as a python dictionary, where keys represent adif fields
    """
    result = ""
    for key in sorted(data.keys()):
        result += field_with_newline(key, data.get(key))
    result += "<eor>\n\n"
    return result
