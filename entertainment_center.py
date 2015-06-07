__author__ = 'bryn'
GOOGLE_API_KEY = "PLACEHOLDER GOOGLE API KEY"

import urllib
import urllib2
import json
from httplib2 import iri2uri

import media
import fresh_tomatoes


def iri_to_uri(iri):
    """Transforms a unicode iri into a ascii uri.
    See http://stackoverflow.com/questions/9887223/
    how-to-request-a-url-with-non-unicode-carachters-on-main-domainname-not-params"""
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
    """Gets the title, plot, poster URL and trailer URL of a movie based on it's title, and returns a Movie object.
    The poster is saved in locally to avoid direct linking problems in the final site.  The poster URL is also local."""

    # Get information using the omdb api and save it in the dictionary movie_info_dict:
    url = u'http://www.omdbapi.com/?t=' + unicode(movie_title) + u'&plot=short&r=json'
    connection = urllib.urlopen(iri_to_uri(url))
    response = connection.read()
    connection.close()
    movie_info_dict = json.loads(response)

    # Save the poster image locally using the unique imdbID as a filename:
    imdb_ID = movie_info_dict.get("imdbID", "noIDfound")
    try:
        poster_url = movie_info_dict.get('Poster')
        file_name = 'poster_' + imdb_ID + '.jpg'
        save_image(poster_url, file_name)
    except:
        file_name = "default_poster.jpg"  # From http://www.reelviews.net/resources/img/default_poster.jpg

    # Get the youtube trailer url and add it to the dictionary movie_info_dict:
    youtube_trailer_url = get_youtube_trailer_url(movie_title)
    movie_info_dict['Trailer'] = youtube_trailer_url

    # Return title, plot, (local) poster URL and trailer URL.
    return movie_info_dict.get('Title', 'Title Not Found'), movie_info_dict.get('Plot', 'Plot Not Found'), \
           'images/' + file_name, movie_info_dict['Trailer']


def get_youtube_trailer_url(movie_title):
    """Uses the google api to to find the url of the trailer on youtube for a particular movie title.
    (Searches for movie_title + 'trailer' and returns the url of the first hit.)
    Returns a 'video not found' video if nothing is found."""
    try:
        youtube_api_search_url = "https://www.googleapis.com/youtube/v3/search?part=id&q=" + unicode(
            movie_title) + "trailer" + "&type=video&maxResults=1&key=" + GOOGLE_API_KEY
        connection = urllib.urlopen(iri_to_uri(youtube_api_search_url))
        response = connection.read()
        connection.close()
        video_id = json.loads(response)['items'][0]['id']['videoId']
        youtube_url = "https://www.youtube.com/watch?v=" + video_id
    except:
        youtube_url = "https://www.youtube.com/watch?v=R7o1PnHas9M"
    return youtube_url

# movie_info = get_movie_info("Inception")
# inception = media.Movie(*movie_info)


#favorite_movies = ["Tfwe0we0 fds"]
# favorite_movies = ["The Terminator", "Terminator 2", "Terminator 3"]
favorite_movies = ["Attack the Block","Borat", "Total Recall", "Kingsman", "Inglourious Basterds", "Battle Royale", "Starred Up", "Edge of Tomorrow", "Cabin in the Woods", "Run Lola Run", "Spirited Away", "The Internet's Own Boy", "It's a Disaster", "Rise of the Planet of the Apes", "Taken", "District 9", "Requiem for a Dream", "Oldboy","Avatar","Face/Off", "Guardians of the Galaxy", "Hostel", "John Wick", "Kill Bill", "Looper", "Moon", "Nightcrawler", "Prometheus", "Quantum of Solace", "Up", "V for Vendetta", "Warrior", "Wreck-it Ralph", "X-Men: First Class", "Your Highness", "Zombieland" ]
favorite_movies.sort()


movies = []
for movie in favorite_movies:
    print "Downloading " + movie + " information."
    movie_info = get_movie_info(movie)
    movie_object = media.Movie(*movie_info)
    movies.append(movie_object)

fresh_tomatoes.open_movies_page(movies)




# toy_story = media.Movie("Toy Story",
# "A boy's toys come to life and have an adventure.",
#                         "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
#                         "https://www.youtube.com/watch?v=KYz2wyBy3kc")
#
# avatar = media.Movie("Avatar",
#                      "A boy falls in love with a blue girl.",
#                      "http://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg",
#                      "https://www.youtube.com/watch?v=5PSNL1qE6VY")
#
# kingsman = media.Movie("Kingsman - The Secret Service",
#                        "A boy fights to save the world from a super-villain",
#                        "http://upload.wikimedia.org/wikipedia/en/8/8b/Kingsman_The_Secret_Service_poster.jpg",
#                        "https://www.youtube.com/watch?v=kl8F-8tR8to")
#
# mad_max = media.Movie("Mad Max - Fury Road",
#                       "Mad Max travels along the furious road",
#                       "http://upload.wikimedia.org/wikipedia/en/2/23/Max_Mad_Fury_Road_Newest_Poster.jpg",
#                       "https://www.youtube.com/watch?v=hEJnMQG9ev8")
