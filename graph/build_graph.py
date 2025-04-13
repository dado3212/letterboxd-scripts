import csv
import plotly.graph_objects as go
from collections import defaultdict
import pandas as pd

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_diary, fetch_watchlist

movies = fetch_diary()
watchlist = fetch_watchlist()

# Convert data into a DataFrame
df = pd.DataFrame(movies)
df['watched_date'] = pd.to_datetime(df['watched_date'])
df['rating'] = df['rating'].fillna(-1)

# Watchlist
df2 = pd.DataFrame(watchlist)
df2['watched_date'] = pd.to_datetime(df2['added_date'])
grouped2 = df2.groupby('watched_date')
date_to_group_watchlist = {date: group for date, group in grouped2}

# Group by date
grouped = df.groupby('watched_date')
dates = []
total_count = []
liked_count = []
rewatched_count = []
watchlist_count = []
rating_counts = defaultdict(list)
tag_counts = defaultdict(list)

cumulative_total = 0
cumulative_liked = 0
cumulative_rewatched = 0
cumulative_watchlist = 0
cumulative_ratings = defaultdict(int)
cumulative_tags = defaultdict(int)

all_dates = pd.date_range(start=df['watched_date'].min(), end=df['watched_date'].max())
date_to_group = {date: group for date, group in grouped}

for date in all_dates:
  dates.append(date)
  if date in date_to_group:
    group = date_to_group[date]
    cumulative_total += len(group)
    cumulative_liked += group['liked'].sum()
    cumulative_rewatched += group['rewatched'].sum()

    all_tags = sum(group['tags'].tolist(), [])
    for tag in set(all_tags):
      count = all_tags.count(tag)
      cumulative_tags[tag] += count

    for rating in group['rating'].unique():
      count = len(group[group['rating'] == rating])
      cumulative_ratings[rating] += count
      
  if date in date_to_group_watchlist:
    cumulative_watchlist += len(date_to_group_watchlist[date])

  total_count.append(cumulative_total)
  liked_count.append(cumulative_liked)
  rewatched_count.append(cumulative_rewatched)
  watchlist_count.append(cumulative_watchlist)

  for rating in cumulative_ratings:
    rating_counts[rating].append(cumulative_ratings[rating])

  for tag in cumulative_tags:
    tag_counts[tag].append(cumulative_tags[tag])

# Fill gaps with zeros for ratings and tags before their first appearance
for rating in rating_counts:
  while len(rating_counts[rating]) < len(dates):
    rating_counts[rating].insert(0, 0)

for tag in tag_counts:
  while len(tag_counts[tag]) < len(dates):
    tag_counts[tag].insert(0, 0)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=total_count, mode='lines', name='Total'))
fig.add_trace(go.Scatter(x=dates, y=liked_count, mode='lines', name='Liked'))
fig.add_trace(go.Scatter(x=dates, y=rewatched_count, mode='lines', name='Rewatched'))
fig.add_trace(go.Scatter(x=dates, y=watchlist_count, mode='lines', name='Watchlist'))

for rating, counts in rating_counts.items():
  if rating != -1:
    fig.add_trace(go.Scatter(x=dates, y=counts, mode='lines', name=f'Rating {rating}'))

for tag, counts in tag_counts.items():
  fig.add_trace(go.Scatter(x=dates, y=counts, mode='lines', name=f'Tag {tag}'))

fig.update_layout(title='Movies Watched Over Time (Cumulative)', xaxis_title='Date', yaxis_title='Number of Movies')

# Save as HTML
fig.write_html(os.path.join(os.path.dirname(__file__), 'movies_graph.html'))
