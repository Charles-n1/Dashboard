# Backend API

The backend is a FastAPI application served by Uvicorn.

- Local base URL: `http://localhost:8080`
- Interactive OpenAPI documentation: `http://localhost:8080/docs`
- OpenAPI JSON: `http://localhost:8080/openapi.json`
- Frontend requests normally use the Vite `/api` proxy.

## Authentication

User login returns a JWT access token. Send it on protected requests with:

```http
Authorization: Bearer <access_token>
```

Tokens contain the user ID and expire after `ACCESS_TOKEN_EXPIRE_MINUTES`. Accounts whose `status` is not `active` cannot authenticate. Admin routes additionally require `is_admin: true`.

## General endpoints

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| `GET` | `/` | None | Returns the API status page. |
| `GET` | `/about.json` | None | Returns client information, server time, and the service/widget description structure. |
| `GET` | `/auth` or `/auth/details` | None | Returns the authentication/services information page. |
| `GET` | `/openapi.json` | None | Returns the generated OpenAPI document. |
| `GET` | `/auth/discord` | None | Reports whether the Discord backend integration is implemented. |
| `GET` | `/auth/steam` | None | Reports whether the Steam backend integration is implemented. |
| `GET` | `/auth/weather` | None | Reports whether the Weather backend integration is implemented. |

HTTP 404 responses are rendered as the backend's HTML 404 page. Other handled HTTP errors use `{ "detail": "..." }`.

## Users

### Public

`POST /users` creates a user. Required fields are `username`, `email`, and a password of at least eight characters. `first_name` and `last_name` are optional.

`POST /users/login` accepts `{ "email": "...", "password": "..." }` and returns:

```json
{
	"access_token": "<jwt>",
	"token_type": "bearer"
}
```

Duplicate usernames or emails return `409 Conflict`. Invalid credentials return `401 Unauthorized`.

### Authenticated

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/users/me` | Returns the current user. |
| `PATCH` | `/users/me` | Updates the current user's username, email, password, first name, or last name. |

### Admin-only

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/users` | Lists all users. |
| `GET` | `/users/{user_id}` | Gets one user. |
| `PATCH` | `/users/{user_id}` | Updates user profile, `status`, or `is_admin`. |
| `DELETE` | `/users/{user_id}` | Deletes a user. Returns `204 No Content`. |

Password hashes are never included in `UserRead` responses.

## Discord

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| `GET` | `/auth/discord` | None | Returns `{ "service": "discord", "status": "implemented" }`. |
| `GET` | `/auth/discord/login` | Optional | Starts Discord OAuth. Pass the application JWT as `?token=...` to link Discord to the logged-in user. |
| `GET` | `/auth/discord/callback` | OAuth state | Exchanges the Discord code, stores the profile, links it to the user, and redirects to the frontend. |
| `GET` | `/discord` | User | Lists Discord records. |
| `GET` | `/discord/me` | User | Returns the Discord record linked to the current user. |
| `GET` | `/discord/{primary_id}` | User | Gets a Discord record. |
| `GET` | `/discord/{primary_id}/exists` | User | Returns `{ "exists": true/false }`. |
| `POST` | `/discord` | Admin | Creates a Discord record. |
| `PATCH` | `/discord/{primary_id}` | Admin | Updates a Discord record. |
| `DELETE` | `/discord/{primary_id}` | Admin | Deletes a Discord record. Returns `204 No Content`. |

Discord OAuth state tokens are separate from login tokens and expire after ten minutes. The callback requires a valid state token, so a callback without a logged-in linking flow is rejected.

The service status routes report backend implementation status, not whether an individual user's provider account is linked. `/discord/me` checks a user's Discord account link.

## Example

```bash
curl -X POST http://localhost:8080/users/login \
	-H 'Content-Type: application/json' \
	-d '{"email":"user@example.com","password":"password123"}'

curl http://localhost:8080/users/me \
	-H 'Authorization: Bearer <access_token>'
```

## Current implementation status

Steam and Weather status routes return HTTP 200 with `"status": "not implemented"`; Discord returns `"status": "implemented"`. The frontend uses these status routes to distinguish a reachable backend from an implemented provider integration. Weather forecast and air-quality data routes are registered and proxy requests to Open-Meteo; city geocoding is performed directly by the frontend.

The backend smoke test in `code/backend/scripts/test_backend.py` covers the root, auth, user, Discord, Steam status, and Weather status routes.
