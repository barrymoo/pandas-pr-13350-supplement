#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Necessary imports
import pandas as pd
import numpy as np
import re
from pandas.util.terminal import get_terminal_size
from pandas.compat import (range, zip, lrange, StringIO, PY3,
                           u, lzip, is_platform_windows,
                           is_platform_32bit)
import pandas.formats.printing as printing
import pandas.formats.format as fmt
import pandas.util.testing as tm


# A few functions necessary for failing tests
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

def gen_test_series():
    s1 = pd.Series(['a'] * 100)
    s2 = pd.Series(['ab'] * 100)
    s3 = pd.Series(['a', 'ab', 'abc', 'abcd', 'abcde', 'abcdef'])
    s4 = s3[::-1]
    test_sers = {'onel': s1, 'twol': s2, 'asc': s3, 'desc': s4}
    return test_sers


# Test  1 test_datetimelike_frame
print("--> Begin: Test 1 test_datetimelike_frame <--")
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
    print(repr(df))

dts = [pd.NaT] * 5 + [pd.Timestamp('2011-01-01', tz='US/Eastern')] * 5
df = pd.DataFrame({"dt": dts,
                    "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
with pd.option_context('display.max_rows', 5):
    expected = ('                          dt   x\n'
                '0                        NaT   1\n'
                '1                        NaT   2\n'
                '..                       ...  ..\n'
                '8  2011-01-01 00:00:00-05:00   9\n'
                '9  2011-01-01 00:00:00-05:00  10\n\n'
                '[10 rows x 2 columns]')
    #assert(repr(df) == expected)
    print(repr(df))

dts = ([pd.Timestamp('2011-01-01', tz='Asia/Tokyo')] * 5 +
        [pd.Timestamp('2011-01-01', tz='US/Eastern')] * 5)
df = pd.DataFrame({"dt": dts,
                    "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
with pd.option_context('display.max_rows', 5):
    expected = ('                           dt   x\n'
                '0   2011-01-01 00:00:00+09:00   1\n'
                '1   2011-01-01 00:00:00+09:00   2\n'
                '..                        ...  ..\n'
                '8   2011-01-01 00:00:00-05:00   9\n'
                '9   2011-01-01 00:00:00-05:00  10\n\n'
                '[10 rows x 2 columns]')
    #assert(repr(df) == expected)
    print(repr(df))

# CORRECTIONS: remove whitespace columns before unicode strings and integers
print("-->  End: Test 1 test_datetimelike_frame  <--")

# Test  2 test_east_asian_unicode_frame
print("-->  Begin: Test 2 test_east_asian_unicode_frame  <--")
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
print(_rep(df))

# last col
df = pd.DataFrame({'a': [1, 222, 33333, 4],
                'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                index=['a', 'bb', 'c', 'ddd'])
expected = (u"         a       b\na        1       あ\n"
            u"bb     222     いいい\nc    33333       う\n"
            u"ddd      4  ええええええ")
#assert(_rep(df) == expected)
print(_rep(df))

# all col
df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                index=['a', 'bb', 'c', 'ddd'])
expected = (u"         a       b\na    あああああ       あ\n"
            u"bb       い     いいい\nc        う       う\n"
            u"ddd    えええ  ええええええ")
#assert(_rep(df) == expected)
print(_rep(df))

# column name
df = pd.DataFrame({u'あああああ': [1, 222, 33333, 4],
                'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                index=['a', 'bb', 'c', 'ddd'])
expected = (u"          b  あああああ\na         あ      1\n"
            u"bb      いいい    222\nc         う  33333\n"
            u"ddd  ええええええ      4")
#assert(_rep(df) == expected)
print(_rep(df))

# index
df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                index=[u'あああ', u'いいいいいい', u'うう', u'え'])
expected = (u"            a       b\nあああ     あああああ       あ\n"
            u"いいいいいい      い     いいい\nうう          う       う\n"
            u"え         えええ  ええええええ")
#assert(_rep(df) == expected)
print(_rep(df))

# index name
df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                index=pd.Index([u'あ', u'い', u'うう', u'え'], name=u'おおおお'))
expected = (u"          a       b\nおおおお               \nあ     あああああ       あ\n"
            u"い         い     いいい\nうう        う       う\nえ       えええ  ええええええ"
            )
#assert(_rep(df) == expected)
print(_rep(df))

# all
df = pd.DataFrame({u'あああ': [u'あああ', u'い', u'う', u'えええええ'],
                u'いいいいい': [u'あ', u'いいい', u'う', u'ええ']},
                index=pd.Index([u'あ', u'いいい', u'うう', u'え'], name=u'お'))
expected = (u"       あああ いいいいい\nお               \nあ      あああ     あ\n"
            u"いいい      い   いいい\nうう       う     う\nえ    えええええ    ええ")
#assert(_rep(df) == expected)
print(_rep(df))

# MultiIndex
idx = pd.MultiIndex.from_tuples([(u'あ', u'いい'), (u'う', u'え'), (
    u'おおお', u'かかかか'), (u'き', u'くく')])
df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                'b': [u'あ', u'いいい', u'う', u'ええええええ']}, index=idx)
expected = (u"              a       b\nあ   いい    あああああ       あ\n"
            u"う   え         い     いいい\nおおお かかかか      う       う\n"
            u"き   くく      えええ  ええええええ")
#assert(_rep(df) == expected)
print(_rep(df))

# truncate
with pd.option_context('display.max_rows', 3, 'display.max_columns', 3):
    df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                        'b': [u'あ', u'いいい', u'う', u'ええええええ'],
                        'c': [u'お', u'か', u'ききき', u'くくくくくく'],
                        u'ああああ': [u'さ', u'し', u'す', u'せ']},
                        columns=['a', 'b', 'c', u'ああああ'])

    expected = (u"        a ...  ああああ\n0   あああああ ...     さ\n"
                u"..    ... ...   ...\n3     えええ ...     せ\n"
                u"\n[4 rows x 4 columns]")
    #assert(_rep(df) == expected)
    print(_rep(df))

    df.index = [u'あああ', u'いいいい', u'う', 'aaa']
    expected = (u"         a ...  ああああ\nあああ  あああああ ...     さ\n"
                u"..     ... ...   ...\naaa    えええ ...     せ\n"
                u"\n[4 rows x 4 columns]")
    #assert(_rep(df) == expected)
    print(_rep(df))

# Emable Unicode option -----------------------------------------
with pd.option_context('display.unicode.east_asian_width', True):

    # mid col
    df = pd.DataFrame({'a': [u'あ', u'いいい', u'う', u'ええええええ'],
                    'b': [1, 222, 33333, 4]},
                    index=['a', 'bb', 'c', 'ddd'])
    expected = (u"                a      b\na              あ      1\n"
                u"bb         いいい    222\nc              う  33333\n"
                u"ddd  ええええええ      4")
    #assert(_rep(df) == expected)
    print(_rep(df))

    # last col
    df = pd.DataFrame({'a': [1, 222, 33333, 4],
                    'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                    index=['a', 'bb', 'c', 'ddd'])
    expected = (u"         a             b\na        1            あ\n"
                u"bb     222        いいい\nc    33333            う\n"
                u"ddd      4  ええええええ")
    #assert(_rep(df) == expected)
    print(_rep(df))

    # all col
    df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                    'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                    index=['a', 'bb', 'c', 'ddd'])
    expected = (u"              a             b\na    あああああ            あ\n"
                u"bb           い        いいい\nc            う            う\n"
                u"ddd      えええ  ええええええ"
                "")
    #assert(_rep(df) == expected)
    print(_rep(df))

    # column name
    df = pd.DataFrame({u'あああああ': [1, 222, 33333, 4],
                    'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                    index=['a', 'bb', 'c', 'ddd'])
    expected = (u"                b  あああああ\na              あ           1\n"
                u"bb         いいい         222\nc              う       33333\n"
                u"ddd  ええええええ           4")
    #assert(_rep(df) == expected)
    print(_rep(df))

    # index
    df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                    'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                    index=[u'あああ', u'いいいいいい', u'うう', u'え'])
    expected = (u"                       a             b\nあああ        あああああ            あ\n"
                u"いいいいいい          い        いいい\nうう                  う            う\n"
                u"え                えええ  ええええええ")
    #assert(_rep(df) == expected)
    print(_rep(df))

    # index name
    df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                    'b': [u'あ', u'いいい', u'う', u'ええええええ']},
                    index=pd.Index([u'あ', u'い', u'うう', u'え'], name=u'おおおお'))
    expected = (u"                   a             b\nおおおお                          \n"
                u"あ        あああああ            あ\nい                い        いいい\n"
                u"うう              う            う\nえ            えええ  ええええええ"
                )
    #assert(_rep(df) == expected)
    print(_rep(df))

    # all
    df = pd.DataFrame({u'あああ': [u'あああ', u'い', u'う', u'えええええ'],
                    u'いいいいい': [u'あ', u'いいい', u'う', u'ええ']},
                    index=pd.Index([u'あ', u'いいい', u'うう', u'え'], name=u'お'))
    expected = (u"            あああ いいいいい\nお                           \n"
                u"あ          あああ         あ\nいいい          い     いいい\n"
                u"うう            う         う\nえ      えええええ       ええ")
    #assert(_rep(df) == expected)
    print(_rep(df))

    # MultiIndex
    idx = pd.MultiIndex.from_tuples([(u'あ', u'いい'), (u'う', u'え'), (
        u'おおお', u'かかかか'), (u'き', u'くく')])
    df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                    'b': [u'あ', u'いいい', u'う', u'ええええええ']}, index=idx)
    expected = (u"                          a             b\nあ     いい      あああああ            あ\n"
                u"う     え                い        いいい\nおおお かかかか          う            う\n"
                u"き     くく          えええ  ええええええ")
    #assert(_rep(df) == expected)
    print(_rep(df))

    # truncate
    with pd.option_context('display.max_rows', 3, 'display.max_columns',
                        3):

        df = pd.DataFrame({'a': [u'あああああ', u'い', u'う', u'えええ'],
                            'b': [u'あ', u'いいい', u'う', u'ええええええ'],
                            'c': [u'お', u'か', u'ききき', u'くくくくくく'],
                            u'ああああ': [u'さ', u'し', u'す', u'せ']},
                            columns=['a', 'b', 'c', u'ああああ'])

        expected = (u"             a   ...    ああああ\n0   あああああ   ...          さ\n"
                    u"..         ...   ...         ...\n3       えええ   ...          せ\n"
                    u"\n[4 rows x 4 columns]")
        #assert(_rep(df) == expected)
        print(_rep(df))

        df.index = [u'あああ', u'いいいい', u'う', 'aaa']
        expected = (u"                 a   ...    ああああ\nあああ  あああああ   ...          さ\n"
                    u"...            ...   ...         ...\naaa         えええ   ...          せ\n"
                    u"\n[4 rows x 4 columns]")
        #assert(_rep(df) == expected)
        print(_rep(df))

    # ambiguous unicode
    df = pd.DataFrame({u'あああああ': [1, 222, 33333, 4],
                    'b': [u'あ', u'いいい', u'¡¡', u'ええええええ']},
                    index=['a', 'bb', 'c', '¡¡¡'])
    expected = (u"                b  あああああ\na              あ           1\n"
                u"bb         いいい         222\nc              ¡¡       33333\n"
                u"¡¡¡  ええええええ           4")
    #assert(_rep(df) == expected)
    print(_rep(df))

# CORRECTIONS: remove whitespace columns before unicode strings and integers
print("-->  End: Test 2 test_east_asian_unicode_frame   <--")

# Test  3 test_index_with_nan
print("--> Begin: Test 3 test_index_with_nan <--")
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
print(result)

# index
y = df.set_index('id2')
result = y.to_string()
expected = u(
    '     id1  id3  value\nid2                 \nNaN  1a3  78d    123\nd67  9h4  79d     64')
#assert(result == expected)
print(result)

# with append (this failed in 0.12)
y = df.set_index(['id1', 'id2']).set_index('id3', append=True)
result = y.to_string()
expected = u(
    '             value\nid1 id2 id3       \n1a3 NaN 78d    123\n9h4 d67 79d     64')
#assert(result == expected)
print(result)

# all-nan in mi
df2 = df.copy()
df2.ix[:, 'id2'] = np.nan
y = df2.set_index('id2')
result = y.to_string()
expected = u(
    '     id1  id3  value\nid2                 \nNaN  1a3  78d    123\nNaN  9h4  79d     64')
#assert(result == expected)
print(result)

# partial nan in mi
df2 = df.copy()
df2.ix[:, 'id2'] = np.nan
y = df2.set_index(['id2', 'id3'])
result = y.to_string()
expected = u(
    '         id1  value\nid2 id3            \nNaN 78d  1a3    123\n    79d  9h4     64')
#assert(result == expected)
print(result)

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
print(result)

# CORRECTIONS: remove whitespace columns before last column
print("-->  End: Test 3 test_index_with_nan  <--")


# Test  4 test_period
print("--> Begin: Test 4 test_period <--")
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
print("-->  End: Test 4 test_period  <--")

# Test  5 test_repr_max_columns_max_rows
print("--> Begin: Test 5 test_repr_max_columns_max_rows <--")
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
        #assert(not has_expanded_repr(df))
        df = mkframe((term_width // 7) + 2)
        print(repr(df))
        printing.pprint_thing(df._repr_fits_horizontal_())
        #assert(has_expanded_repr(df))
        print(repr(df))

print("Failure on line 481, but unsure why. I think it is expecting the df to " +
      "be too large to fit, but missing whitespace fixes that problem")
# CORRECTIONS: Unsure
print("-->  End: Test 5 test_repr_max_columns_max_rows <--")

# Test  6 test_repr_truncation
print("--> Begin: Test 6 test_repr_truncation <--")
max_len = 20
with pd.option_context("display.max_colwidth", max_len):
    df = pd.DataFrame({'A': np.random.randn(10),
                       'B': [tm.rands(np.random.randint(
                                max_len - 1, max_len + 1)) for i in range(10)
                            ]})
    r = repr(df)
    r = r[r.find('\n') + 1:]

    adj = fmt._get_adjustment()

    for line, value in lzip(r.split('\n'), df['B']):
        if adj.len(value) + 1 > max_len:
            assert('...' not in line)
        else:
            assert('...' not in line)

with pd.option_context("display.max_colwidth", 999999):
    assert('...' not in repr(df))

with pd.option_context("display.max_colwidth", max_len + 2):
    assert('...' not in repr(df))
    
# CORRECTIONS: None, test passes on my machine (both py2 and py3)
print("-->  End: Test 6 test_repr_truncation  <--")

# Test  7 test_str_max_colwidth
print("--> Begin: Test 7 test_str_max_colwidth <--")
df = pd.DataFrame([{'a': 'foo',
                    'b': 'bar',
                    'c': 'uncomfortably long line with lots of stuff',
                    'd': 1}, {'a': 'foo',
                                'b': 'bar',
                                'c': 'stuff',
                                'd': 1}])
df.set_index(['a', 'b', 'c'])
#assert(
#    str(df) ==
#    '     a    b                                           c  d\n'
#    '0  foo  bar  uncomfortably long line with lots of stuff  1\n'
#    '1  foo  bar                                       stuff  1')
print(str(df))
with pd.option_context('max_colwidth', 20):
#    assert(str(df) == '     a    b                    c  d\n'
#                    '0  foo  bar  uncomfortably lo...  1\n'
#                    '1  foo  bar                stuff  1')
    print(str(df))
# CORRECTIONS: Fixing whitespace
print("-->  End: Test 7 test_str_max_colwidth  <--")

# Test  8 test_to_latex
print("--> Begin: Test 8 test_to_latex <--")
df = pd.DataFrame({'a': [1, 2], 'b': ['b1', 'b2']})
withindex_result = df.to_latex()
withindex_expected = r"""\begin{tabular}{lrl}
\toprule
{} &  a &   b \\
\midrule
0 &  1 &  b1 \\
1 &  2 &  b2 \\
\bottomrule
\end{tabular}
"""
#assert(withindex_result == withindex_expected)
print(withindex_result)

withoutindex_result = df.to_latex(index=False)
withoutindex_expected = r"""\begin{tabular}{rl}
\toprule
 a &   b \\
\midrule
 1 &  b1 \\
 2 &  b2 \\
\bottomrule
\end{tabular}
"""
#assert(withoutindex_result == withoutindex_expected)
print(withoutindex_result)

# CORRECTIONS: Fix whitespace
print("-->  End: Test 8 test_to_latex  <--")

# Test  9 test_to_latex_decimal
print("--> Begin: Test 9 test_to_latex_decimal <--")
df = pd.DataFrame({'a': [1.0, 2.1], 'b': ['b1', 'b2']})
withindex_result = df.to_latex(decimal=',')
withindex_expected = r"""\begin{tabular}{lrl}
\toprule
{} &    a &   b \\
\midrule
0 &  1,0 &  b1 \\
1 &  2,1 &  b2 \\
\bottomrule
\end{tabular}
"""
#assert(withindex_result == withindex_expected)
print(withindex_result)
# CORRECTIONS: Fix whitespace
print("-->  End: Test 9 test_to_latex_decimal  <--")

# Test 10 test_to_latex_escape_special_chars
print("--> Begin: Test 10 test_to_latex_escape_special_chars <--")
a = 'a'
b = 'b'

test_dict = {u('co^l1'): {a: "a",
                          b: "b"},
             u('co$e^x$'): {a: "a",
                            b: "b"}}

unescaped_result = pd.DataFrame(test_dict).to_latex(escape=False)
escaped_result = pd.DataFrame(test_dict).to_latex(
)  # default: escape=True

unescaped_expected = r'''\begin{tabular}{lll}
\toprule
{} & co$e^x$ & co^l1 \\
\midrule
a &       a &     a \\
b &       b &     b \\
\bottomrule
\end{tabular}
'''

escaped_expected = r'''\begin{tabular}{lll}
\toprule
{} & co\$e\textasciicircumx\$ & co\textasciicircuml1 \\
\midrule
a &       a &     a \\
b &       b &     b \\
\bottomrule
\end{tabular}
'''

assert(unescaped_result == unescaped_expected)
assert(escaped_result == escaped_expected)
# CORRECTIONS:
print("-->  End: Test 10 test_to_latex_escape_special_chars  <--")

# Test 11 test_to_latex_format
print("--> Begin: Test 11 test_to_latex_format <--")
df = pd.DataFrame({'a': [1, 2], 'b': ['b1', 'b2']})
withindex_result = df.to_latex(column_format='ccc')
withindex_expected = r"""\begin{tabular}{ccc}
\toprule
{} &  a &   b \\
\midrule
0 &  1 &  b1 \\
1 &  2 &  b2 \\
\bottomrule
\end{tabular}
"""
#assert(withindex_result == withindex_expected)
print(withoutindex_result)
# CORRECTIONS: Whitespace correction
print("-->  End: Test 11 test_to_latex_format  <--")

# Test 12 test_to_latex_longtable
print("--> Begin: Test 12 test_to_latex_longtable <--")
df = pd.DataFrame({'a': [1, 2], 'b': ['b1', 'b2']})
withindex_result = df.to_latex(longtable=True)
withindex_expected = r"""\begin{longtable}{lrl}
\toprule
{} &  a &   b \\
\midrule
\endhead
\midrule
\multicolumn{3}{r}{{Continued on next page}} \\
\midrule
\endfoot

\bottomrule
\endlastfoot
0 &  1 &  b1 \\
1 &  2 &  b2 \\
\end{longtable}
"""

#assert(withindex_result == withindex_expected)
print(withindex_result)

withoutindex_result = df.to_latex(index=False, longtable=True)
withoutindex_expected = r"""\begin{longtable}{rl}
\toprule
 a &   b \\
\midrule
\endhead
\midrule
\multicolumn{3}{r}{{Continued on next page}} \\
\midrule
\endfoot

\bottomrule
\endlastfoot
 1 &  b1 \\
 2 &  b2 \\
\end{longtable}
"""
#assert(withoutindex_result == withoutindex_expected)
print(withoutindex_result)
# CORRECTIONS: fixing whitespace
print("-->  End: Test 12 test_to_latex_longtable  <--")

# Test 13 test_to_latex_multiindex
print("--> Begin: Test 13 test_to_latex_multiindex <--")
df = pd.DataFrame({('x', 'y'): ['a']})
result = df.to_latex()
expected = r"""\begin{tabular}{ll}
\toprule
{} &  x \\
{} &  y \\
\midrule
0 &  a \\
\bottomrule
\end{tabular}
"""

#assert(result == expected)
print(result)

result = df.T.to_latex()
expected = r"""\begin{tabular}{lll}
\toprule
  &   &  0 \\
\midrule
x & y &  a \\
\bottomrule
\end{tabular}
"""

#assert(result == expected)
print(result)

df = pd.DataFrame.from_dict({
    ('c1', 0): pd.Series(dict((x, x) for x in range(4))),
    ('c1', 1): pd.Series(dict((x, x + 4) for x in range(4))),
    ('c2', 0): pd.Series(dict((x, x) for x in range(4))),
    ('c2', 1): pd.Series(dict((x, x + 4) for x in range(4))),
    ('c3', 0): pd.Series(dict((x, x) for x in range(4))),
}).T
result = df.to_latex()
expected = r"""\begin{tabular}{llrrrr}
\toprule
   &   &  0 &  1 &  2 &  3 \\
\midrule
c1 & 0 &  0 &  1 &  2 &  3 \\
   & 1 &  4 &  5 &  6 &  7 \\
c2 & 0 &  0 &  1 &  2 &  3 \\
   & 1 &  4 &  5 &  6 &  7 \\
c3 & 0 &  0 &  1 &  2 &  3 \\
\bottomrule
\end{tabular}
"""

#assert(result == expected)
print(result)

# GH 10660
df = pd.DataFrame({'a': [0, 0, 1, 1],
                    'b': list('abab'),
                    'c': [1, 2, 3, 4]})
result = df.set_index(['a', 'b']).to_latex()
expected = r"""\begin{tabular}{llr}
\toprule
  &   &  c \\
a & b &    \\
\midrule
0 & a &  1 \\
  & b &  2 \\
1 & a &  3 \\
  & b &  4 \\
\bottomrule
\end{tabular}
"""

#assert(result == expected)
print(result)

result = df.groupby('a').describe().to_latex()
expected = r"""\begin{tabular}{llr}
\toprule
  &       &         c \\
a & {} &           \\
\midrule
0 & count &  2.000000 \\
  & mean &  1.500000 \\
  & std &  0.707107 \\
  & min &  1.000000 \\
  & 25\% &  1.250000 \\
  & 50\% &  1.500000 \\
  & 75\% &  1.750000 \\
  & max &  2.000000 \\
1 & count &  2.000000 \\
  & mean &  3.500000 \\
  & std &  0.707107 \\
  & min &  3.000000 \\
  & 25\% &  3.250000 \\
  & 50\% &  3.500000 \\
  & 75\% &  3.750000 \\
  & max &  4.000000 \\
\bottomrule
\end{tabular}
"""

assert(result == expected)
# CORRECTIONS: fix whitespace
print("-->  End: Test 13 test_to_latex_multiindex  <--")

# Test 14 test_to_latex_no_header
print("--> Begin: Test 14 test_to_latex_no_header <--")
df = pd.DataFrame({'a': [1, 2], 'b': ['b1', 'b2']})
withindex_result = df.to_latex(header=False)
withindex_expected = r"""\begin{tabular}{lrl}
\toprule
0 &  1 &  b1 \\
1 &  2 &  b2 \\
\bottomrule
\end{tabular}
"""

#assert(withindex_result == withindex_expected)
print(withindex_result)

withoutindex_result = df.to_latex(index=False, header=False)
withoutindex_expected = r"""\begin{tabular}{rl}
\toprule
 1 &  b1 \\
 2 &  b2 \\
\bottomrule
\end{tabular}
"""

#assert(withoutindex_result == withoutindex_expected)
print(withoutindex_result)
# CORRECTIONS: fix whitespace
print("-->  End: Test 14 test_to_latex_no_header  <--")

# Test 15 test_to_string_float_index
print("--> Begin: Test 15 test_to_string_float_index <--")
index = pd.Index([1.5, 2, 3, 4, 5])
df = pd.DataFrame(lrange(5), index=index)

result = df.to_string()
expected = ('     0\n'
            '1.5  0\n'
            '2.0  1\n'
            '3.0  2\n'
            '4.0  3\n'
            '5.0  4')
#assert(result == expected)
print(result)
# CORRECTIONS: fix whitespace
print("-->  End: Test 15 test_to_string_float_index  <--")

# Test 16 test_to_string_format_na
print("--> Begin: Test 16 test_to_string_format_na <--")
df =pd.DataFrame({'A': [np.nan, -1, -2.1234, 3, 4],
                'B': [np.nan, 'foo', 'foooo', 'fooooo', 'bar']})
result = df.to_string()

expected = ('        A       B\n'
            '0     NaN     NaN\n'
            '1 -1.0000     foo\n'
            '2 -2.1234   foooo\n'
            '3  3.0000  fooooo\n'
            '4  4.0000     bar')
#assert(result == expected)
print(result)

df =pd.DataFrame({'A': [np.nan, -1., -2., 3., 4.],
                'B': [np.nan, 'foo', 'foooo', 'fooooo', 'bar']})
result = df.to_string()

expected = ('     A       B\n'
            '0  NaN     NaN\n'
            '1 -1.0     foo\n'
            '2 -2.0   foooo\n'
            '3  3.0  fooooo\n'
            '4  4.0     bar')
#assert(result == expected)
print(result)
# CORRECTIONS: whitespace
print("-->  End: Test 16 test_to_string_format_na  <--")

# Test 17 test_to_string_index_formatter
print("--> Begin: Test 17 test_to_string_index_formatter <--")
df = pd.DataFrame([lrange(5), lrange(5, 10), lrange(10, 15)])

rs = df.to_string(formatters={'__index__': lambda x: 'abc' [x]})

xp = """\
    0   1   2   3   4
a   0   1   2   3   4
b   5   6   7   8   9
c  10  11  12  13  14\
"""

#assert(rs == xp)
print(rs)
# CORRECTIONS:
print("-->  End: Test 17 test_to_string_index_formatter  <--")

# Test 18 test_to_string_left_justify_cols
print("--> Begin: Test 18 test_to_string_left_justify_cols <--")
df = pd.DataFrame({'x': [3234, 0.253]})
df_s = df.to_string(justify='left')
expected = ('   x       \n' '0  3234.000\n' '1     0.253')
#assert(df_s == expected)
print(df_s)
# CORRECTIONS: whitespace
print("-->  End: Test 18 test_to_string_left_justify_cols  <--")

# Test 19 test_to_string_line_width
print("--> Begin: Test 19 test_to_string_line_width <--")
df = pd.DataFrame(123, lrange(10, 15), lrange(30))
s = df.to_string(line_width=80)
#assert(max(len(l) for l in s.split('\n')) == 80)
print('Line 910 max line width: {0}'.format(max(len(l) for l in s.split('\n'))))
# CORRECTIONS:
print("-->  End: Test 19 test_to_string_line_width  <--")

# Test 20 test_to_string_no_header
print("--> Begin: Test 20 test_to_string_no_header <--")
df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

df_s = df.to_string(header=False)
expected = "0  1  4\n1  2  5\n2  3  6"

#assert(df_s == expected)
print(df_s)
# CORRECTIONS:
print("-->  End: Test 20 test_to_string_no_header  <--")

# Test 21 test_to_string_no_index
print("--> Begin: Test 21 test_to_string_no_index <--")
df =pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

df_s = df.to_string(index=False)
expected = "x  y\n1  4\n2  5\n3  6"

#assert(df_s == expected)
print(df_s)
# CORRECTIONS:
print("-->  End: Test 21 test_to_string_no_index  <--")

# Test 22 test_to_string_with_formatters
print("--> Begin: Test 22 test_to_string_with_formatters <--")
df =pd.DataFrame({'int': [1, 2, 3],
                'float': [1.0, 2.0, 3.0],
                'object': [(1, 2), True, False]},
                columns=['int', 'float', 'object'])

formatters = [('int', lambda x: '0x%x' % x),
                ('float', lambda x: '[% 4.1f]' % x),
                ('object', lambda x: '-%s-' % str(x))]
result = df.to_string(formatters=dict(formatters))
result2 = df.to_string(formatters=lzip(*formatters)[1])
#assert(result == ('  int  float    object\n'
#                            '0 0x1 [ 1.0]  -(1, 2)-\n'
#                            '1 0x2 [ 2.0]    -True-\n'
#                            '2 0x3 [ 3.0]   -False-'))
print(result)
assert(result == result2)
# CORRECTIONS:
print("-->  End: Test 22 test_to_string_with_formatters  <--")

# Test 23 test_east_asian_unicode_series
print("--> Begin: Test 23 test_east_asian_unicode_series <--")
if PY3:
    _rep = repr
else:
    _rep = unicode
# not alighned properly because of east asian width

# unicode index
s = pd.Series(['a', 'bb', 'CCC', 'D'],
            index=[u'あ', u'いい', u'ううう', u'ええええ'])
expected = (u"あ         a\nいい       bb\nううう     CCC\n"
            u"ええええ      D\ndtype: object")
#assert(_rep(s) == expected)
print(_rep(s))

# unicode values
s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'],
            index=['a', 'bb', 'c', 'ddd'])
expected = (u"a         あ\nbb       いい\nc       ううう\n"
            u"ddd    ええええ\ndtype: object")
#assert(_rep(s) == expected)
print(_rep(s))

# both
s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'],
            index=[u'ああ', u'いいいい', u'う', u'えええ'])
expected = (u"ああ         あ\nいいいい      いい\nう        ううう\n"
            u"えええ     ええええ\ndtype: object")
#assert(_rep(s) == expected)
print(_rep(s))

# unicode footer
s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'],
            index=[u'ああ', u'いいいい', u'う', u'えええ'], name=u'おおおおおおお')
