import './register.css'
import { useState } from 'react'
import { BACKEND_URLS } from '../config'

async function onSubmit(e, onRegister) {
  e.preventDefault()

  const data = Object.fromEntries(new FormData(e.target))
  let response

  try {
    response = await fetch(BACKEND_URLS.register, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
  } catch {
    throw new Error('Impossible de joindre le serveur. Vérifiez que le backend est démarré.')
  }

  if (!response.ok) {
    const error = await response.json().catch(() => null)
    throw new Error(error?.detail || 'La création du compte a échoué.')
  }

  onRegister()
}

function Register({ onRegister }) {
  const [error, setError] = useState('')

  return (
    <form className="register" onSubmit={e => onSubmit(e, onRegister).catch(error => setError(error.message))}>
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <input name="username" placeholder="Username" maxLength="256"/>
      <input name="email" type="email" placeholder="Email" maxLength="1024"/>
      <input name="password" type="password" placeholder="Password" minLength="8" maxLength="256"/>
      <input name="first_name" placeholder="First name" maxLength="256"/>
      <input name="last_name" placeholder="Last name" maxLength="256"/>
      <button>S'inscrire</button>
    </form>
  )
}

export default Register
