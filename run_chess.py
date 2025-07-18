#!/usr/bin/env python3
"""
Chess Game Launcher
Simple script to run the chess game with setup instructions
"""

import os
import subprocess
import sys


def check_flask():
    """Check if Flask is installed"""
    try:
        import flask

        print(f"✅ Flask {flask.__version__} is installed")
        return True
    except ImportError:
        print("❌ Flask is not installed")
        return False


def install_flask():
    """Install Flask if not present"""
    print("Installing Flask...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask>=2.3.0"])
        print("✅ Flask installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Flask")
        return False


def main():
    """Main launcher function"""
    print("♔ Chess Game Launcher ♛")
    print("=" * 40)

    # Check if Flask is installed
    if not check_flask():
        print("\nFlask is required to run the chess game.")
        response = input("Would you like to install Flask now? (y/n): ")
        if response.lower() in ["y", "yes"]:
            if not install_flask():
                print("Please install Flask manually: pip install flask")
                return
        else:
            print("Please install Flask manually: pip install flask")
            return

    print("\n🚀 Starting Chess Game...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)

    # Run the chess app
    try:
        from chess_app import app

        app.run(debug=True, host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print("\n👋 Chess game stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting chess game: {e}")


if __name__ == "__main__":
    main()
