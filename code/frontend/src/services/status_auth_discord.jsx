import './status_auth_discord.css'

function Status_auth_discord({ user, token, isLoading, loginUrl }) {
  if (user)
    return <p>Connecté en tant que {user.global_name || user.username}</p>

  if (isLoading)
    return <p>Vérification de la connexion Discord...</p>

  return (
    token
      ? <a href={loginUrl}>Connecter Discord</a>
      : <p>Connectez-vous à votre compte pour lier Discord.</p>
  )
}

export default Status_auth_discord
