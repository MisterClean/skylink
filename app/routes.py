from flask import Blueprint, render_template, request, redirect, url_for
from .feed_manager import BlueskyFeedManager

# Define the main Blueprint
main = Blueprint("main", __name__)

# Create an instance of BlueskyFeedManager
feed_manager = BlueskyFeedManager()

@main.route("/")
def home():
    """Render the home page."""
    feeds = feed_manager.list_feeds()
    return render_template("home.html", feeds=feeds)

@main.route("/login", methods=["POST"])
def login():
    """Handle login requests."""
    username = request.form["username"]
    app_password = request.form["app_password"]
    if feed_manager.login(username, app_password):
        return redirect(url_for("main.home"))
    return "Login failed. Please try again."

@main.route("/create_feed", methods=["POST"])
def create_feed():
    """Handle creating a new feed."""
    feed_name = request.form["feed_name"]
    starter_packs = request.form["starter_packs"].split(",")
    feed_manager.create_feed(feed_name, starter_packs)
    return redirect(url_for("main.home"))

@main.route("/save_feeds")
def save_feeds():
    """Save feeds to a file."""
    feed_manager.save_feeds()
    return redirect(url_for("main.home"))

@main.route("/load_feeds")
def load_feeds():
    """Load feeds from a file."""
    feed_manager.load_feeds()
    return redirect(url_for("main.home"))
