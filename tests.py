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
# CORRECTIONS:
print("-->  End: Test 11 test_to_latex_format  <--")

# Test 12 test_to_latex_longtable
print("--> Begin: Test 12 test_to_latex_longtable <--")
# CORRECTIONS:
print("-->  End: Test 12 test_to_latex_longtable  <--")

# Test 13 test_to_latex_multiindex
print("--> Begin: Test 13 test_to_latex_multiindex <--")
# CORRECTIONS:
print("-->  End: Test 13 test_to_latex_multiindex  <--")

# Test 14 test_to_latex_no_header
print("--> Begin: Test 14 test_to_latex_no_header <--")
# CORRECTIONS:
print("-->  End: Test 14 test_to_latex_no_header  <--")

# Test 15 test_to_string_float_index
print("--> Begin: Test 15 test_to_string_float_index <--")
# CORRECTIONS:
print("-->  End: Test 15 test_to_string_float_index  <--")

# Test 16 test_to_string_format_na
print("--> Begin: Test 16 test_to_string_format_na <--")
# CORRECTIONS:
print("-->  End: Test 16 test_to_string_format_na  <--")

# Test 17 test_to_string_index_formatter
print("--> Begin: Test 17 test_to_string_index_formatter <--")
# CORRECTIONS:
print("-->  End: Test 17 test_to_string_index_formatter  <--")

# Test 18 test_to_string_left_justify_cols
print("--> Begin: Test 18 test_to_string_left_justify_cols <--")
# CORRECTIONS:
print("-->  End: Test 18 test_to_string_left_justify_cols  <--")

# Test 19 test_to_string_line_width
print("--> Begin: Test 19 test_to_string_line_width <--")
# CORRECTIONS:
print("-->  End: Test 19 test_to_string_line_width  <--")

# Test 20 test_to_string_no_header
print("--> Begin: Test 20 test_to_string_no_header <--")
# CORRECTIONS:
print("-->  End: Test 20 test_to_string_no_header  <--")

# Test 21 test_to_string_no_index
print("--> Begin: Test 21 test_to_string_no_index <--")
# CORRECTIONS:
print("-->  End: Test 21 test_to_string_no_index  <--")

# Test 22 test_to_string_with_formatters
print("--> Begin: Test 22 test_to_string_with_formatters <--")
# CORRECTIONS:
print("-->  End: Test 22 test_to_string_with_formatters  <--")

# Test 23 test_east_asian_unicode_series
print("--> Begin: Test 23 test_east_asian_unicode_series <--")
# CORRECTIONS:
print("-->  End: Test 23 test_east_asian_unicode_series  <--")

# Test 24 test_format_explicit
print("--> Begin: Test 24 test_format_explicit <--")
# CORRECTIONS:
print("-->  End: Test 24 test_format_explicit  <--")

# Test 25 test_period
print("--> Begin: Test 25 test_period <--")
# CORRECTIONS:
print("-->  End: Test 25 test_period  <--")

# Test 26 test_to_string_dtype
print("--> Begin: Test 26 test_to_string_dtype <--")
# CORRECTIONS:
print("-->  End: Test 26 test_to_string_dtype  <--")

# Test 27 test_to_string_header
print("--> Begin: Test 27 test_to_string_header <--")
# CORRECTIONS:
print("-->  End: Test 27 test_to_string_header  <--")

# Test 29 test_to_string_length
print("--> Begin: Test 29 test_to_string_length <--")
# CORRECTIONS:
print("-->  End: Test 29 test_to_string_length  <--")

# Test 30 test_to_string_mixed
print("--> Begin: Test 30 test_to_string_mixed <--")
# CORRECTIONS:
print("-->  End: Test 30 test_to_string_mixed  <--")

# Test 31 test_to_string_name
print("--> Begin: Test 31 test_to_string_name <--")
# CORRECTIONS:
print("-->  End: Test 31 test_to_string_name  <--")

# Test 32 test_truncate_ndots
print("--> Begin: Test 32 test_truncate_ndots <--")
# CORRECTIONS:
print("-->  End: Test 32 test_truncate_ndots  <--")

print("Look into:")
print("--> Non-failing tests: 6, 10")
