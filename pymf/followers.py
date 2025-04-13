import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_likers, fetch_statistics, followable

review_seed = '1nP61r'
unwatched_likers = fetch_likers(review_seed, include_no_review=False, include_review=True)
for unwatched_liker in unwatched_likers:
  info = fetch_statistics(unwatched_liker['id'])
  if info['reviewLikes'] > 2000 and info['watches'] > 100 and info['diaryEntriesThisYear'] > 5:
    if followable(unwatched_liker['id']):
      print('https://boxd.it/' + unwatched_liker['id'] + ' [' + ('Watched' if unwatched_liker['watched'] else 'Unwatched') + '] - ' + str(info['reviewLikes']) + ' - ' + str(round(info['following'] * 100.0 / info['followers']) / 100))
