import './status_auth_steam.css'

function Status_auth_steam({ user, token, loginUrl }) {
  if (!token)
    return <p>Connectez-vous à votre compte pour lier Steam.</p>

  if (!user)
    return <a href={loginUrl}>Se connecter avec Steam</a>

  return (
    <div className="steam_user">
      <img src={user.avatar} alt="Avatar Steam" />
      <p>Connecté en tant que {user.username}</p>
    </div>
  )
}

export default Status_auth_steam
