"""
Main entry point for the Python project.
"""

from app import app
import sys
import os
import webbrowser
import time

# Add src directory to Python path BEFORE importing app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    """Main function that runs the web application."""
    print("Starting web application...")
    print("Opening browser to http://localhost:5000")

    # Give Flask a moment to start before opening browser
    def open_browser():
        time.sleep(1)
        webbrowser.open('http://localhost:5000')

    import threading
    thread = threading.Thread(target=open_browser)
    thread.daemon = True
    thread.start()

    # Run Flask app
    app.run(debug=True, port=5000, use_reloader=False)


if __name__ == "__main__":
    main()
