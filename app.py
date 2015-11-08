#!/usr/bin/env python
# Copyright 2015 Jacob Petrie

import os
import re

from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/', methods=['POST'])
def post_request():

  source_type = None
  source_values = None
  types = ('base10', 'base36')

  if 'source_type' in request.form.keys():
    source_type = request.form['source_type']

  if 'source_values' in request.form.keys():
    source_values = request.form['source_values']
    if source_values == '':
      source_values = None

  if source_type not in types:
    return render_template('error.html',
                           message='invalid source_type')

  if source_values is None:
    return render_template('error.html',
                           message='please provide values to convert')

  if source_type == 'base10':
    invalid_value_chars = r'[^0-9\r\n]'
  else:
    invalid_value_chars = r'[^a-zA-Z0-9\r\n]'

  pattern = re.compile(invalid_value_chars)
  if pattern.findall(source_values):
    return render_template('error.html', 
                           message='at least one invalid value was entered')

  source_values = source_values.replace("\r\n", "\n")

  values = source_values.split("\n")

  converted = []

  for i in values:
    # skip empty lines
    if not i:
      continue

    if source_type == 'base10':
      new_value = base36encode(int(i))
    else:
      new_value = base36decode(i)

    converted.append((i, new_value))

  if source_type == types[0]:
    new_type = types[1]
  else:
    new_type = types[0]

  return render_template('results.html',
                         converted=converted,
                         source_type=source_type,
                         new_type=new_type)


def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36.lower()


def base36decode(number):
    return int(number, 36)


if __name__ == '__main__':
  app.run(debug=True)
