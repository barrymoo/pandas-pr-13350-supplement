#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re

from pandas.util.terminal import get_terminal_size
from pandas.compat import (range, zip, lrange, StringIO, PY3,
                           u, lzip, is_platform_windows,
                           is_platform_32bit)
import pandas.formats.printing as printing

def has_expanded_repr(df):
    r = repr(df)
    for line in r.split('\n'):
        if line.endswith('\\'):
            return True
    return False

def has_doubly_truncated_repr(df):
    return has_horizontally_truncated_repr(
        df) and has_vertically_truncated_repr(df)

def has_truncated_repr(df):
    return has_horizontally_truncated_repr(
        df) or has_vertically_truncated_repr(df)

def has_vertically_truncated_repr(df):
    r = repr(df)
    only_dot_row = False
    for row in r.splitlines():
        if re.match('^[\.\ ]+$', row):
            only_dot_row = True
    return only_dot_row

def has_horizontally_truncated_repr(df):
    try:  # Check header row
        fst_line = np.array(repr(df).splitlines()[0].split())
        cand_col = np.where(fst_line == '...')[0][0]
    except:
        return False
    # Make sure each row has this ... in the same place
    r = repr(df)
    for ix, l in enumerate(r.splitlines()):
        if not r.split()[cand_col] == '...':
            return False
    return True

# Test  1 test_datetimelike_frame
df = pd.DataFrame({'date' : [pd.Timestamp('20130101').tz_localize('UTC')] + [pd.NaT]*5})
with pd.option_context("display.max_rows", 5):
    result = str(df)
    assert('2013-01-01 00:00:00+00:00' in result)
    assert('NaT' in result)
    assert('...' in result)
    assert('[6 rows x 1 columns]' in result)