expected = (u"ああ         あ\nいいいい      いい\nう        ううう\n"
            u"えええ     ええええ\nName: おおおおおおお, dtype: object")
#assert(_rep(s) == expected)
print(_rep(s))

# MultiIndex
idx = pd.MultiIndex.from_tuples([(u'あ', u'いい'), (u'う', u'え'), (
    u'おおお', u'かかかか'), (u'き', u'くく')])
s = pd.Series([1, 22, 3333, 44444], index=idx)
expected = (u"あ    いい          1\nう    え          22\nおおお  かかかか     3333\n"
            u"き    くく      44444\ndtype: int64")
#assert(_rep(s) == expected)
print(_rep(s))

# object dtype, shorter than unicode repr
s = pd.Series([1, 22, 3333, 44444], index=[1, 'AB', np.nan, u'あああ'])
expected = (u"1          1\nAB        22\nNaN     3333\n"
            u"あああ    44444\ndtype: int64")
#assert(_rep(s) == expected)
print(_rep(s))

# object dtype, longer than unicode repr
s = pd.Series([1, 22, 3333, 44444],
            index=[1, 'AB', pd.Timestamp('2011-01-01'), u'あああ'])
expected = (u"1                          1\nAB                        22\n"
            u"2011-01-01 00:00:00     3333\nあああ                    44444\ndtype: int64"
            )
