from app import app

# Vercel Python serverless expects a WSGI `app` callable exported at module-level.
# This file maps the root Flask app so Vercel can run it as a serverless function.

# Expose the WSGI application as `app` (already imported above).

# Optionally, you can add middleware or wrappers here.
