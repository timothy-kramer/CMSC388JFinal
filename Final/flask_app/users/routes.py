from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User, Review


users = Blueprint("users", __name__)


""" ************ User Management views ************ """
#loggedin = False
#current_user = None


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("movies.index")) 

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        new_user.save()
        login_user(new_user)

        return redirect(url_for("movies.index"))

    return render_template("register.html", form=form)

# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("movies.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first() 

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and password.", "danger")

    return render_template("login.html", form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("movies.index"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()

    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            current_user.modify(username=update_username_form.username.data)
            current_user.save()
            login_user(current_user)
            flash("Username updated successfully!", "success")
            return redirect(url_for("users.account"))  

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            picture = update_profile_pic_form.picture.data
            if picture:
                filename = secure_filename(picture.filename)
                
                current_user.profile_pic.replace(picture, filename=filename)
                current_user.save()

                flash("Profile picture updated successfully!", "success")
                return redirect(url_for("users.account"))


    image_data = None
    if current_user.profile_pic:
        image_binary = current_user.profile_pic.read() 
        if image_binary:  
            image_data = base64.b64encode(image_binary).decode("utf-8")

    return render_template(
        "account.html",
        update_username_form=update_username_form,
        update_profile_pic_form=update_profile_pic_form,
        image=image_data,
    )
    # TODO: handle get requests  


@users.route("/user/<username>")
@login_required 
def user_detail(username):
    user = User.objects(username=username).first()
    
    if not user:
        return render_template("user_detail.html", error="User not found", reviews=None)

    reviews = Review.objects(commenter=user)

    image_data = None
    if user.profile_pic:
        image_binary = user.profile_pic.read() 
        image_data = base64.b64encode(image_binary).decode("utf-8")

    return render_template("user_detail.html", user=user, reviews=reviews, image=image_data)