#assert(_rep(s) == expected)
print(_rep(s))

# truncate
with pd.option_context('display.max_rows', 3):
    s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'], name=u'おおおおおおお')

    expected = (u"0       あ\n     ... \n"
                u"3    ええええ\nName: おおおおおおお, dtype: object")
    #assert(_rep(s) == expected)
    print(_rep(s))

    s.index = [u'ああ', u'いいいい', u'う', u'えええ']
    expected = (u"ああ        あ\n       ... \n"
                u"えええ    ええええ\nName: おおおおおおお, dtype: object")
    #assert(_rep(s) == expected)
    print(_rep(s))

# Emable Unicode option -----------------------------------------
with pd.option_context('display.unicode.east_asian_width', True):

    # unicode index
    s = pd.Series(['a', 'bb', 'CCC', 'D'],
                index=[u'あ', u'いい', u'ううう', u'ええええ'])
    expected = (u"あ            a\nいい         bb\nううう      CCC\n"
                u"ええええ      D\ndtype: object")
    #assert(_rep(s) == expected)
    print(_rep(s))

    # unicode values
    s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'],
                index=['a', 'bb', 'c', 'ddd'])
    expected = (u"a            あ\nbb         いい\nc        ううう\n"
                u"ddd    ええええ\ndtype: object")
    #assert(_rep(s) == expected)
    print(_rep(s))

    # both
    s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'],
                index=[u'ああ', u'いいいい', u'う', u'えええ'])
    expected = (u"ああ              あ\nいいいい        いい\nう            ううう\n"
                u"えええ      ええええ\ndtype: object")
    #assert(_rep(s) == expected)
    print(_rep(s))

    # unicode footer
    s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'],
                index=[u'ああ', u'いいいい', u'う', u'えええ'], name=u'おおおおおおお')
    expected = (u"ああ              あ\nいいいい        いい\nう            ううう\n"
                u"えええ      ええええ\nName: おおおおおおお, dtype: object")
    #assert(_rep(s) == expected)
    print(_rep(s))

    # MultiIndex
    idx = pd.MultiIndex.from_tuples([(u'あ', u'いい'), (u'う', u'え'), (
        u'おおお', u'かかかか'), (u'き', u'くく')])
    s = pd.Series([1, 22, 3333, 44444], index=idx)
    expected = (u"あ      いい            1\nう      え             22\nおおお  かかかか     3333\n"
                u"き      くく        44444\ndtype: int64")
    #assert(_rep(s) == expected)
    print(_rep(s))

    # object dtype, shorter than unicode repr
    s = pd.Series([1, 22, 3333, 44444], index=[1, 'AB', np.nan, u'あああ'])
    expected = (u"1             1\nAB           22\nNaN        3333\n"
                u"あああ    44444\ndtype: int64")
    #assert(_rep(s) == expected)
    print(_rep(s))

    # object dtype, longer than unicode repr
    s = pd.Series([1, 22, 3333, 44444],
                index=[1, 'AB', pd.Timestamp('2011-01-01'), u'あああ'])
    expected = (u"1                          1\nAB                        22\n"
                u"2011-01-01 00:00:00     3333\nあああ                 44444\ndtype: int64"
                )
    #assert(_rep(s) == expected)
    print(_rep(s))

    # truncate
    with pd.option_context('display.max_rows', 3):
        s = pd.Series([u'あ', u'いい', u'ううう', u'ええええ'], name=u'おおおおおおお')
        expected = (u"0          あ\n       ...   \n"
                    u"3    ええええ\nName: おおおおおおお, dtype: object")
        #assert(_rep(s) == expected)
        print(_rep(s))

        s.index = [u'ああ', u'いいいい', u'う', u'えええ']
        expected = (u"ああ            あ\n            ...   \n"
                    u"えええ    ええええ\nName: おおおおおおお, dtype: object")
        #assert(_rep(s) == expected)
        print(_rep(s))

    # ambiguous unicode
    s = pd.Series([u'¡¡', u'い¡¡', u'ううう', u'ええええ'],
                index=[u'ああ', u'¡¡¡¡いい', u'¡¡', u'えええ'])
    expected = (u"ああ              ¡¡\n¡¡¡¡いい        い¡¡\n¡¡            ううう\n"
                u"えええ      ええええ\ndtype: object")
    #assert(_rep(s) == expected)
    print(_rep(s))
