import csv, copy, math, requests
from typing import TypedDict, Optional, Any
from bs4 import BeautifulSoup

# TODO: Fix this
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_diary

# TODO: Properly type this
def create_website(movies):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Letterboxd Diary Month</title>
        <style>
            body {
                background-color: rgb(20, 24, 28);
                color: rgb(85, 102, 119);

                display: grid;
                justify-content: center;
                gap: 10px;
                margin: 20px 0;
                
                font-size: 1.2em;
            }

            .movie {
                position: relative;
            }

            .title {
                display: none;
            }

            img.poster {
                width: 100%;
                border-radius: 4px;
                border: 1px solid #ddeeff96;
            }

            .liked {
                display: inline-block;
                transform: scaleX(1.3);
                position: relative;
                bottom: 4px;
                right: -3px;
            }

            .rating {
                position: relative;
                top: -5px;
            }

            .rewatched {
                position: absolute;
                top: 0px;
                right: 0px;
                font-size: 30px;
                padding: 2px 2px 4px 4px;
                background: linear-gradient(45deg, transparent 0%, transparent 50%, rgb(0 0 0 / 77%) 53%, #1A5AB6 53%, #1A5AB6 100%);
                width: 40px;
                height: 42px;
                color: white;
                border-top-right-radius: 4px;
                text-align: right;
                vertical-align: top;
                line-height: 16px;
        }
        </style>
        <script>
            // Function to calculate the grid layout
            function calculateGridLayout() {
                const screenWidth = window.innerWidth - 30;
                const screenHeight = window.innerHeight - 70;

                const elementWidth = 30;
                const elementHeight = 45;
                const padding = 10;
                const verticalAdd = 27;
                const elementAspectRatio = elementWidth / elementHeight;

                let isHorizontalLayout = true;

                // Determine if the screen is taller than the element
                if (screenWidth / screenHeight < elementAspectRatio) {
                    isHorizontalLayout = false;
                }

                let minRow, maxRow, optimalColumns, optimalWidth, width, height;
    """
    html_content += "let numMovies = {num_movies}".format(num_movies=len(movies))
    html_content += """
                if (isHorizontalLayout) {
                    minRow = 1
                    maxRow = Math.floor(Math.sqrt(numMovies));
                } else {
                    minRow = Math.floor(Math.sqrt(numMovies)) - 1;
                    maxRow = numMovies;
                }

                let coverage = 0;
                for (var rows = minRow; rows <= maxRow; rows++) {
                    let columns = Math.ceil(numMovies / rows);

                    let maxSizedWidth = (screenWidth - (columns - 1) * padding) / columns;
                    let maxSizedHeight = (screenHeight - (rows - 1) * padding - rows * verticalAdd) / rows;

                    if (maxSizedWidth * elementHeight / elementWidth < maxSizedHeight) {
                        width = maxSizedWidth;
                        height = maxSizedWidth * elementHeight / elementWidth;
                    } else {
                        width = maxSizedHeight * elementWidth / elementHeight;
                        height = maxSizedHeight;
                    }

                    const currentCoverage = (width * columns) * (height * rows) / (screenWidth * screenHeight);

                    if (currentCoverage > coverage) {
                        coverage = currentCoverage;
                        optimalColumns = columns;
                        optimalWidth = width;
                    }
                }

                document.body.style.gridTemplateColumns = 'repeat(' + optimalColumns + ', auto)';
                document.querySelectorAll('.movie').forEach(element => {
                    element.style.width = optimalWidth + 'px';
                });
            }

            // Call the function on page load
            window.addEventListener('load', calculateGridLayout);
            // and reload
            window.addEventListener('resize', calculateGridLayout);
        </script>
    </head>
    <body>
    """

    for movie in movies:
        rating = ''
        if movie['rating'] is not None:
            for _ in range(math.floor(movie['rating'])):
                rating += '★'
            if (movie['rating'] % 1 == 0.5):
                rating += '½'

        html_content += '''
            <div class='movie'>
            <span class='title'>{name}</span>
            <img class='poster' src='{image}'>
            <span class='rating'>{rating}</span>
        '''.format(name=movie['name'], image=movie['poster_url'], rating=rating)
        if (movie['liked']):
            html_content += "<span class='liked'>♥</span>"
        if (movie['rewatched']):
            html_content += "<span class='rewatched'>⟳</span>"

        html_content += "</div>\n"

    html_content += "</body>\n</html>"

    # Save the HTML content to a file
    with open(os.path.join(os.path.dirname(__file__), 'index.html'), "w") as html_file:
        html_file.write(html_content)

diary = fetch_diary(year=2025, month=3)
create_website(diary[::-1])
