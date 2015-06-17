import webbrowser
import os
import re
import codecs

# Styles and scripting for the page
main_page_head = u'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Movies</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/bootstrap-theme.css">
    <link rel="stylesheet" href="css/sticky-footer.css">
    <script src="js/jquery-1.10.1.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
    body {
        padding-top: 80px;
        background: #000;
        }
        #trailer .modal-dialog {
        margin-top: 100px;
        }
        .hanging-close {
        position: absolute;
        top: -12px;
        right: -12px;
        z-index: 9001;
        }
        #trailer-video {
        width: 100%;
        height: 100%;
        }
        .movie-tile {
        //max-height:270px;
        }
        .movie-tile:hover {
        background-color: #FFF;
        cursor: pointer;
        }
        .poster-image {
        max-height:100%;
        max-width:100%;
        }
        .poster-image:hover {
        opacity:0.7;
        }
        .scale-media {
        padding-bottom: 56.25%;
        position: relative;
        }
        .scale-media iframe {
        border: none;
        height: 100%;
        position: absolute;
        width: 100%;
        left: 0;
        top: 0;
        background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1&iv_load_policy=3';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show(50, showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = u'''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="images/close_window_X.png"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Favourite Movies</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
    <footer class="footer navbar-inverse">
        <div class="container text-center">
            <p class="text-muted">All images are copyright to their respective owners.</p>
        </div>
    </footer>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = u'''
<div class="col-xs-12 col-sm-4 col-md-3 col-lg-2 movie-tile" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img class="poster-image img-responsive" src="{poster_image_url}" alt="{movie_title}" title="{movie_title}: {movie_storyline}">
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = u''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+',
                                     movie.trailer_youtube_url)
        youtube_id_match = \
            youtube_id_match or re.search(r'(?<=be/)[^&#]+',
                                          movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) \
            if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            poster_image_url=movie.poster_image_url,
            movie_title=movie.title.replace('"', '&#34'),
            movie_storyline=movie.storyline.replace('"', '&#34'),
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = codecs.open('static/index.html', 'w', encoding='utf-8')

    # Replace the placeholder for the movie tiles with
    # the actual dynamically generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)  # open in a new tab, if possible
