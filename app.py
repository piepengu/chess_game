#!/usr/bin/env python3
"""
Production entry point for Chess Game Application
"""

import os

from chess_app import app

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
else:
    # For production (gunicorn will import this)
    application = app
