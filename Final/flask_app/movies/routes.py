import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user


from .. import movie_client
from ..forms import MovieReviewForm, SearchForm, WatchlistForm
from ..models import User, Review, Watchlist
from ..utils import current_time

movies = Blueprint("movies", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@movies.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("movies.query_results", query=form.search_query.data))

    watchlist_movies = []
    if current_user.is_authenticated:
        watchlist_movies = Watchlist.objects(user=current_user._get_current_object()).order_by("-priority")[:3]
    return render_template("index.html", form=form, watchlist_movies=watchlist_movies)


@movies.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@movies.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    watchlist_form = WatchlistForm()

    # Check if movie is already in the watchlist
    movie_in_watchlist = False
    if current_user.is_authenticated:
        existing = Watchlist.objects(user=current_user._get_current_object(), imdb_id=movie_id).first()
        movie_in_watchlist = bool(existing)

    if watchlist_form.validate_on_submit() and current_user.is_authenticated and not movie_in_watchlist:
        watchlist_entry = Watchlist(
            user=current_user._get_current_object(),
            imdb_id=movie_id,
            movie_title=result.title,
            priority=watchlist_form.priority.data,
            date_added=current_time()
        )
        watchlist_entry.save()
        flash("Movie added to watchlist!", "success")
        return redirect(request.path)

    if not current_user.is_authenticated and watchlist_form.validate_on_submit():
        flash("Please log in to add to your watchlist.", "warning")
        return redirect(url_for("users.login"))

    if form.validate_on_submit():
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
    reviews_with_images = []
    for review in reviews:
        image_data = get_b64_img(review.commenter.username)
        reviews_with_images.append({
            'review': review,
            'image_data': image_data
        })

    return render_template("movie_detail.html",form=form,watchlist_form=watchlist_form,movie=result,reviews=reviews_with_images,movie_in_watchlist=movie_in_watchlist)

@movies.route("/user/<username>")
def user_detail(username):
    #uncomment to get review image
    #user = find first match in db
    #img = get_b64_img(user.username) use their username for helper function
    return "user_detail"

@movies.route("/watchlist", methods=["GET"])
@login_required
def watchlist():
    watchlist_movies = Watchlist.objects(user=current_user._get_current_object()).order_by("-priority")
    return render_template("watchlist.html", watchlist_movies=watchlist_movies)

