#!/usr/bin/env python3
"""module use regex for handling Personal Data"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """function return a log message obfuscated"""
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return (message)
