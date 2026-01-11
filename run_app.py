import uvicorn
import webbrowser
import threading
import time
import os
import sys

# Ensure we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def main():
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait a moment for server to initialize
    time.sleep(1.5)

    # Open the browser to the local server
    print("Launching AirtimeX in your browser...")
    webbrowser.open("http://127.0.0.1:8000")

    # Keep the main thread alive nicely
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down AirtimeX...")

if __name__ == "__main__":
    main()
