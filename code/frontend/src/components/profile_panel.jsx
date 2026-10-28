import default_profile from '../assets/default_256.jpg'
import './profile_panel.css'
import { useEffect, useRef, useState } from 'react'
import { BACKEND_URLS } from '../config'

function Profile_panel({ isOpen, onLogout, onUserUpdated }) {
  const [user, setUser] = useState(null)
  const [avatarUrl, setAvatarUrl] = useState(default_profile)
  const [editing, setEditing] = useState(null)
  const [username, setUsername] = useState('')
  const [currentPassword, setCurrentPassword] = useState('')
  const [password, setPassword] = useState('')
  const [passwordConfirmation, setPasswordConfirmation] = useState('')
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const avatarObjectUrl = useRef(null)

  useEffect(() => {
      const token = localStorage.getItem('access_token')
      if (!token)
          return

      fetch(BACKEND_URLS.me, {headers: {Authorization: `Bearer ${token}`}})
          .then(response => response.ok ? response.json() : null)
          .then(data => data && setUser(data))
          .catch(() => {})
  }, [])

  useEffect(() => () => {
    if (avatarObjectUrl.current)
      URL.revokeObjectURL(avatarObjectUrl.current)
  }, [])

  async function saveProfile(event) {
    event.preventDefault()
    setError('')
    setMessage('')

    if (editing === 'password' && password !== passwordConfirmation) {
      setError('Les mots de passe ne correspondent pas.')
      return
    }

    const token = localStorage.getItem('access_token')
    if (!token) {
      setError('Vous devez être connecté pour modifier votre profil.')
      return
    }

    const payload = editing === 'username'
      ? { username: username.trim() }
      : { current_password: currentPassword, password }
    setSaving(true)
    try {
      const response = await fetch(BACKEND_URLS.me, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
      const result = await response.json().catch(() => null)
      if (!response.ok)
        throw new Error(result?.detail || 'La modification a échoué.')

      setUser(result)
      onUserUpdated?.({ user: result })
      setEditing(null)
      setCurrentPassword('')
      setPassword('')
      setPasswordConfirmation('')
      setMessage(editing === 'username' ? 'Nom mis à jour.' : 'Mot de passe mis à jour.')
    } catch (requestError) {
      setError(requestError.message || 'Une erreur réseau est survenue.')
    } finally {
      setSaving(false)
    }
  }

  async function changeAvatar(event) {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (!file)
      return

    setError('')
    setMessage('')
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      setError('Choisissez une image JPEG ou PNG.')
      return
    }

    try {
      const bitmap = await createImageBitmap(file)
      const scale = Math.min(1, 512 / Math.max(bitmap.width, bitmap.height))
      const canvas = document.createElement('canvas')
      canvas.width = Math.max(1, Math.round(bitmap.width * scale))
      canvas.height = Math.max(1, Math.round(bitmap.height * scale))
      canvas.getContext('2d').drawImage(bitmap, 0, 0, canvas.width, canvas.height)
      bitmap.close()

      const resizedImage = await new Promise((resolve, reject) => {
        canvas.toBlob(
          (blob) => blob ? resolve(blob) : reject(new Error('Impossible de redimensionner cette image.')),
          file.type,
          0.9,
        )
      })
      const previewUrl = URL.createObjectURL(resizedImage)
      if (avatarObjectUrl.current)
        URL.revokeObjectURL(avatarObjectUrl.current)
      avatarObjectUrl.current = previewUrl
      setAvatarUrl(previewUrl)
      onUserUpdated?.({ avatarUrl: previewUrl })
      setMessage('Aperçu de la photo mis à jour.')
      // TODO: Upload this resized JPEG/PNG to the profile-picture endpoint when one is available.
    } catch (imageError) {
      setError(imageError.message || 'Impossible de lire cette image.')
    }
  }

  return (
    <aside className={`profile_panel ${isOpen ? 'profile_panel_open' : ''}`}>
      <div className="profile_container">
        <h2 className="profile_options_title">Profile</h2>
        <div className="profile_avatar_wrap">
          <img className="profile_avatar" src={avatarUrl} alt="Photo de profil" />
          <label className="profile_avatar_edit" htmlFor="profile-avatar-input">
            Modifier la photo
            <input
              id="profile-avatar-input"
              className="profile_avatar_input"
              type="file"
              accept="image/jpeg,image/png"
              onChange={changeAvatar}
            />
          </label>
        </div>
        <div className="profile_name_row">
          {editing === 'username' ? (
            <form className="profile_edit_form" onSubmit={saveProfile}>
              <label htmlFor="profile-username">Nom d'utilisateur</label>
              <input
                id="profile-username"
                type="text"
                autoComplete="username"
                minLength={1}
                maxLength={256}
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                required
              />
              <div className="profile_edit_actions">
                <button type="submit" disabled={saving}>{saving ? 'Enregistrement…' : 'Enregistrer'}</button>
                <button type="button" onClick={() => setEditing(null)}>Annuler</button>
              </div>
            </form>
          ) : (
            <>
              <h1 className="profile_name">{user?.username || ''}</h1>
              <button
                className="profile_edit_button"
                type="button"
                onClick={() => {
                  setUsername(user?.username || '')
                  setEditing('username')
                  setMessage('')
                  setError('')
                }}
              >
                Modifier le nom
              </button>
            </>
          )}
        </div>
        <p className="profile_email">{user?.email || ''}</p>
      </div>
      <div className="options_container">
        <h2 className="profile_options_title">Security</h2>
        {editing === 'password' ? (
          <form className="profile_edit_form" onSubmit={saveProfile}>
            <label htmlFor="profile-current-password">Current Password</label>
            <input
              id="profile-current-password"
              type="password"
              autoComplete="current-password"
              value={currentPassword}
              onChange={(event) => setCurrentPassword(event.target.value)}
              required
            />
            <label htmlFor="profile-password">Nouveau mot de passe</label>
            <input
              id="profile-password"
              type="password"
              autoComplete="new-password"
              minLength={8}
              maxLength={256}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
            <label htmlFor="profile-password-confirmation">Confirmer le mot de passe</label>
            <input
              id="profile-password-confirmation"
              type="password"
              autoComplete="new-password"
              minLength={8}
              maxLength={256}
              value={passwordConfirmation}
              onChange={(event) => setPasswordConfirmation(event.target.value)}
              required
            />
            <div className="profile_edit_actions">
              <button type="submit" disabled={saving}>{saving ? 'Enregistrement…' : 'Enregistrer'}</button>
              <button
                type="button"
                onClick={() => {
                  setEditing(null)
                  setCurrentPassword('')
                  setPassword('')
                  setPasswordConfirmation('')
                }}
              >
                Annuler
              </button>
            </div>
          </form>
        ) : (
          <button
            className="profile_edit_button"
            type="button"
            onClick={() => {
              setEditing('password')
              setCurrentPassword('')
              setPassword('')
              setPasswordConfirmation('')
              setMessage('')
              setError('')
            }}
          >
            Modifier le mot de passe
          </button>
        )}
      </div>
      {(message || error) && (
        <p className={`profile_feedback ${error ? 'profile_feedback_error' : ''}`} role="status">
          {error || message}
        </p>
      )}
      <div className="delete_container">
        <button className="logout" type="button" onClick={onLogout}>
          log out
        </button>
        {/*<button className="logout" type="button" onClick={onDeleteAccount}>
          delete account
        </button>*/}
      </div>
    </aside>
  )
}

export default Profile_panel
