import { useEffect, useState } from 'react'
import { DISCORD_URLS } from '../../config'
import './widget_discord_profile.css'

async function getProfile() {
  const token = localStorage.getItem('access_token')
  const response = await fetch(DISCORD_URLS.profile, {headers: {Authorization: `Bearer ${token}`}})

  if (!response.ok)
    return null
  return response.json()
}

function avatarUrl(profile, avatarSize) {
  return `${DISCORD_URLS.avatar}/${profile.id}/${profile.avatar}.png?size=${avatarSize}`
}

function showProfile(profile, avatarSize) {
  if (!profile)
    return 'Discord : non connecté'

  return (
    <>
      <img src={avatarUrl(profile, avatarSize)} style={{ width: avatarSize, height: avatarSize }} alt="Avatar Discord" />
      <p>{profile.global_name ?? profile.username}</p>
    </>
  )
}

function Widget_discord_profile({ avatarSize }) {
  const [profile, setProfile] = useState(null)

  useEffect(() => { getProfile().then(setProfile) }, [])

  return (
    <div className="widget_discord_profile">
      {showProfile(profile, avatarSize)}
    </div>
  )
}


export default Widget_discord_profile
