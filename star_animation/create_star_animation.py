import copy, imageio
from typing import TypedDict, Optional, Any
from PIL import Image, ImageDraw, ImageFont

# TODO: Fix this
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_diary

class Movie(TypedDict):
    name: str
    rating: Optional[float] # out of 5

def map_diary_into_movies(diary_entries: list) -> dict[str, list[Movie]]:
    movies: dict[str, list[Movie]] = {}

    for entry in diary_entries:
        if entry['watched_date'] not in movies:
            movies[entry['watched_date']] = []
            movies[entry['watched_date']].append({
                'name': entry['name'],
                'rating': entry['rating'],
            })
    return movies

# For a current distribution of movies, creates a single Image frame
def create_image(bucket_info: dict[float, list[Movie]], count: int, scale: int):
    # Dimensions of the frames and GIF
    width: int = 256 * scale # actually 250 on the website
    height: int = 80 * scale

    frame = Image.new('RGB', (width, height), '#14181c')

    # Create a drawing object
    draw = ImageDraw.Draw(frame)

    # Draw the ratings text
    text = 'RATINGS'
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'resources', 'fonts', 'Graphik-Regular-Web.woff'), size=13 * scale)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_start_height = text_bbox[1]
    text_height = text_bbox[3]
    draw.text((1, 1), text, font=font, fill='#9ab')

    # Draw the number of reviews text
    text = str(count)
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'resources', 'fonts', 'Graphik-Regular-Web.woff'), size=11 * scale)
    text_bbox = draw.textbbox((0, 0), text, font=font)

    draw.text((width - text_bbox[2] - 1 * scale, text_start_height + text_height - text_bbox[3]), text, font=font, fill='#678')

    # Draw the underline
    draw.line(
        (0, text_height + text_start_height + 2 * scale, width, text_height + text_start_height + 2 * scale),
        fill='#456',
        width=1 * scale
    )

    # Calculate the boxes that we're going to draw
    boxes: list[int] = []
    highest: int = 0
    for key in bucket_info.keys():
        count = len(bucket_info[key])
        boxes.append(count)
        if (count > highest):
            highest = count

    box_width = 17 * scale
    box_max_height = 44 * scale

    offset = 15 * scale

    # Draw the boxes
    for count in boxes:
        draw.rectangle((
            offset,
            height - (box_max_height * 1.0 * count / highest) - 1,
            offset + box_width,
            height + 1,
        ), fill='#678')
        offset += box_width + 2 * scale

    # Draw the stars
    star_font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '..', 'resources', 'fonts', 'seguisym.ttf'), size=12*scale)
    text = '★'
    text_bbox = draw.textbbox((0, 0), text, font=star_font)
    text_start_height = text_bbox[1]
    text_height = text_bbox[3]
    draw.text((1 * scale, height - text_height - 1), text, font=star_font, fill='#00c030')

    text = '★★★★★'
    text_bbox = draw.textbbox((0, 0), text, font=star_font)
    text_width = text_bbox[2]
    text_height = text_bbox[3]
    draw.text((width - text_width, height - text_height - 1 * scale), text, font=star_font, fill='#00c030')

    # Append the frame to the list
    return frame

# Define the easing function
def ease(t: float) -> float:
    if t < 0.05:
        return 1
    elif t < 0.2:
        return 1 - ((t - 0.05) / 0.15)
    elif t < 0.95:
        return 0
    else:
        return (t - 0.95) / 0.05

# Takes in a list of movies and creates an animation
def create_and_save_animation(movies: dict[str, list[Movie]]):
    # Define the duration range (in seconds)
    target_duration_seconds = 10
    # How long to stay on the final frame for (in seconds)
    final_frame_duration = 1
    # MP4s don't loop by default. This allows you to calculate how many times
    # the generated MP4 will 'loop' by having the same set of frames repeated.
    num_loops = 1
    # Scale the created video. With a default scale of 1 it will generate 
    # a video with the dimensions of 256x80.
    scale_image = 4
    # How many frames to turn each frame into to give us wiggle room to ease
    # duration. At a scale effect of 2 we have len(frames) extra frames to work
    # with. Must be >= 1. Treat this as the "strength" of the easing function.
    scale_effect: int = 2

    animation_slices: list[dict[float, list[Movie]]] = []

    current_buckets: dict[float, list[Movie]] = {
        0.5: [],
        1: [],
        1.5: [],
        2: [],
        2.5: [],
        3: [],
        3.5: [],
        4: [],
        4.5: [],
        5: [],
    }
    for key in sorted(movies.keys()):
        day_list = movies[key]
        for movie in day_list:
            rating = movie['rating']
            if rating is not None:
                current_buckets[rating].append(movie)
                animation_slices.append(copy.deepcopy(current_buckets))    

    # Create a list to store frames
    frames: list[Any] = []
    for i, slice in enumerate(animation_slices):
        frames.append(create_image(slice, i + 1, scale_image))

    # Calculate durations for each frame. Effectively this ends up just being
    # calculating the easing function for each frame
    num_frames = len(frames)
    durations: list[float] = []
    for i in range(num_frames):
        t = i / (num_frames - 1)  # Normalized time between 0 and 1
        eased_t = ease(t)  # Apply easing function
        durations.append(eased_t)

    # Calculate FPS
    fps = round(len(movies) / target_duration_seconds)
    
    # Duplicate frames based on their durations
    num_frames = len(frames)
    total_duration = sum(durations)
    duplicated_frames: list[Any] = []
    for i in range(num_frames):
        frame = frames[i]
        t = i / (num_frames - 1)  # Normalized time between 0 and 1
        num_repetitions = int(1 + (durations[i] / total_duration) * ((scale_effect - 1) * num_frames))

        if i == num_frames - 1:
            num_repetitions = int(fps * scale_effect * final_frame_duration)
        duplicated_frames.extend([frame] * num_repetitions)

    # Save the frames as an animated mp4
    imageio.mimsave(os.path.join(os.path.dirname(__file__), 'animation.mp4'), duplicated_frames * num_loops, fps=fps * scale_effect)

# Example usage
diary = fetch_diary()
movies = map_diary_into_movies(diary)
create_and_save_animation(movies)