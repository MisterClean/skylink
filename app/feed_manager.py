import requests

class BlueskyFeedManager:
    def __init__(self):
        """Initialize the BlueskyFeedManager with required attributes."""
        self.username = None
        self.app_password = None
        self.session = requests.Session()
        self.token = None
        self.login_status = {"success": False, "message": ""}  # For tracking login status
        self.feeds = {}  # Initialize feeds as an empty dictionary

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

            # Save the token and update login status
            self.token = response.json().get("accessJwt")
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            self.login_status = {"success": True, "message": "Successfully logged in!"}
            return True
        except requests.HTTPError as e:
            self.login_status = {
                "success": False,
                "message": f"Login failed: {e.response.status_code} {e.response.text}",
            }
            return False

    def get_starter_pack_users(self, starter_pack_uri):
        """Fetch users from a starter pack URI with pagination."""
        all_users = []
        cursor = None  # Cursor for pagination

        try:
            while True:
                # Prepare request parameters for pagination
                params = {"cursor": cursor} if cursor else {}
                response = self.session.get(f"{starter_pack_uri}", params=params)
                response.raise_for_status()  # Raise error for HTTP issues

                data = response.json()
                users = data.get("users", [])
                all_users.extend(users)  # Add users to the list

                # Check if there's a cursor for the next page
                cursor = data.get("cursor")
                if not cursor:
                    break  # No more pages

            return all_users

        except requests.HTTPError as e:
            print(f"Failed to fetch users from starter pack: {e}")
            return []

    def create_feed_on_bluesky(self, feed_name, users):
        """Create a feed on Bluesky with the given user list."""
        try:
            response = self.session.post(
                "https://bsky.social/xrpc/com.atproto.feed.createFeed",  # Replace with actual endpoint
                json={
                    "name": feed_name,
                    "users": users,
                },
            )
            response.raise_for_status()
            print(f"Feed '{feed_name}' successfully created on Bluesky!")
            return True
        except requests.HTTPError as e:
            print(f"Failed to create feed on Bluesky: {e.response.status_code} {e.response.text}")
            return False

    def process_starter_pack(self, feed_name, starter_pack_uri):
        """Fetch users from a starter pack and create a feed on Bluesky."""
        print(f"Fetching users from starter pack: {starter_pack_uri}")
        users = self.get_starter_pack_users(starter_pack_uri)

        if users:
            print(f"Fetched {len(users)} users from starter pack.")
            success = self.create_feed_on_bluesky(feed_name, users)
            return success
        else:
            print("No users found in the starter pack.")
            return False

    def list_feeds(self):
        """Return the current feeds stored in the manager."""
        return self.feeds
