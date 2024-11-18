from app import create_app

# Initialize the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the app on localhost
    app.run(debug=True, host="127.0.0.1", port=5000)
