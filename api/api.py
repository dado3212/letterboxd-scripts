import requests, json, os, time, urllib
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

def fetch_diary():
  entries = []
  cursor = None
  num_pages = 1
  
  while True:
    params = {
      'perPage': '100',
      'sort': 'Date',
      'member': MEMBER_ID,
      'memberRelationship': 'Owner',
      'where': 'HasDiaryDate',
    }
    if cursor:
      params['cursor'] = cursor
    response = requests.get('https://api.letterboxd.com/api/v0/log-entries', headers=HEADERS, cookies=COOKIES, params=params).json()
    for item in response['items']:
      try:
        entries.append({
          'watched_date': item['diaryDetails']['diaryDate'],
          'name': item['film']['name'],
          'rating': item.get('rating'), # can be unrated
        })
      except Exception as e:
        print(e)
        print(item)
        raise e

    if 'next' not in response:
      break
    print(f"Going to page {num_pages}")
    num_pages += 1
    cursor = response['next']
    
  return entries
