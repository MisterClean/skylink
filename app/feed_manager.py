import os
import json
import requests

class BlueskyFeedManager:
    """Handles Bluesky feed management."""

    def __init__(self):
        self.username = None
        self.app_password = None
        self.session = requests.Session()
        self.token = None
        self.feeds = {}

    def login(self, username, app_password):
        """Authenticate with Bluesky and store the access token."""
        self.username = username
        self.app_password = app_password
        try:
            response = self.session.post(
                "https://bsky.social/xrpc/com.atproto.server.createSession",
                json={"identifier": self.username, "password": self.app_password},
            )
            response.raise_for_status()
            self.token = response.json().get("accessJwt")
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            return True
        except requests.HTTPError as e:
            print(f"Login failed: {e}")
            return False

    def create_feed(self, feed_name, starter_packs):
        """Create a feed from one or more starter packs."""
        all_users = set()
        for pack in starter_packs:
            try:
                response = self.session.get(f"https://bsky.social/xrpc/starterpacks/{pack}")
                response.raise_for_status()
                all_users.update(response.json().get("users", []))
            except requests.HTTPError:
                continue
        self.feeds[feed_name] = {"starter_packs": starter_packs, "users": list(all_users)}

    def list_feeds(self):
        """Return all feeds with their details."""
        return self.feeds

    def save_feeds(self):
        """Save feed data to a JSON file."""
        with open("feeds.json", "w") as f:
            json.dump(self.feeds, f, indent=4)

    def load_feeds(self):
        """Load feed data from a JSON file."""
        if os.path.exists("feeds.json"):
            with open("feeds.json", "r") as f:
                self.feeds = json.load(f)
