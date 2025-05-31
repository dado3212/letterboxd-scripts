import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_fans, fetch_statistics, followable

from itertools import combinations

favorite_movies = [
  '43bI', # about time
  'cUqs', # your name
  '1XLm', # incredibles
  'dYmm', # cmbyn
]

# Get all combinations of favorites, starting from the most of them
all_combinations = []
for r in range(len(favorite_movies), 0, -1):
  all_combinations.extend(combinations(favorite_movies, r))

# If you want to print them:
for combo in all_combinations:
  print()
  print(combo)
  fans = fetch_fans(list(combo), 2)
  for fan in fans:
    info = fetch_statistics(fan['id'])
    if info['reviewLikes'] > 500 and info['watches'] > 50 and info['diaryEntriesThisYear'] > 5:
      if followable(fan['id']):
        print('https://boxd.it/' + fan['id'] + ': ' + fan['name'] + ' - ' + str(info['reviewLikes']) + ' - ' + str(round(info['following'] * 100.0 / info['followers']) / 100))
