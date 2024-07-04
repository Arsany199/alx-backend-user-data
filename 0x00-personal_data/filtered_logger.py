#!/usr/bin/env python3
"""module use regex for handling Personal Data"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("email", "name", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """function return a log message obfuscated"""
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return (message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """funcrion returns filtered values from log record"""
        my_rec = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            my_rec, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """function that returns the logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    my_handler = logging.StreamHandler()
    my_handler.setFormatter(RedactingFormatter(List(PII_FIELDS)))
    logger.addHandler(my_handler)
    return (logger)
