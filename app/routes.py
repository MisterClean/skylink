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
    # Ensure `login_status` is always available
    login_status = feed_manager.login_status if hasattr(feed_manager, 'login_status') else {"success": False, "message": ""}
    return render_template("home.html", feeds=feeds, login_status=login_status)

@main.route("/login", methods=["POST"])
def login():
    """Handle login requests."""
    username = request.form["username"]
    app_password = request.form["app_password"]
    if feed_manager.login(username, app_password):
        return redirect(url_for("main.home"))
    return redirect(url_for("main.home"))

@main.route("/create_feed", methods=["POST"])
def create_feed():
    """Create a new feed from starter packs."""
    feed_name = request.form["feed_name"]
    starter_pack_uri = request.form["starter_pack_uri"]  # A single starter pack URI is expected

    success = feed_manager.process_starter_pack(feed_name, starter_pack_uri)
    if success:
        return f"Feed '{feed_name}' created successfully!", 200
    else:
        return f"Failed to create feed '{feed_name}'.", 500

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
