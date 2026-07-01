Vercel deployment guide

Repository structure recommended for Vercel:

- app.py                    # Main Flask application
- api/index.py              # Vercel serverless entrypoint (exposes `app`)
- requirements.txt          # Dependency list
- .python-version           # Python runtime pin (e.g., 3.11)
- vercel.json               # Optional: explicit build/install config
- model.py                  # DB helpers (has SQLite fallback)
- Frontend/                 # static templates, CSS, JS

How Vercel resolves this project
- If `api/` contains Python files, Vercel treats them as Serverless Functions.
  `api/index.py` must export a WSGI callable named `app` (Flask app works).
- `requirements.txt` is used to install dependencies.
- `.python-version` pins the Python runtime.

Recommended deployment steps
1. Ensure `requirements.txt` contains all dependencies.
2. Set environment variables in Vercel Dashboard (if using TiDB):
   - `TIDB_HOST`, `TIDB_PORT`, `TIDB_USER`, `TIDB_PASSWORD`, `TIDB_DB`, `TIDB_SSL_CA`.
3. Push to GitHub (already on `main`). Vercel will auto-deploy.

Local testing
- Run locally with Python:
```bash
python -m pip install -r requirements.txt
python app.py
```
- Or use Vercel CLI to test functions locally:
```bash
vercel dev
```

Notes
- I added `model.py` fallback to SQLite so the app won't crash without DB env vars.
- Keep only `requirements.txt` (remove any misspelled duplicates).
- If you prefer to control builds from Dashboard, remove `builds` from `vercel.json`.
