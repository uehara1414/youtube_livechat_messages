from datetime import datetime

ISO8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def isostr_to_datetime(isostr: str) -> datetime:
    return datetime.strptime(isostr, ISO8601_FORMAT)
