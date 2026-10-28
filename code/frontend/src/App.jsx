import { useEffect, useState } from 'react'
import Register from './pages/register'
import Login from './pages/login'
import Dashboard from './pages/dashboard'
import { BACKEND_URLS } from './config'
import logo from './assets/logo.svg'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    () => localStorage.getItem('access_token') ? null : false,
  )
  const [isVisitor, setIsVisitor] = useState(false)
  const [showLogin, setShowLogin] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token)
      return

    fetch(BACKEND_URLS.me, {headers: {Authorization: `Bearer ${token}`}})
      .then(response => {
        if (!response.ok)
          localStorage.removeItem('access_token')
        setIsAuthenticated(response.ok)
      })
      .catch(() => {
        localStorage.removeItem('access_token')
        setIsAuthenticated(false)
      })
  }, [])

  function handleLogout() {
    localStorage.removeItem('access_token')
    setIsAuthenticated(false)
    setIsVisitor(false)
    setShowLogin(true)
  }

  if (isAuthenticated === null)
    return null

  if (isAuthenticated || isVisitor)
    return (
      <Dashboard
        isVisitor={isVisitor}
        onSignIn={() => {
          setIsVisitor(false)
          setShowLogin(true)
        }}
        onLogout={handleLogout}
      />
    )

  return (
    <main className="auth-page">
      <div className="lava-background" aria-hidden="true">
        <span className="lava-orb orb-1" />
        <span className="lava-orb orb-2" />
        <span className="lava-orb orb-3" />
        <span className="lava-orb orb-4" />
      </div>

      <section className="auth-panel">
        <img className="auth-logo" src={logo} alt="Logo Wunderbar" />
        <p className="auth-kicker">Wunderbar</p>
        <p className="auth-kicker">Dashboard</p>
        {showLogin ? (
          <>
            <Login onLogin={() => {
              setIsAuthenticated(true)
              setIsVisitor(false)
            }} />
            <button className="auth-switch" type="button" onClick={() => setShowLogin(false)}>
              Créer un compte
            </button>
          </>
        ) : (
          <>
            <Register onRegister={() => setShowLogin(true)} />
            <button className="auth-switch" type="button" onClick={() => setShowLogin(true)}>
              Se connecter
            </button>
          </>
        )}
        <button className="auth-visitor" type="button" onClick={() => setIsVisitor(true)}>
          Visiter
        </button>
      </section>
    </main>
  )
}

export default App
