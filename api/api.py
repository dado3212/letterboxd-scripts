import requests, os, time, json
from typing import Optional
from .secret import COOKIES, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, MEMBER_ID

HEADERS = {
  'Accept': '*/*',
  'User-Agent': 'Letterboxd/6499 CFNetwork/3826.400.120 Darwin/24.3.0',
  'Host': 'api.letterboxd.com',
  'Connection': 'keep-alive',
  'Cache-Control': 'no-cache',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9',
}

def fetch_token():
  # Try and get the token from where we saved it in a file
  token = None
  token_path = os.path.join(os.path.dirname(__file__), 'token.txt')
  if os.path.exists(token_path):
    with open(token_path, 'r') as f:
      token, expires = f.read().split('\t')
      # If it's stale we need to refetch it
      if int(time.time()) > int(expires):
        print('Token too old, refetching')
        token = None
  if (token is not None):
    return token
  params = {
    'grant_type': 'refresh_token',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'refresh_token': REFRESH_TOKEN,
  }
  headers = HEADERS
  headers['Content-Type'] = 'application/x-www-form-urlencoded'
  headers['Accept'] = 'application/json'
  response = requests.post('https://api.letterboxd.com/api/v0/auth/token', headers=headers, cookies=COOKIES, data=params).json()
  token = response['access_token']
  expires = int(time.time()) + int(response['expires_in'])
  # Update the file
  with open(token_path, 'w') as f:
    f.write(f'{token}\t{expires}')
  return token

# TODO: Hacky, remove this to have a proper API authorization function
HEADERS['Authorization'] = f'Bearer {fetch_token()}'

def fetch_diary(member: str = MEMBER_ID, year: Optional[int] = None, month: Optional[int] = None):
  entries = []
  cursor = None
  num_pages = 1
  
  while True:
    params = {
      'perPage': '100',
      'sort': 'Date',
      'member': member,
      'memberRelationship': 'Owner',
      'where': 'HasDiaryDate',
    }
    if year:
      params['year'] = year
    if month:
      params['month'] = month
    if cursor:
      params['cursor'] = cursor
    response = requests.get('https://api.letterboxd.com/api/v0/log-entries', headers=HEADERS, cookies=COOKIES, params=params).json()
    for item in response['items']:
      entries.append({
        'watched_date': item['diaryDetails']['diaryDate'],
        'name': item['film']['name'],
        'rating': item.get('rating'), # can be unrated
        'rewatched': item['diaryDetails']['rewatch'],
        'liked': item['like'],
        'poster_url': item['film']['poster']['sizes'][-1]['url'] if 'poster' in item['film'] else None,
        'tags': item.get('tags') or [],
        'review_id': item['id'],
        'film_id': item['film']['id'],
        'average_rating': item['film'].get('rating'),
      })

    if 'next' not in response:
      break
    print(f"Diary page {num_pages}")
    num_pages += 1
    cursor = response['next']
    
  return entries

def fetch_watchlist(member: str = MEMBER_ID):
  entries = []
  cursor = None
  num_pages = 1
  
  while True:
    params = {
      'perPage': '100',
      'sort': 'DateLatestFirst',
    }
    if cursor:
      params['cursor'] = cursor
    response = requests.get(f'https://api.letterboxd.com/api/v0/member/{member}/watchlist', headers=HEADERS, cookies=COOKIES, params=params).json()
    for item in response['items']:
      entries.append({
        'added_date': item['relationships'][-1]['relationship']['whenAddedToWatchlist'].split("T")[0],
        'name': item['name'],
        'poster_url': item['poster']['sizes'][-1]['url'] if 'poster' in item else None,
        'film_id': item['id'],
      })

    if 'next' not in response:
      break
    print(f"Watchlist page {num_pages}")
    num_pages += 1
    cursor = response['next']
    
  return entries

# TODO: Unused
def fetch_followers_list(member):
  params = {
    'perPage': '100',
    'sort': 'Date',
    'member': member,
    'memberRelationship': 'IsFollowedBy'
  }
  response = requests.get('https://api.letterboxd.com/api/v0/members', headers=HEADERS, cookies=COOKIES, params=params)
  a = response.json()
  print(json.dumps(a, indent=2))
  print(len(a['items']))
  
def fetch_statistics(member):
  statistics_url = f'https://api.letterboxd.com/api/v0/member/{member}/statistics'
  response = requests.get(statistics_url, headers=HEADERS, cookies=COOKIES).json()
  return {
    'reviewLikes': response['counts']['reviewLikes'],
    'diaryEntries': response['counts']['diaryEntries'],
    'diaryEntriesThisYear': response['counts']['diaryEntriesThisYear'],
    'reviews': response['counts']['reviews'],
    'followers': response['counts']['followers'],
    'following': response['counts']['following'],
    'watches': response['counts']['watches'],
    'ratings': response['counts']['ratings'],
  }
  
def followable(member):
  url = f'https://api.letterboxd.com/api/v0/member/{member}/me'
  response = requests.get(url, headers=HEADERS, cookies=COOKIES).json()
  return not response['following'] and not response['followedBy'] and not response['blocking'] and not response['blockedBy']

def get_member_id():
  return MEMBER_ID

