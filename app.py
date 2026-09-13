#!/usr/bin/env python3
"""
Production entry point for Chess Game Application
"""

import os

from chess_app import app

# Ensure Flask secret key works in production
app.secret_key = os.environ.get("SECRET_KEY", app.secret_key)

# Gunicorn imports this module and looks for `application`
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
