#!/usr/bin/env python
import pandas as pd
import numpy as np

# Test 1
frame = pd.DataFrame(data={0: 0, 1: 0}, index=[0])
formatter = lambda x: '{:10.3f}'.format(x)
string = frame.to_string()
print('--> Begin Test 1 <--')
print(string)
print('-->  End Test 1  <--')

# Test 2
df = pd.DataFrame(np.random.randn(3, 3), columns=['one', 'two', 'three'])
string = df.to_string()
print('--> Begin Test 2 <--')
print(string)
print('-->  End Test 2  <--')

# Test 3
df = pd.DataFrame({'a':range(5)})
string = df.to_string()
print('--> Begin Test 3 <--')
print(string)
print('-->  End Test 3  <--')

# Test 4
NAMES = ['Short', 'Longer', 'Much Longer name to the Max -----------']
VALUES = [1, 9374518, 32432]
d = pd.DataFrame({'Name': NAMES, 'Value': VALUES})
string = d.to_string()
print('--> Begin Test 4 <--')
print(string)
print('-->  End Test 4  <--')
