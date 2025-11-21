import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_likers, fetch_statistics, followable

review_seed = 'b6a62J'
follower_ratio = 1
unwatched_likers = fetch_likers(review_seed, force_review=True, include_no_review=False, include_review=True)
# unwatched_likers = fetch_likers(review_seed, include_no_review=False, include_review=True)
for unwatched_liker in unwatched_likers:
  info = fetch_statistics(unwatched_liker['id'])
  if info['reviewLikes'] > 2000 and info['watches'] > 100 and info['diaryEntriesThisYear'] > 5:
    if followable(unwatched_liker['id']) and (info['followers'] > 0 and info['following'] * 1.0 / info['followers'] > follower_ratio):
      if unwatched_liker['watched']:
        watch_status = '[Watched]'
        if 'review_id' in unwatched_liker:
          watch_status += ' (https://boxd.it/' + unwatched_liker['review_id'] + ')'
      else:
        watch_status = '[Unwatched]'
      print('https://boxd.it/' + unwatched_liker['id'] + ': ' + unwatched_liker['name'] + ' ' + watch_status + ' - ' + str(info['reviewLikes']) + ' - ' + str(round(info['following'] * 100.0 / info['followers']) / 100))