# CORRECTIONS:
print("-->  End: Test 23 test_east_asian_unicode_series  <--")

# Test 24 test_format_explicit
print("--> Begin: Test 24 test_format_explicit <--")
with pd.option_context("display.max_rows", 4):
    test_sers = gen_test_series()
    res = repr(test_sers['onel'])
    exp = '0     a\n1     a\n     ..\n98    a\n99    a\ndtype: object'
    #assert(exp == res)
    print(res)
    res = repr(test_sers['twol'])
    exp = ('0     ab\n1     ab\n      ..\n98    ab\n99    ab\ndtype:'
            ' object')
    #assert(exp == res)
    print(res)
    res = repr(test_sers['asc'])
    exp = ('0         a\n1        ab\n      ...  \n4     abcde\n5'
            '    abcdef\ndtype: object')
    #assert(exp == res)
    print(res)
    res = repr(test_sers['desc'])
    exp = ('5    abcdef\n4     abcde\n      ...  \n1        ab\n0'
            '         a\ndtype: object')
    #assert(exp == res)
    print(res)
# CORRECTIONS:
print("-->  End: Test 24 test_format_explicit  <--")

# Test 25 test_period
print("--> Begin: Test 25 test_period <--")
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
print(str(df))
# CORRECTIONS:
print("-->  End: Test 25 test_period  <--")

