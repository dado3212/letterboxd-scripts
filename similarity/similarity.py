import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_watchlist, fetch_diary, fetch_likers, fetch_statistics, followable, get_member_id

# TODO: Currently only properly handles two users
users = ['JoWz', get_member_id()] # '6L7hn', 

'''
1. Get all watchlist movies
2. Get all rated movies

Intersections of watchlist
'''

# Fetch all of the info
user_info = {}
for user in users:
  # Get all of the movies in their watchlist
  watchlist = fetch_watchlist(user)
  diary = fetch_diary(user)
  
  user_info[user] = {
    'watchlist': {x['id']: x['name'] for x in watchlist},
    'diary': {x['film_id']: x['rating'] for x in diary},
  }
  
# Process it
watchlist_intersection = None

diary_intersection_by_similarity = {}

for user in user_info:
  # Intersections of watchlist
  if watchlist_intersection is None:
    watchlist_intersection = user_info[user]['watchlist']
  else:
    watchlist_intersection = {id: watchlist_intersection[id] for id in watchlist_intersection.keys() & user_info[user]['watchlist'].keys()}
    
  # TODO: Recommendations for watchlist where other person rated highly?
  
  for film_id in user_info[user]['diary']:
    if film_id not in diary_intersection_by_similarity:
      diary_intersection_by_similarity[film_id] = {'ratings': [user_info[user]['diary'][film_id]] if user_info[user]['diary'][film_id] else []}
    elif user_info[user]['diary'][film_id]:
      diary_intersection_by_similarity[film_id]['ratings'].append(user_info[user]['diary'][film_id])

print(watchlist_intersection)

for film in diary_intersection_by_similarity:
  if len(diary_intersection_by_similarity[film]['ratings']) == len(users):
    # TODO: Handle more users
    diff = abs(diary_intersection_by_similarity[film]['ratings'][0] - diary_intersection_by_similarity[film]['ratings'][1])
    if diff > 1.5:
      print(f'https://boxd.it/{film}')
      print(diary_intersection_by_similarity[film])