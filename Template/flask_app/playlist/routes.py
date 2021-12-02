from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_app import playlist
from flask_login import current_user

<<<<<<< HEAD
from .. import deezer_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time

songs = Blueprint("songs", __name__)
=======
from .. import movie_client
from ..forms import MovieReviewForm, SearchForm, FavoritePlaylistForm
from ..models import Playlist, User, Review
from ..utils import current_time

import io
import base64

movies = Blueprint("movies", __name__)
>>>>>>> ac7eff266afe93e162468b68417ceb01fb54dc0a

@songs.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("songs.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@songs.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = deezer_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("songs.index"))

    return render_template("query.html", results=results)

#Displays playlist and gives user option to favorite
@playlist.route("/playlist/<playlist_id>", methods=["GET", "POST"])
def movie_detail(playlist_id):
    try:
<<<<<<< HEAD
        result = deezer_client.retrieve_movie_by_id(playlist_id)
=======
        playlist = Playlist.objects(id=playlist_id).first()
>>>>>>> ac7eff266afe93e162468b68417ceb01fb54dc0a
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("playlist.index"))

    img = get_b64_img(playlist)

    form = FavoritePlaylistForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        user = current_user._get_current_object()
        user.favorites.append(playlist)
        user.save()
        return redirect(request.path)
        
    return render_template("movie_detail.html", playlist=playlist, image=img, form=form)

#Edit Playlist Add/Remove Songs, edit playlist title,bio, and picture
@playlist.route("/editplaylist/<playlist_id>", methods=["GET", "POST"])
def edit_playlist(playlist_id):
    try:
        playlist = Playlist.objects(id=playlist_id).first()
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("playlist.index"))

    form = MovieReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )


def get_b64_img(playlist):
    bytes_im = io.BytesIO(playlist.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image