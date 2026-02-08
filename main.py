# main.py
from app import create_app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Local debug run (optional)
    # On Render, this line is ignored because gunicorn will serve the app
    app.run(debug=True)