def fetch_likers(review, force_review = False, include_no_review = False, include_review = False):
  likers = []
  cursor = None
  num_pages = 1
  
  while True:
    params = {
      'perPage': '100',
      'sort': 'Date',
    }
    if cursor:
      params['cursor'] = cursor
    response = requests.get(f'https://api.letterboxd.com/api/v0/log-entry/{review}/members', headers=HEADERS, cookies=COOKIES, params=params).json()
    for item in response['items']:
      if (force_review):
        if (len(item['relationship']['reviews']) > 0):
          likers.append({
            'id': item['member']['id'],
            'watched': item['relationship']['watched'],
          })
      else:
        if (
          not item['relationship']['watched'] or
          (include_no_review and len(item['relationship']['reviews']) == 0) or
          (include_review and len(item['relationship']['reviews']) > 0)
        ):
          likers.append({
            'id': item['member']['id'],
            'watched': item['relationship']['watched'],
          })

    if 'next' not in response:
      break
    print(f"Going to page {num_pages}")
    num_pages += 1
    cursor = response['next']
  return likers

def fetch_review_likes(review) -> int:
  response = requests.get(f'https://api.letterboxd.com/api/v0/log-entry/{review}/statistics', headers=HEADERS, cookies=COOKIES).json()
  try:
    return response['counts']['likes']
  except:
    print(response)
    return response['counts']['likes']

def get_index_first_review_under_likes(reviews, max_likes: int) -> Optional[int]:
  left, right = 0, len(reviews) - 1
  result = None

  while left <= right:
    mid = (left + right) // 2
    likes = fetch_review_likes(reviews[mid]['id'])

    if likes < max_likes:
      result = mid
      right = mid - 1
    else:
      left = mid + 1

  return result
  
# NOTE: Because ReviewPopularity is not strictly like count, this can return reviews
# that have more than max_likes (though it's hopefully close)
def fetch_reviews(film, max_pages: Optional[int] = None, max_likes: Optional[int] = None):
  reviews = []
  cursor = None
  num_pages = 1
  found_max = False
  
  while max_pages is None or num_pages <= max_pages:
    params = {
      'perPage': '100',
      'sort': 'ReviewPopularity',
      'film': film,
    }
    if cursor:
      params['cursor'] = cursor
    response = requests.get('https://api.letterboxd.com/api/v0/log-entries', headers=HEADERS, cookies=COOKIES, params=params).json()
    response_items = response['items']
    # If you've set a max likes and the last entry sorted by likes is too high, just go to the next page
    if max_likes and not found_max:
      last_review_likes = fetch_review_likes(response['items'][-1]['id'])
      if (last_review_likes > max_likes):
        if 'next' not in response:
          break
        print(f"Skipping page, too popular")
        cursor = response['next']
        continue
      # Now you've found it, find the first entry that's under max_likes
      first_index = get_index_first_review_under_likes(response_items, max_likes)
      assert first_index is not None, "You have to find one I think"
      response_items = response_items[first_index:]
      # From now on, don't need to check any of this while paginating
      found_max = True
        
    for item in response_items:
      reviews.append({
        'watched_date': item['diaryDetails']['diaryDate'] if 'diaryDetails' in item else item['whenCreated'].split("T")[0],
        'name': item['film']['name'],
        'rating': item.get('rating'), # can be unrated
        'rewatched': item['diaryDetails']['rewatch'] if 'diaryDetails' in item else False, # just treat as not a rewatch if not listed
        'liked': item['like'],
        'poster_url': item['film']['poster']['sizes'][-1]['url'] if 'poster' in item['film'] else None,
        'tags': item.get('tags') or [],
        'review_id': item['id'],
        'reviewer_id': item['owner']['id'],
        'reviewer_name': item['owner']['displayName'],
      })

    if 'next' not in response:
      break
    num_pages += 1
    print(f"Going to page {num_pages}")
    cursor = response['next']
    
  return reviews

def fetch_reviews_liked(member, film):
  reviews = []
  cursor = None
  num_pages = 1
  
  while True:
    params = {
      'perPage': '100',
      'sort': 'WhenLiked',
      'film': film,
      'member': member,
      'memberRelationship': 'Liked',
      'where': 'HasReview',
    }
    if cursor:
      params['cursor'] = cursor
    response = requests.get('https://api.letterboxd.com/api/v0/log-entries', headers=HEADERS, cookies=COOKIES, params=params).json()
    response_items = response['items']
        
    for item in response_items:
      reviews.append({
        'watched_date': item['diaryDetails']['diaryDate'] if 'diaryDetails' in item else item['whenCreated'].split("T")[0],
        'name': item['film']['name'],
        'rating': item.get('rating'), # can be unrated
        'rewatched': item['diaryDetails']['rewatch'] if 'diaryDetails' in item else False, # just treat as not a rewatch if not listed
        'liked': item['like'],
        'poster_url': item['film']['poster']['sizes'][-1]['url'] if 'poster' in item['film'] else None,
        'tags': item.get('tags') or [],
        'review_id': item['id'],
        'reviewer_id': item['owner']['id'],
      })

    if 'next' not in response:
      break
    num_pages += 1
    print(f"Going to page {num_pages}")
    cursor = response['next']
    
  return reviews