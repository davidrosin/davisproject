# FastAPI + Auth0 OAuth2 Protected API

This is a simple FastAPI application protected with Auth0 using OAuth2.

## 🛠 Setup

1. Create a `.env` file based on `.env.example`.
2. Run locally with:
   ```bash
   uvicorn main:app --reload
   ```

3. Deploy to Render:
   - Use the start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - Add your `.env` variables in the dashboard.
