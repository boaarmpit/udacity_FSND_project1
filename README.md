## Synopsis

This application creates an HTML summary of a list of movies, including the posters and links to the trailers. Given a list of movie titles, it downloads the relevant information and poster images using the omdb and YouTube APIs and outputs a static HTML page.

See an [example output](http://boaarmpit.github.io/static/index.html).

This is also Project 1 of the [Udacity Full Stack Nano Degree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Motivation

This project was started to meet the requirements of the Udacity Full Stack Nano Degree, and was extended to be a tool to easily show lists of movie recommendations to my friends.

## Installation
This script is designed for python 2.7.6 and requires the following library aside from the Python Standard Libraries:  
*httplib2*

Also, a (free) Google API key with the YouTube API enabled is required to search for the movie trailers on YouTube.  
Replace `PLACEHOLDER GOOGLE API KEY` in *entertainment_center.py* with your Google API key.


## Usage

Run *fresh_tomatoes.py* as it is (after entering your Google API key) to display an example output.
Edit the following line if your favourite movies differ from the ones displayed.  
`favorite_movies = ["Attack the Block","Borat", "Total Recall", "Kingsman", ...]`

## References
This script includes example code from Udacity Full Stack Nano Degree *Programming Foundations with Python* course and css/javascript code from [bootstrap](http://getbootstrap.com/) and [jquery](https://jquery.com/).  Movie poster images in the *static/images* folder were acquired using the [omdb api](omdbapi.com) and belong to the respective copyright holders.

