import { useEffect, useState } from 'react'
import { STEAM_URLS } from '../../config'
import './widget_steam_profile.css'

async function getProfile() {
  const token = localStorage.getItem('access_token')
  const response = await fetch(STEAM_URLS.profile, {headers: {Authorization: `Bearer ${token}`}})

  if (!response.ok)
    return null
  return response.json()
}

function showProfile(profile, avatarSize) {
  if (!profile)
    return 'Steam : non connecté'

  return (
    <>
      <img src={profile.avatar} style={{ width: avatarSize, height: avatarSize }} alt="Avatar Steam" />
      <p>{profile.username}</p>
    </>
  )
}

function Widget_steam_profile({ avatarSize }) {
  const [profile, setProfile] = useState(null)

  useEffect(() => { getProfile().then(setProfile) }, [])

  return (
    <div className="widget_steam_profile">
      {showProfile(profile, avatarSize)}
    </div>
  )
}

export default Widget_steam_profile
