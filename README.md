# <img src='https://a.ltrbxd.com/logos/letterboxd-decal-dots-pos-rgb-500px.png' height='34' /> Letterboxd Scripts

There's a [Letterboxd API](https://api-docs.letterboxd.com/) but it's a mostly private API [here](https://letterboxd.com/api-beta/). In the past I've used a combination of TMDb's API, scraping Letterboxd, or using their `.zip` export (for [Letterboxd Gaps](https://alexbeals.com/projects/letterboxd/) and [letterboxd-anim](https://github.com/dado3212/letterboxd-anim) among others. But if you happen to get access to the API ([\*cough\*](#notyet)) then these are some of the scripts that I've used in the past.

## Installation

Get an API key, either through the formal process or...[other ways](#notyet).

Create a `secret.py` file in the `api` folder with the following data. Details coming soon on how to best do this.
```
COOKIES = {
  '_ga': 'GA**',
  '_ga_**': 'GS1**',
  'com.xk72.webparts.csrf': '**',
  'letterboxd.signed.in.as': '**'
}
CLIENT_ID = '**'
CLIENT_SECRET = '**'
REFRESH_TOKEN = '**'
MEMBER_ID = '**'
```

> [!NOTE]  
> The requirements.txt file is for all subscripts, so it may be unnecessary depending on which part you're runnning.

```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Running

```
source venv/bin/activate
```

### Review Animation
```
python star_animation/create_star_animation.py
```

Creates an animation of the evolution of your rating curve over time.

![animation-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/395ae947-acab-479a-941e-5fae769da49f)

### Diary Snapshot

```
python month_diary/create_diary.py 2025 3
```

Given a month and a year it creates an HTML file of all watches in that month that's autoformatted for screenshots.

<img width="1319" alt="Screenshot 2025-04-14 at 3 47 53 PM" src="https://github.com/user-attachments/assets/0a782624-8ccb-4c7e-9e13-536326d4560f" />

### Timeline Graph

```
python graph/build_graph.py
```

Creates an interactive HTML page with a graph of your movies over time, split down by total watched, ratings, tags, watchlist, etc.

<img width="1464" alt="Screenshot 2025-04-14 at 3 59 33 PM" src="https://github.com/user-attachments/assets/1e013703-e543-4b0d-b3b7-467af657b0b3" />

### Similarity
```
python similarity/similarity.py
```

Takes in a list of users and finds common movies in their watchlist, along with movies where they significantly disagreed (or agreed, but contrary to average ratings).

<img width="702" alt="Screenshot 2025-04-14 at 4 10 45 PM" src="https://github.com/user-attachments/assets/f6484e8c-23af-44a4-8c2c-313da5a14ed6" />

```
python pymf/followers.py
```

```
python pymf/review_likes.py
```

## TODO

* Properly type API
* Fix imports
* Individual READMEs
* Improve reviews you might like/people you may follow algorithms
* Add in list reordering by color

## Thanks

There are lots of great resources for the APIs. Thanks to <TODO: insert links>

Thanks to Letterboxd for being a great service, and for the use of the [font](https://s.ltrbxd.com/fonts/Graphik-Regular-Web.woff) used for replicating the UI in various scripts. All rights go to Letterboxd.