# Test 26 test_to_string_dtype
print("--> Begin: Test 26 test_to_string_dtype <--")
s = pd.Series(range(100), dtype='int64')
res = s.to_string(max_rows=2, dtype=True)
exp = '0      0\n      ..\n99    99\ndtype: int64'
#assert(res == exp)
print(res)
res = s.to_string(max_rows=2, dtype=False)
exp = '0      0\n      ..\n99    99'
#assert(res == exp)
print(res)
# CORRECTIONS:
print("-->  End: Test 26 test_to_string_dtype  <--")

# Test 27 test_to_string_header
print("--> Begin: Test 27 test_to_string_header <--")
s = pd.Series(range(10), dtype='int64')
s.index.name = 'foo'
res = s.to_string(header=True, max_rows=2)
exp = 'foo\n0    0\n    ..\n9    9'
#assert(res == exp)
print(res)
res = s.to_string(header=False, max_rows=2)
exp = '0    0\n    ..\n9    9'
#assert(res == exp)
print(res)
# CORRECTIONS:
print("-->  End: Test 27 test_to_string_header  <--")

# Test 29 test_to_string_length
print("--> Begin: Test 29 test_to_string_length <--")
s = pd.Series(range(100), dtype='int64')
res = s.to_string(max_rows=2, length=True)
exp = '0      0\n      ..\n99    99\nLength: 100'
#assert(res == exp)
print(res)
# CORRECTIONS:
print("-->  End: Test 29 test_to_string_length  <--")

