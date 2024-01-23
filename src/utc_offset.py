import re

class ValidationError(Exception):
    pass


def parse(utc_offset):
    """
    Parses the input string and returns UTC offset (hours, minutes) as an
    integer pair (tuple).
    """
    utc_offset_hours = 0
    utc_offset_minutes = 0
    utc_offset_multiplier = 1
    matched = False

    # When INPUT_UTC_OFFSET is undefined, assume UTC
    if not utc_offset:
        logging.debug(f"INPUT_UTC_OFFSET is null; Skipping TZ conversion")
        return (0, 0)

    # Handle leading minus sign
    if utc_offset[0] == '-':
        utc_offset = utc_offset[1:]
        utc_offset_multiplier = -1

    # Match H or HH
    result = re.match(r'(\d{1,2})$', utc_offset)
    if result:
        matched = True
        utc_offset_hours = int(result.group(1))
        utc_offset_minutes = 0

    # Match HHMM
    result = re.match(r'(\d{4})$', utc_offset)
    if result:
        matched = True
        utc_offset_hours = int(result.group(1)[0:2])
        utc_offset_minutes = int(result.group(1)[2:4])

    # Match [-]HH:MM
    result = re.match(r'(\d{2}):(\d{2})$', utc_offset)
    if result:
        matched = True
        utc_offset_hours = int(result.group(1))
        utc_offset_minutes = int(result.group(2))

    # Validation
    if not matched:
        raise ValidationError(f"failed to parse [{utc_offset}]")

    if not (utc_offset_hours >=0 and utc_offset_hours <=12):
        raise ValidationError(f"hours out of range")

    if not (utc_offset_minutes >=0 and utc_offset_minutes <=59):
        raise ValidationError(f"minutes out of range")

    if not (utc_offset_multiplier in (1, -1)):
        raise ValidationError(f"multiplier out of range")

    utc_offset_hours *= utc_offset_multiplier
    utc_offset_minutes *= utc_offset_multiplier

    return (utc_offset_hours, utc_offset_minutes)


def to_string(utc_offset):
    (utc_offset_hours, utc_offset_minutes) = parse(utc_offset)
    offset_direction = "+"

    if utc_offset_hours < 0:
        offset_direction = "-"

    if utc_offset_hours < 0:
        utc_offset_hours *= -1

    if utc_offset_minutes < 0:
        utc_offset_minutes *= -1

    return f"{offset_direction}{utc_offset_hours:02d}:{utc_offset_minutes:02d}"
