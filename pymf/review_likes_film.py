import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_reviews, fetch_review_likes, fetch_likers, fetch_reviews_liked, get_member_id

film = 'KQMM'
member_id = get_member_id()
max_likes = 30
max_rating = 5
reviews = fetch_reviews(film, max_pages=10, max_likes=max_likes)
for review in reviews:
  num_likes = fetch_review_likes(review['review_id'])
  if review['rating'] is not None and review['rating'] > max_rating:
    continue
  if num_likes < max_likes:
    # If it's under, get the list of users who liked the review who also had a review
    likers = [x['id'] for x in fetch_likers(review['review_id'], force_review=True)]
    if len(likers) < 5:
      continue
    # If it includes you, skip it
    if member_id in likers:
      continue
    # Also get the list of users who the reviewer liked
    reviews_liked = fetch_reviews_liked(review['reviewer_id'], film)
    users_who_reviewer_liked = set()
    for review_liked in reviews_liked:
      users_who_reviewer_liked.add(review_liked['reviewer_id'])
    
    reciprocal = 0
    for liker in likers:
      if liker in users_who_reviewer_liked:
        reciprocal += 1
        
    rate = reciprocal * 100.0 / len(likers)
    if (rate > 45):
      print(f'https://boxd.it/{review['review_id']} [{review['rating']}, {review['reviewer_name']}] - {reciprocal} out of {len(likers)}: {reciprocal * 100.0 / len(likers)}')
    