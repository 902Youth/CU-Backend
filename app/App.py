from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def welcome():
    return "Welcome to the API!"

# Run the Flask application
if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) and port 3000
    app.run(host='127.0.0.1', port=3000)
