import requests

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_list

# tnoCm -> letterboxd posters
items = fetch_list('yLQLO')
# yLQLO

folder = 'posters'

folder_path = os.path.join(os.path.dirname(__file__), folder)
if not os.path.exists(folder_path):
  os.makedirs(folder_path)

for item in items:
  print(item['name'])
  open(os.path.join(os.path.dirname(__file__), folder, f'{item['name']}.jpg'), 'wb').write(requests.get(item['poster_url']).content)
