import re
_STATUS = re.compile(r'"\s+(\d{3})\s')
def extract_status(line):
    match = _STATUS.search(line)
    return match.group(1) if match else None
