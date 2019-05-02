import time

from flask import Blueprint, render_template, request, redirect, url_for

from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from . import database
from . import models

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@bp.route("/login", methods=["POST"])
def login_try():
    username = request.form.get("username", None)
    pw = request.form.get("password", None)
    if username is not None and pw is not None:
        users = database.get_db().query(models.User).filter_by(username=username)

        for user in users:
            if check_password_hash(user.password, pw):
                login_user(user, remember=True)
                return redirect(url_for("table.index"))

    time.sleep(5)

    return login()


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("table.index"))
