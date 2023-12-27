def field(name, value):
    vlen = len(str(value))
    return f"<{name}:{vlen}>{value}"

def field_with_newline(name, value):
    return field(name, value) + "\n"

def qso(data):
    result = ""
    for key in sorted(data.keys()):
        result += field(key, data.get(key)) + "\n"
    result += "<eor>\n\n"
    return result

