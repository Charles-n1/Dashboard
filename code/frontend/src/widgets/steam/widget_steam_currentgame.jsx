import { useEffect, useState } from 'react'
import { STEAM_URLS } from '../../config'
import './widget_steam_currentgame.css'

async function getCurrentGame() {
  const token = localStorage.getItem('access_token')
  const response = await fetch(STEAM_URLS.currentGame, {headers: {Authorization: `Bearer ${token}`}})

  if (!response.ok)
    return null
  return response.json()
}

function showCurrentGame(game) {
  if (!game)
    return 'Steam : non connecté'

  if (!game.name)
    return 'Aucun jeu en cours'

  return <p>{game.name}</p>
}

function Widget_steam_currentgame() {
  const [game, setGame] = useState(null)

  useEffect(() => { getCurrentGame().then(setGame) }, [])

  return (
    <div className="widget_steam_currentgame">
      {showCurrentGame(game)}
    </div>
  )
}

export default Widget_steam_currentgame
