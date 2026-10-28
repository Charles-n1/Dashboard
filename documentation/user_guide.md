# User Guide

## Start the dashboard

Run the project with Docker Compose:

```bash
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173) in a browser.

## Create an account

1. Select **Créer un compte** on the authentication screen.
2. Enter a username, valid email address, password, and optional first and last names.
3. Submit the form.
4. Return to the login form and sign in.

Passwords must contain at least eight characters. Usernames and email addresses must be unique.

## Sign in

Enter the email and password used during registration. The session is stored in the browser as a JWT access token. If the token expires or becomes invalid, the application returns to the authentication screen.

## Use the dashboard

Open the menu button to display services and available widgets. Drag a widget from the menu into an empty dashboard cell. Widgets already on the dashboard can be moved by dragging them to another cell.

Use the delete button on a widget to remove it from the grid. The layout is saved locally in the browser and is restored when the dashboard is reopened on the same browser.

## Widget settings

Widget inputs are applied when you press **Enter**:

- Discord profile: avatar size.
- Discord banner: banner width.
- Weather: city name.
- All widgets: refresh interval in seconds.

The weather widget defaults to Lyon and uses Open-Meteo for geocoding and the current temperature.

## Connect services

The services menu contains Discord and Steam connection actions.

Discord starts an OAuth flow. The backend exchanges the authorization code, stores the Discord profile, links it to the current user, and redirects to the frontend after success.

Steam currently displays an OpenID login link, but the backend Steam routes and data widgets are not complete.

## Troubleshooting

- If the page does not load, check that the frontend is running on port `5173` and the backend is running on port `8080`.
- If login fails immediately after startup, check the backend database connection and the `SECRET_KEY` and `ACCESS_TOKEN_EXPIRE_MINUTES` environment variables.
- If Discord login fails, verify the Discord client ID, client secret, and callback URL. The callback URL must match the Discord application configuration.
- If an account is suspended, only an administrator can change its `status` through the backend API.

The current frontend still has incomplete Steam widgets and known Discord/weather client integration mismatches. See [frontend.md](frontend.md) for implementation details.
