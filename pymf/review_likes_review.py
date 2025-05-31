import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_reviews, fetch_review_likes, fetch_likers, fetch_reviews_liked, get_member_id

# Get a review
film = '7nZE'
review = '7yGa5h'
member_id = get_member_id()
max_likes = 30
min_likes = 0
rating_range = [2.5, 5] # inclusive
# Get everyone who liked that review and also reviewed the movie, and has < max_likes on their review
review_likers = fetch_likers(review, force_review=True)
for liker in review_likers:
  # Skip it if it's out of the range
  review_rating = liker['rating']
  if review_rating is None or review_rating < rating_range[0] or review_rating > rating_range[1]:
    continue
  num_likes = fetch_review_likes(liker['review_id'])
  if num_likes < max_likes and num_likes > min_likes:
    # If it's under, get the list of users who liked the review who also had a review
    likers = [x['id'] for x in fetch_likers(liker['review_id'], force_review=True)]
    if len(likers) < 1:
      continue
    # If it includes you, skip it
    if member_id in likers:
      continue
    # Also get the list of users who the reviewer liked
    reviews_liked = fetch_reviews_liked(liker['id'], film)
    users_who_reviewer_liked = set()
    for review_liked in reviews_liked:
      users_who_reviewer_liked.add(review_liked['reviewer_id'])
    
    reciprocal = 0
    for l in likers:
      if l in users_who_reviewer_liked:
        reciprocal += 1
        
    rate = reciprocal * 100.0 / len(likers)
    if (rate > 40):
      print(f'https://boxd.it/{liker['review_id']} [?] - {reciprocal} out of {len(likers)}: {reciprocal * 100.0 / len(likers)}')
    