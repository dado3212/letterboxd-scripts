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

```
python star_animation/create_star_animation.py
```

## Thanks

There are lots of great resources for the APIs. Thanks to <TODO: insert links>

Thanks to Letterboxd for being a great service, and for the use of the [font](https://s.ltrbxd.com/fonts/Graphik-Regular-Web.woff) used for replicating the UI in various scripts. All rights go to Letterboxd.