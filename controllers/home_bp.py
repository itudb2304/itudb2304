from flask import Blueprint, render_template, request, redirect, url_for

def home_bp():
    home = Blueprint(
        "home",
        __name__,
        template_folder="templates",
        static_folder="static/",
        url_prefix="/",
    )

    @home.route("/")
    def home_page():
        return render_template("home.html")
    
    return home