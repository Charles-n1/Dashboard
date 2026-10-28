# Frontend

The frontend is a React 19 application built and served by Vite.

## Application flow

`src/App.jsx` checks `localStorage.access_token` on startup by calling `/users/me`.

- No token, an invalid token, or an unavailable backend shows the login/register view.
- A valid token shows the dashboard.
- Login stores the access token and switches to the dashboard.

The dashboard is composed of a header, a collapsible services menu, a profile panel, and a configurable widget grid.

## Pages and components

- `pages/login.jsx`: email/password login.
- `pages/register.jsx`: account creation.
- `pages/dashboard.jsx`: widget grid, drag and drop, deletion, refresh timers, and persistence.
- `components/header.jsx`: menu and profile panel toggles.
- `components/services_panel.jsx`: service connection controls, backend status checks, and draggable widget catalogue.
- `components/profile_panel.jsx`: static profile panel currently displayed by the UI.

## Widgets

The grid currently registers these widget names:

| Widget | Intended data | Local settings |
| --- | --- | --- |
| `discord_profile` | Linked Discord avatar and display name | `avatar_size_<cell>` and refresh interval |
| `discord_banner` | Linked Discord banner | `banner_width_<cell>` and refresh interval |
| `steam_profile` | Steam profile | Placeholder UI |
| `steam_currentgame` | Current Steam game | Placeholder UI |
| `steam_lastgame` | Last Steam game | Placeholder UI |
| `meteo` | Current temperature for a city | `city_<cell>` and refresh interval |

Widgets can be dragged from the services menu into the grid or moved between cells. The grid layout is stored as `localStorage.cells`. Empty cells are represented by empty objects in the current implementation. Widget refresh values default to 30 seconds and are stored as `refresh_<cell>`.

## Configuration

`src/config.js` reads:

- `VITE_API_URL`, defaulting to `/api`.
- `VITE_DISCORD_CLIENT_ID`, currently defined for frontend configuration.

Vite proxies `/api` to the backend. Discord profile data is requested from `/discord/me` with the application JWT.

The services panel checks `/auth/discord`, `/auth/steam`, and `/auth/weather` on load. These unauthenticated GETs report whether the backend endpoint is reachable and whether its provider integration is implemented; they do not indicate whether a user's provider account is linked. Discord's linked-account status is checked separately through `/discord/me`.

## Current limitations

- Steam provider integration is not implemented; its backend status endpoint reports this and Steam widgets remain placeholders.
- The Discord banner widget references a banner URL configuration that is not currently defined in `config.js`.
- The Discord widgets read a `badge` local-storage value, while authentication currently stores `access_token`; connecting the service therefore needs this client-side token handling aligned.
- Weather city geocoding is fetched directly from Open-Meteo. Forecast and air-quality requests go through the backend `/weather` endpoints, which proxy Open-Meteo.
- The header and profile panel currently display static profile content rather than the logged-in user's data.
