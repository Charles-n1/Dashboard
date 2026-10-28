import { useEffect, useState } from 'react'
import { STEAM_URLS } from '../config'
import Status_auth_steam from './status_auth_steam'
import './auth_steam.css'


function createSteamLoginUrl(token) {
  return `${STEAM_URLS.login}?jwt=${encodeURIComponent(token)}`
}

function Auth_steam({ onConnectionChange }) {
  const [user, setUser] = useState(null)
  const token = localStorage.getItem('access_token')
  const loginUrl = createSteamLoginUrl(token)

  useEffect(() => {
    if (!token)
      return

    fetch(STEAM_URLS.profile, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => (response.ok ? response.json() : null))
      .then(setUser)
      .catch(() => setUser(null))
  }, [token])
  useEffect(() => { onConnectionChange(user) }, [user, onConnectionChange])

  return (
    <Status_auth_steam user={user} token={token} loginUrl={loginUrl} />
  )
}

export default Auth_steam
