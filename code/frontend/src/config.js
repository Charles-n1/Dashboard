const API_URL = import.meta.env.VITE_API_URL || '/api'

export const DISCORD_URLS = {
    login: `${API_URL}/auth/discord/login`,
    profile: `${API_URL}/discord/me`,
    avatar: 'https://cdn.discordapp.com/avatars',
    defaultAvatar: 'https://cdn.discordapp.com/embed/avatars',
    banner: 'https://cdn.discordapp.com/banners',
}

export const STEAM_URLS = {
    login: `${API_URL}/auth/steam/login`,
    profile: `${API_URL}/steam/me`,
    currentGame: `${API_URL}/steam/current-game`,
    lastGame: `${API_URL}/steam/last-game`,
    icon: 'https://media.steampowered.com/steamcommunity/public/images/apps',
}

export const BACKEND_URLS = {
    register: `${API_URL}/users`, // TODO Modifier les liens renvoyer vers l'api Wunderbar
    login: `${API_URL}/users/login`, // TODO Modifier les liens renvoyer vers l'api Wunderbar
    me: `${API_URL}/users/me`, // TODO Modifier les liens renvoyer vers l'api Wunderbar
}

export const SERVICE_STATUS_URLS = {
    discord: `${API_URL}/auth/discord`,
    steam: `${API_URL}/auth/steam`,
    weather: `${API_URL}/auth/weather`,
}

export const GRID = {
    columns: 13,
    rows: 6,
}

export const GRID_URLS = {
    current: `${API_URL}/grid/me`,
}

export const METEO_URLS = {
    city_location: 'https://geocoding-api.open-meteo.com/v1/search',
    weather: `${API_URL}/weather`,
    forecast: `${API_URL}/weather/forecast`,
    air_quality: `${API_URL}/weather/air-quality`
}

export const DISCORD_CLIENT_ID = import.meta.env.VITE_DISCORD_CLIENT_ID 