# Test 30 test_to_string_mixed
print("--> Begin: Test 30 test_to_string_mixed <--")
s = pd.Series(['foo', np.nan, -1.23, 4.56])
result = s.to_string()
expected = (u('0     foo\n') + u('1     NaN\n') + u('2   -1.23\n') +
            u('3    4.56'))
assert(result == expected)

# but don't count NAs as floats
s = pd.Series(['foo', np.nan, 'bar', 'baz'])
result = s.to_string()
expected = (u('0    foo\n') + '1    NaN\n' + '2    bar\n' + '3    baz')
#assert(result == expected)
print(result)

s = pd.Series(['foo', 5, 'bar', 'baz'])
result = s.to_string()
expected = (u('0    foo\n') + '1      5\n' + '2    bar\n' + '3    baz')
#assert(result == expected)
print(result)
# CORRECTIONS:
print("-->  End: Test 30 test_to_string_mixed  <--")

# Test 31 test_to_string_name
print("--> Begin: Test 31 test_to_string_name <--")
s = pd.Series(range(100), dtype='int64')
s.name = 'myser'
res = s.to_string(max_rows=2, name=True)
exp = '0      0\n      ..\n99    99\nName: myser'
#assert(res == exp)
print(res)
res = s.to_string(max_rows=2, name=False)
exp = '0      0\n      ..\n99    99'
#assert(res == exp)
print(res)
# CORRECTIONS:
print("-->  End: Test 31 test_to_string_name  <--")

# Test 32 test_truncate_ndots
print("--> Begin: Test 32 test_truncate_ndots <--")
def getndots(s):
    return len(re.match('[^\.]*(\.*)', s).groups()[0])

s = pd.Series([0, 2, 3, 6])
with pd.option_context("display.max_rows", 2):
    strrepr = repr(s).replace('\n', '')
assert(getndots(strrepr) == 2)

s = pd.Series([0, 100, 200, 400])
with pd.option_context("display.max_rows", 2):
    strrepr = repr(s).replace('\n', '')
#assert(getndots(strrepr) == 3)
print(getndots(strrepr))
# CORRECTIONS:
print("-->  End: Test 32 test_truncate_ndots  <--")

print("Look into:")
print("--> Non-failing tests: 6, 10, 32")
print("--> Need opinions about formatting here")
