'''SQL utilities
'''
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Union

from fishsense_data_processing_worker.metrics import get_summary


def load_query(path: Union[Path, str]) -> str:
    """Load query from file

    Args:
        path (Union[Path, str]): Path to query

    Returns:
        str: Prepared statement
    """
    path = Path(path)
    with open(path, 'r', encoding='utf-8') as handle:
        return handle.read()

def do_query(path: Union[Path, str], cur: sqlite3.Cursor, params: Dict[str, Any] = None) -> None:
    """Do single prepared statement

    Args:
        path (Union[Path, str]): Path to SQL statement
        cur (sqlite3.Cursor): Cursor
        params (Dict[str, Any]): Params. Defaults to None.
    """
    path = Path(path)
    query = load_query(path)
    with get_summary('query_timing').labels(query=path.stem).time():
        cur.execute(
            query,
            params
        )


def do_seq_query(path: Union[Path, str],
                 cur: sqlite3.Cursor,
                 param_seq: List[Dict[str, Any]]) -> None:
    """Do sequential prepared statement

    Args:
        path (Union[Path, str]): Path to SQL statement
        cur (sqlite3.Cursor): Cursor
        param_seq (List[Dict[str, Any]], optional): Sequence of parameters.
    """
    path = Path(path)
    query = load_query(path)
    with get_summary('query_timing').labels(query=f'{path.stem}_x{len(param_seq)}').time():
        cur.executemany(
            query,
            param_seq
        )


def do_script(path: Union[Path, str], cur: sqlite3.Cursor) -> None:
    """Do multiple prepared statements

    Args:
        path (Union[Path, str]): Path to SQL query
        cur (sqlite3.Cursor): Cursor
    """
    path = Path(path)
    query = load_query(path)
    with get_summary('query_timing').labels(query=path.stem).time():
        cur.executescript(query)
