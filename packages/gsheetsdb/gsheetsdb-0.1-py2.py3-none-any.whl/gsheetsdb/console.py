"""Google Spreadsheets CLI

Usage:
  gsheetsdb [--headers=<headers>]
  gsheetsdb (-h | --help)
  gsheetsdb --version

Options:
  -h --help             Show this screen.
  --version             Show version.
  --headers=<headers>   Specifies how many rows are header rows [default: 0]

"""

from __future__ import unicode_literals

import os

from docopt import docopt
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.lexers import SqlLexer
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle
from pygments.styles import get_style_by_name
from six.moves.urllib import parse
from tabulate import tabulate

from gsheetsdb import connect, __version__


keywords = [
    'and',
    'asc',
    'by',
    'date',
    'datetime',
    'desc',
    'false',
    'format',
    'group',
    'label',
    'limit',
    'not',
    'offset',
    'options',
    'or',
    'order',
    'pivot',
    'select',
    'timeofday',
    'timestamp',
    'true',
    'where',
]

aggregate_functions = [
    'avg',
    'count',
    'max',
    'min',
    'sum',
]

scalar_functions = [
    'year',
    'month',
    'day',
    'hour',
    'minute',
    'second',
    'millisecond',
    'quarter',
    'dayOfWeek',
    'now',
    'dateDiff',
    'toDate',
    'upper',
    'lower',
]


def get_connection_kwargs(url):
    parts = parse.urlparse(url)
    if ':' in parts.netloc:
        host, port = parts.netloc.split(':', 1)
        port = int(port)
    else:
        host = parts.netloc
        port = 8082

    return {
        'host': host,
        'port': port,
        'path': parts.path,
        'scheme': parts.scheme,
    }


def get_autocomplete(connection):
    return keywords + aggregate_functions + scalar_functions


def main():
    history = FileHistory(os.path.expanduser('~/.gsheetsdb_history'))

    arguments = docopt(__doc__, version=__version__.__version__)
    connection = connect()
    headers = int(arguments['--headers'])
    cursor = connection.cursor()

    lexer = PygmentsLexer(SqlLexer)
    words = get_autocomplete(connection)
    completer = WordCompleter(words, ignore_case=True)
    style = style_from_pygments_cls(get_style_by_name('monokai'))

    while True:
        try:
            query = prompt(
                '> ', lexer=lexer, completer=completer,
                style=style, history=history)
        except EOFError:
            break  # Control-D pressed.

        # run query
        query = query.strip('; ')
        if query:
            try:
                result = cursor.execute(query, headers=headers)
            except Exception as e:
                print(e)
                continue

            columns = [t[0] for t in cursor.description or []]
            print(tabulate(result, headers=columns))

    print('GoodBye!')


if __name__ == '__main__':
    main()
