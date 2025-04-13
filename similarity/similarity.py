import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_watchlist, fetch_diary, fetch_likers, fetch_statistics, followable, get_member_id

# TODO: Currently only properly handles two users
# users = ['JoWz', get_member_id()]
users = ['6L7hn', get_member_id()] # '6L7hn', 

'''
1. Get all watchlist movies
2. Get all rated movies

Intersections of watchlist
'''

# Fetch all of the info
user_info = {}
for user in users:
  # Get all of the movies in their watchlist
  diary = fetch_diary(user)
  watchlist = fetch_watchlist(user)
  
  user_info[user] = {
    'watchlist': {x['film_id']: x for x in watchlist},
    'diary': {x['film_id']: x for x in diary},
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
  
  # Movie intersections
  for film_id in user_info[user]['diary']:
    if film_id not in diary_intersection_by_similarity:
      diary_intersection_by_similarity[film_id] = []
    diary_intersection_by_similarity[film_id].append(user_info[user]['diary'][film_id])
  
print('== COMMON WATCHLIST ==')  
for film_id in watchlist_intersection:
  print(f'{watchlist_intersection[film_id]['name']} - https://boxd.it/{film_id}')

print()
print('== DIFFERING RATINGS ==')
for film in diary_intersection_by_similarity:
  # If everyone reviewed it a rating
  if len(diary_intersection_by_similarity[film]) == len(users):
    rating_one = diary_intersection_by_similarity[film][0]['rating']
    rating_two = diary_intersection_by_similarity[film][1]['rating']
    if rating_one is None or rating_two is None:
      continue
    # Get how close the ratings are
    diff = abs(rating_one - rating_two)
    # If they're far apart, print it out
    if (diff > 1.5):
      print(f'FAR APART: {diary_intersection_by_similarity[film][0]['name']} ({rating_one} vs {rating_two}) - https://boxd.it/{film}')
    # If they're close together, but that close rating is FAR from the average, then also interesting
    if (diary_intersection_by_similarity[film][0]['average_rating'] and diff < 0.6 and abs(diary_intersection_by_similarity[film][0]['average_rating'] - (rating_one + rating_two) / 2.0) > 1.5):
      print(f'BUCKING THE TREND: {diary_intersection_by_similarity[film][0]['name']} ({rating_one} and {rating_two} vs. {diary_intersection_by_similarity[film][0]['average_rating']}) - https://boxd.it/{film}')
      
    
