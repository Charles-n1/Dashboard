import { useEffect, useState } from 'react'
import { DISCORD_URLS } from '../config'
import Status_auth_discord from './status_auth_discord'
import './auth_discord.css'

function Auth_discord({ onConnectionChange }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const token = localStorage.getItem('access_token')

  useEffect(() => {
    let isCurrent = true

    async function loadDiscordAccount() {
      if (!token) {
        setUser(null)
        setIsLoading(false)
        return
      }

      setIsLoading(true)
      try {
        const response = await fetch(DISCORD_URLS.profile, {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (isCurrent)
          setUser(response.ok ? await response.json() : null)
      } catch {
        if (isCurrent)
          setUser(null)
      } finally {
        if (isCurrent)
          setIsLoading(false)
      }
    }

    loadDiscordAccount()
    return () => { isCurrent = false }
  }, [token])

  useEffect(() => { onConnectionChange(user) }, [user, onConnectionChange])

  const loginUrl = token
    ? `${DISCORD_URLS.login}?token=${encodeURIComponent(token)}`
    : DISCORD_URLS.login

  return <Status_auth_discord user={user} token={token} isLoading={isLoading} loginUrl={loginUrl} />
}

export default Auth_discord
