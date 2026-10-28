

WUNDERBAR_DASHBOARD_API_TITLE = "Wunderbar Dashboard API"
WUNDERBAR_DASHBOARD_API_DESCRIPTION = "API for Wunderbar Dashboard"

ALGORITHM="HS256"
HTTP_TIMEOUT = 10.0

WIDGET_CATALOG = [
	{
		"name": "discord",
		"widgets": [
			{
				"name": "discord_profile",
				"params": [
					{"name": "avatar_size", "type": "int"},
				],
			},
			{
				"name": "discord_banner", # TODO faire un chemin API vers discord/discord_banner pour récupérer la bannière de l'utilisateur
				"params": [
					{"name": "banner_width", "type": "int"},
				],
			},
		],
	},
	{
		"name": "steam",
		"widgets": [
			{
				"name": "steam_profile",
				"params": [
					{"name": "avatar_size", "type": "int"},
				],
			},
			{
				"name": "steam_currentgame",
				"params": [
					{"name": "icon_size", "type": "int"},
				],
			},
			{
				"name": "steam_lastgame",
				"params": [
					{"name": "count", "type": "int"},
				],
			},
		],
	},
	{
		"name": "weather",
		"widgets": [
			{
				"name": "forecast",
				"params": [
					{"name": "city", "type": "string"},
				],
			},
			{
				"name": "air_quality",
				"params": [
					{"name": "city", "type": "string"},
				],
			},
		],
	},
]
