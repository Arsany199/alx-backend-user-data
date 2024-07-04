#!/usr/bin/env python3
"""model uses regex to repalce a certain value"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """function returns the log message obfuscated"""
    for f in fields:
        message = re.sub(f'{f}=(.*?){separator}',
                         f'{f}={redaction}{separator}', message)
    return (message)
