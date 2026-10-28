import { useEffect, useState } from 'react'
import { STEAM_URLS } from '../../config'
import './widget_steam_lastgame.css'

async function getLastGames() {
  const token = localStorage.getItem('access_token')
  const response = await fetch(`${STEAM_URLS.lastGame}?count=3`, {headers: {Authorization: `Bearer ${token}`}})

  if (!response.ok)
    return null
  return response.json()
}

function iconUrl(game) {
  return `${STEAM_URLS.icon}/${game.appid}/${game.img_icon_url}.jpg`
}

function showGame(game) {
  return (
    <div className="widget_steam_lastgame_row" key={game.appid}>
      <p>{game.name}</p>
      <img src={iconUrl(game)} alt="" />
    </div>
  )
}

function showLastGames(games) {
  if (!games)
    return 'Steam : non connecté'

  if (games.length === 0)
    return 'Aucun jeu récent'

  return games.map(showGame)
}

function Widget_steam_lastgame() {
  const [games, setGames] = useState(null)

  useEffect(() => { getLastGames().then(setGames) }, [])

  return (
    <div className="widget_steam_lastgame">
      {showLastGames(games)}
    </div>
  )
}

export default Widget_steam_lastgame