dts = [pd.Timestamp('2011-01-01', tz='US/Eastern')] * 5 + [pd.NaT] * 5
df = pd.DataFrame({"dt": dts,
                    "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

with pd.option_context('display.max_rows', 5):
    expected = ('                          dt   x\n'
                '0  2011-01-01 00:00:00-05:00   1\n'
                '1  2011-01-01 00:00:00-05:00   2\n'
                '..                       ...  ..\n'
                '8                        NaT   9\n'
                '9                        NaT  10\n\n'
                '[10 rows x 2 columns]')
    #assert(repr(df) == expected)

# NOTES: No need to go further, test fails because column 4 is int (extra leading space)
# CORRECTIONS: remove 1 whitespace column between 'dt' and 'x'

# Test  2 test_east_asian_unicode_frame
if PY3:
    _rep = repr
else:
    _rep = unicode

# mid col
df = pd.DataFrame({'a': [u'あ', u'いいい', u'う', u'ええええええ'],
                'b': [1, 222, 33333, 4]},
                index=['a', 'bb', 'c', 'ddd'])
expected = (u"          a      b\na         あ      1\n"
            u"bb      いいい    222\nc         う  33333\n"
            u"ddd  ええええええ      4")
#assert(_rep(df) == expected)

# NOTES: No need to go further, test fails because int and unicode string columns have (extra leading space)
# CORRECTIONS: remove 1 whitespace column before unicode strings and integers

# Test  3 test_index_with_nan
df = pd.DataFrame({'id1': {0: '1a3',
                        1: '9h4'},
                'id2': {0: np.nan,
                        1: 'd67'},
                'id3': {0: '78d',
                        1: '79d'},
                'value': {0: 123,
                            1: 64}})

# multi-index
y = df.set_index(['id1', 'id2', 'id3'])
result = y.to_string()
expected = u(
    '             value\nid1 id2 id3       \n1a3 NaN 78d    123\n9h4 d67 79d     64')
#assert(result == expected)

df = pd.DataFrame({'id1': {0: np.nan,
                        1: '9h4'},
                'id2': {0: np.nan,
                        1: 'd67'},
                'id3': {0: np.nan,
                        1: '79d'},
                'value': {0: 123,
                            1: 64}})

y = df.set_index(['id1', 'id2', 'id3'])
result = y.to_string()
expected = u(
    '             value\nid1 id2 id3       \nNaN NaN NaN    123\n9h4 d67 79d     64')
#assert(result == expected)

# NOTES: No need to go further, checked first and last test in this set
# CORRECTIONS: remove 1 whitespace column before last column

# Test  4 test_period
df = pd.DataFrame({'A': pd.period_range('2013-01',
                                        periods=4, freq='M'),
                    'B': [pd.Period('2011-01', freq='M'),
                            pd.Period('2011-02-01', freq='D'),
                            pd.Period('2011-03-01 09:00', freq='H'),
                            pd.Period('2011-04', freq='M')],
                    'C': list('abcd')})
exp = ("        A                B  C\n0 2013-01          2011-01  a\n"
        "1 2013-02       2011-02-01  b\n2 2013-03 2011-03-01 09:00  c\n"
        "3 2013-04          2011-04  d")
#assert(str(df) == exp)

# CORRECTIONS: remove 1 whitespace column before last column

# Test  5 test_repr_max_columns_max_rows
term_width, term_height = get_terminal_size()
if term_width < 10 or term_height < 10:
    raise nose.SkipTest("terminal size too small, "
                        "{0} x {1}".format(term_width, term_height))

def mkframe(n):
    index = ['%05d' % i for i in range(n)]
    return pd.DataFrame(0, index, index)

df6 = mkframe(6)
df10 = mkframe(10)
with pd.option_context('mode.sim_interactive', True):
    with pd.option_context('display.width', term_width * 2):
        with pd.option_context('display.max_rows', 5,
                            'display.max_columns', 5):
            assert(not has_expanded_repr(mkframe(4)))
            assert(not has_expanded_repr(mkframe(5)))
            assert(not has_expanded_repr(df6))
            assert(has_doubly_truncated_repr(df6))

        with pd.option_context('display.max_rows', 20,
                            'display.max_columns', 10):
            # Out off max_columns boundary, but no extending
            # since not exceeding width
            assert(not has_expanded_repr(df6))
            assert(not has_truncated_repr(df6))

        with pd.option_context('display.max_rows', 9,
                            'display.max_columns', 10):
            # out vertical bounds can not result in exanded repr
            assert(not has_expanded_repr(df10))
            assert(has_vertically_truncated_repr(df10))

    # width=None in terminal, auto detection
    with pd.option_context('display.max_columns', 100, 'display.max_rows',
                        term_width * 20, 'display.width', None):
        df = mkframe((term_width // 7) - 2)
        print(term_width // 7)
        print(repr(df))
        assert(not has_expanded_repr(df))
        df = mkframe((term_width // 7) + 2)
        print(repr(df))
        printing.pprint_thing(df._repr_fits_horizontal_())
        #assert(has_expanded_repr(df))
        print(repr(df))

# NOTES: Failure on 187, but unsure why. I think it was expecting the df to
#  be too large to fit, but missing whitespace fixes that problem
# CORRECTIONS: Unsure

# Test  6 test_repr_truncation
# Test  7 test_str_max_colwidth
# Test  8 test_to_latex
# Test  9 test_to_latex_decimal
# Test 10 test_to_latex_escape_special_chars
# Test 11 test_to_latex_format
# Test 12 test_to_latex_longtable
# Test 13 test_to_latex_multiindex
# Test 14 test_to_latex_no_header
# Test 15 test_to_string_float_index
# Test 16 test_to_string_format_na
# Test 17 test_to_string_index_formatter
# Test 18 test_to_string_left_justify_cols
# Test 19 test_to_string_line_width
# Test 20 test_to_string_no_header
# Test 21 test_to_string_no_index
# Test 22 test_to_string_with_formatters
# Test 23 test_east_asian_unicode_series
# Test 24 test_format_explicit
# Test 25 test_period
# Test 26 test_to_string_dtype
# Test 27 test_to_string_header
# Test 29 test_to_string_length
# Test 30 test_to_string_mixed
# Test 31 test_to_string_name
# Test 32 test_truncate_ndots
