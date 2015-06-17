import sys
import urllib
import urllib2
import json
from httplib2 import iri2uri

import media
import fresh_tomatoes

GOOGLE_API_KEY = "PLACEHOLDER GOOGLE API KEY"


def iri_to_uri(iri):
    """Transforms a unicode iri into a ascii uri.
    See http://stackoverflow.com/questions/9887223/"""
    if not isinstance(iri, unicode):
        raise TypeError('iri %r should be unicode.' % iri)
    return bytes(iri2uri(iri))


def save_image(url, file_name):
    """Saves an image from a url to the static/images/ folder"""
    image_file = urllib2.urlopen(url)
    output = open('static/images/' + file_name, 'wb')
    output.write(image_file.read())
    output.close()


def get_movie_info(movie_title):
    """Gets the title, plot, poster URL and trailer URL of a movie based on
    it's title, and returns a Movie object. The poster is saved in locally to
    avoid direct linking problems in the final site.
    The poster URL is also local."""

    # Get information using the omdb api and save it in the
    # dictionary movie_info_dict:
    url = u'http://www.omdbapi.com/?t=' + unicode(
        movie_title) + u'&plot=short&r=json'
    connection = urllib.urlopen(iri_to_uri(url))
    response = connection.read()
    connection.close()
    movie_info_dict = json.loads(response)

    # Save the poster image locally using the unique imdbID as a filename:
    imdb_id = movie_info_dict.get("imdbID", "noIDfound")
    try:
        poster_url = movie_info_dict.get('Poster')
        file_name = 'poster_' + imdb_id + '.jpg'
        save_image(poster_url, file_name)
    except:
        file_name = "default_poster.jpg"
        # From http://www.reelviews.net/resources/img/default_poster.jpg

    # Get the youtube trailer url and add it to the dictionary movie_info_dict:
    youtube_trailer_url = get_youtube_trailer_url(movie_title)
    movie_info_dict['Trailer'] = youtube_trailer_url

    # Return title, plot, (local) poster URL and trailer URL.
    return (movie_info_dict.get('Title', 'Title Not Found'),
            movie_info_dict.get('Plot', 'Plot Not Found'),
            'images/' + file_name,
            movie_info_dict['Trailer'])


def get_youtube_trailer_url(movie_title):
    """Uses the google api to to find the url of the trailer on youtube for a
    particular movie title. (Searches for movie_title + 'trailer' and returns
    the url of the first hit.)
    Returns a 'video not found' video if nothing is found."""
    try:
        youtube_api_search_url = \
            "https://www.googleapis.com/youtube/v3/search?part=id&q=" \
            + unicode(movie_title) \
            + "trailer" \
            + "&type=video&maxResults=1&key=" \
            + GOOGLE_API_KEY
        connection = urllib.urlopen(iri_to_uri(youtube_api_search_url))
        response = connection.read()
        connection.close()
        video_id = json.loads(response)['items'][0]['id']['videoId']
        youtube_url = "https://www.youtube.com/watch?v=" + video_id
    except:
        youtube_url = "https://www.youtube.com/watch?v=R7o1PnHas9M"
    return youtube_url


def main(movie_list):
    """Main function: gets movie information on list of movies (movie_list)
    and generates and displays html output."""

    # Alphabetises list of movie titles:
    movie_list.sort()

    # Download movie information and create list of Movie objects in movies:
    movies = []
    for movie in movie_list:
        print "Downloading " + movie + " information."
        movie_info = get_movie_info(movie)
        movie_object = media.Movie(*movie_info)
        movies.append(movie_object)

    # Create HTML output file and display in web browser:
    fresh_tomatoes.open_movies_page(movies)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Requires list of movie titles as the input argument.\n" \
              "E.g. 'Attack the Block' 'Avatar' 'Borat'"
    else:
        print "OK"
        main(sys.argv[1:])
