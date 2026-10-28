import { useEffect, useState } from 'react'
import { DISCORD_URLS } from '../../config'
import './widget_discord_banner.css'

async function getProfile() {
  const token = localStorage.getItem('access_token')
  const response = await fetch(DISCORD_URLS.profile, {headers: {Authorization: `Bearer ${token}`}})

  if (!response.ok)
    return null
  return response.json()
}

function showBanner(profile, bannerWidth) {
  if (!profile)
    return 'Discord : non connecté'
  if (!profile.banner)
    return 'Pas de bannière'
  return <img src={`${DISCORD_URLS.banner}/${profile.id}/${profile.banner}.png`} style={{ width: bannerWidth }} alt="Bannière Discord" />
}

function Widget_discord_banner({ bannerWidth }) {
  const [profile, setProfile] = useState(null)

  useEffect(() => { getProfile().then(setProfile) }, [])

  return (
    <div className="widget_discord_banner">
      {showBanner(profile, bannerWidth)}
    </div>
  )
}

export default Widget_discord_banner
