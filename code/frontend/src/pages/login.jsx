import './login.css'
import { useState } from 'react'
import { BACKEND_URLS } from '../config'

async function onSubmit(e, onLogin) {
  e.preventDefault()
  const data = Object.fromEntries(new FormData(e.target))
  let response
  try {
    response = await fetch(BACKEND_URLS.login, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
  } catch {
    throw new Error('Impossible de joindre le serveur. Vérifiez que le backend est démarré.')
  }

  if (!response.ok)
    throw new Error('Identifiants invalides.')

  const { access_token: accessToken } = await response.json()
  localStorage.setItem('access_token', accessToken)
  onLogin()
}

function Login({ onLogin }) {
  const [error, setError] = useState('')

  return (
    <form className="login" onSubmit={e => onSubmit(e, onLogin).catch(error => setError(error.message))}>
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <input name="email" type="email" placeholder="Email" maxLength="1024"/>
      <input name="password" type="password" placeholder="Password" maxLength="256"/>
      <button>Se connecter</button>
    </form>
  )
}

export default Login
