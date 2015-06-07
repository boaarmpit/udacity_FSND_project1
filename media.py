__author__ = 'bryn'
import webbrowser

class Movie():
    """"Movie object: Contains the following basic information about the movie (all strings):
    movie_title:        The title of the movie
    movie_storyline;    A summary of the storyline of the movie
    poster_image;       The URL of an image of the poster
    trailer_youtube;    The URL of the trailer on youtube"""
    def __init__(self, movie_title, movie_storyline, poster_image, trailer_youtube):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    #  Test functions to display the poster and the trailer (no longer used)
    # def show_poster(self):
    #     webbrowser.open(self.poster_image_url)
    #
    # def show_trailer(self):
    #     webbrowser.open(self.trailer_youtube_url)