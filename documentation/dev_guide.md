# Developer Guide

## Requirements

- Docker and Docker Compose
- A recent browser
- Node.js 22 and npm if running the frontend outside Docker
- Python 3.12 if running the backend outside Docker

## Configuration

Create a `.env` file at the repository root. Docker Compose expects:

```dotenv
POSTGRES_USER=dashing
POSTGRES_PASSWORD=change-me
POSTGRES_DB=dashboard
SECRET_KEY=replace-with-a-long-random-value
ACCESS_TOKEN_EXPIRE_MINUTES=60
DISCORD_CLIENT_ID=your-discord-client-id
DISCORD_CLIENT_SECRET=your-discord-client-secret
BACKEND_URL=http://localhost:8080
FRONTEND_URL=http://localhost:5173
DISCORD_REDIRECT_URI=http://localhost:8080/auth/discord/callback
```

`DATABASE_URL` is assembled automatically for the backend container. Keep secrets out of source control.

## Run with Docker Compose

From the repository root:

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8080`
- PostgreSQL: `localhost:5432`

### Access from another computer

To access the frontend from another computer on the same network, find the host
machine's LAN address with `ip -4 addr` (for example, `192.168.0.36`). Set the
public-facing URLs in the root `.env` to that address:

```dotenv
BACKEND_URL=http://192.168.0.36:8080
FRONTEND_URL=http://192.168.0.36:5173
DISCORD_REDIRECT_URI=http://192.168.0.36:8080/auth/discord/callback
```

Add the exact `DISCORD_REDIRECT_URI` value to the OAuth2 redirect URLs in the
Discord Developer Portal. After changing `.env`, recreate the containers:

```bash
docker compose up --build -d
```

Then open the frontend on the other computer:

```text
http://<host-lan-ip>:5173
```

Allow the frontend port and the backend callback port through UFW on the host:

```bash
sudo ufw allow 5173/tcp
sudo ufw allow 8080/tcp
```

When remote access is no longer needed, remove the rule:

```bash
sudo ufw delete allow 5173/tcp
sudo ufw delete allow 8080/tcp
```

The frontend proxies `/api/*` to the backend and removes the `/api` prefix, so
normal API traffic stays within the host and Docker network. `BACKEND_URL` is
used for external OAuth callbacks (Discord and Steam); `FRONTEND_URL` is where
those callbacks send the browser afterward. Outside Docker, the Vite proxy
target defaults to `http://localhost:8080`; Compose sets it to
`http://backend:8080`.

Stop the stack with:

```bash
docker compose down
```

Use `docker compose down -v` only when the persistent PostgreSQL volume should also be deleted.

## Run services directly

Backend:

```bash
cd code/backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$PWD"
uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload
```

Frontend:

```bash
cd code/frontend
npm ci
npm run dev -- --host 0.0.0.0
```

Useful frontend commands are `npm run build`, `npm run lint`, and `npm run preview`.

## Backend smoke tests

Start the backend and database first, then run:

```bash
code/backend/scripts/run_backend_tests.sh --base-url http://localhost:8080 --verbose
```

The test creates temporary user and Discord records, checks authentication and CRUD behavior, then removes the records. Use `--keep-data` to preserve generated records while debugging.

## Project layout

```text
code/backend/app/       FastAPI app, routes, services, schemas, database access
code/backend/scripts/   Backend smoke test runner
code/frontend/src/      React app, pages, services, widgets, and styles
code/database/          PostgreSQL schema dumps
documentation/          Project documentation
```

## Adding an API resource

Follow the existing pattern:

1. Add the SQLAlchemy model in `code/backend/app/database.py`.
2. Add Pydantic request/response schemas.
3. Put database operations in a service module.
4. Add an `APIRouter` and include it in `code/backend/app/app.py`.
5. Protect routes with `get_current_user` or `get_current_admin` where needed.
6. Extend the smoke test and this API document.

## Adding a widget

1. Create the widget component and its stylesheet in the matching directory under `code/frontend/src/widgets/` (for example, `discord/`, `steam/`, or `weather/`). Accept the cell `index` and refresh props when the widget needs per-cell settings or periodic refresh. Use `src/settings.js` to load and save settings in local storage.
2. Register the component in both `SERVICE_WIDGETS` in `src/components/widgets_panel.jsx` and `WIDGETS` in `src/components/cell.jsx`. The first registration displays it in the service catalogue; the second renders it in the dashboard.
3. Add its name to `WIDGET_NAMES` in `src/pages/dashboard.jsx`. This list validates widgets when they are added, moved, or deleted.
4. Add service-specific settings or controls to the widget panel if needed. Keep the widget name, service key, and component registrations consistent.
5. Verify adding, moving, resizing, refreshing, and deleting the widget. Run `npm run lint` and `npm run build` from `code/frontend`; update the user guide and this documentation when behavior changes.

## Adding a service

1. Create a service directory under `code/frontend/src/services/` and implement its connection component and styles. Follow the existing Discord or Steam component pattern for connection state and controls.
2. Add the service to `ServicesPanel` in `src/components/services_panel.jsx`. Provide its display name, connection state, details, and authentication control. The service key is derived from the lowercase display name and must match the key used by `SERVICE_WIDGETS` in `src/components/widgets_panel.jsx`.
3. Add the service's widgets following the widget steps above. Add configuration values or API URLs in `src/config.js` rather than embedding shared endpoints in components.
4. If the service requires backend integration, add its model, schemas, service, and router following the existing backend resource pattern. Register the router in `code/backend/app/app.py`, protect user-specific routes, and extend the backend smoke test and `documentation/backend_api.md`.
5. Document required environment variables, OAuth callback configuration, and any external API limits. Keep credentials in the root `.env` file, never in frontend source code.

## Technical decision template

Use this blank template for each implementation choice. Keep the entry descriptive and record constraints and alternatives without presenting them as arguments.

```text
### [Decision title]

- Date:
- Context / feature:
- Current choice:
- Purpose:
- Constraints (budget, time, technical, or other):
- Alternatives considered:
- Reason for the current choice:
- Consequences and limitations:
- Conditions for reconsidering the choice:
- References:
```

Create one entry for each choice to document, for example the 30-second default refresh interval, the selected API, or the storage location for dashboard settings. Fill in the values based on the project's actual decisions and constraints.
