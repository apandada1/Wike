# wikipedia.py
#
# This file is part of Wike, a Wikipedia Reader for the GNOME Desktop.
# Copyright 2021 Hugo Olabera <hugolabe@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import requests


# create a session for wikipedia requests

_session = requests.Session()
_api = 'https://en.wikipedia.org/w/api.php'

# Set api uri for selected language

def set_lang(lang):
  global _api
  _api = 'https://' + lang + '.wikipedia.org/w/api.php'

# Get Wikipedia random page

def get_random():
  params = { 'action': 'query',
             'generator': 'random',
             'grnlimit': 1,
             'grnnamespace': 0,
             'prop': 'info',
             'inprop': 'url',
             'format': 'json' }

  result = _request(params)
  pages = result['query']['pages']
  for page, info in pages.items():
    uri = info['fullurl']

  return uri

# Search in Wikipedia with a limit of responses

def search(text, limit):
  params = { 'action': 'opensearch',
             'search': text,
             'limit': limit,
             'namespace': 0,
             'redirects': 'resolve',
             'format': 'json' }

  result = _request(params)

  if len(result[1]) == 0:
    return None
  else:
    return result[1], result[3]

# Get sections and langlinks for Wikipedia page

def get_properties(page, lang):
  api = 'https://' + lang + '.wikipedia.org/w/api.php'
  params = api + '?format=json&action=parse&prop=sections|langlinks&redirects&page=' + page

  result = _request(params)

  return result['parse']

# Perform query to Wikipedia API with given parameters

def _request(params):
  global _session
  global _api
  headers = { 'User-Agent': 'Wike/1.5.0 (https://github.com/hugolabe)' }

  if type(params) is dict:
    response = _session.get(url=_api, params=params, headers=headers, timeout=(4, 12))
  else:
    response = _session.get(url=params, params=None, headers=headers, timeout=(4, 12))

  return response.json()

