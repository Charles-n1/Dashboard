import './header.css'
import menuButton from '../assets/add_256.png'
import logo from '../assets/logo.svg'
import default_profile from '../assets/default_256.jpg'
import ServicesPanel from './services_panel'
import { useEffect, useState } from 'react'
import Profile_panel from './profile_panel'
import { BACKEND_URLS } from '../config'

function Header({ isMenuOpen, setIsMenuOpen, onWidgetSelect, gridShape, onGridShapeChange, isVisitor, onSignIn, onLogout }) {
    const [isPanelOpen, setIsPanelOpen] = useState(false)
    const [user, setUser] = useState(null)
    const [profileAvatar, setProfileAvatar] = useState(default_profile)

    function handleProfileUpdate({ user: updatedUser, avatarUrl }) {
        if (updatedUser)
            setUser(updatedUser)
        if (avatarUrl)
            setProfileAvatar(avatarUrl)
    }

    useEffect(() => {
        if (isVisitor)
            return

        const token = localStorage.getItem('access_token')
        if (!token) {
            return
        }

        fetch(BACKEND_URLS.me, {headers: {Authorization: `Bearer ${token}`}})
            .then(response => response.ok ? response.json() : null)
            .then(data => data && setUser(data))
            .catch(() => {})
    }, [isVisitor])

    return (
        <div className="header">
            <button className="header_menu" type="button" aria-label="Ouvrir le menu" onClick={() => setIsMenuOpen(!isMenuOpen)} aria-expanded={isMenuOpen}>
                <img src={menuButton} className={isMenuOpen ? "menu_icon menu_icon--open" : "menu_icon"} alt="Add a new widget" />
            </button>

            <div className="header_logo_container">
                <img className="header_logo_image" src={logo} alt="Logo de l'application" />
                <span className="header_logo_text">DASHBOARD IST WUNDERBAR</span>
            </div>

            <div className={isVisitor ? 'header_profile_container header_visitor_container' : 'header_profile_container'}>
                {isVisitor ? (
                    <button className="header_auth_button" type="button" onClick={onSignIn}>
                        Se connecter
                    </button>
                ) : (
                    <>
                        <span className="header_username">{user?.username || ''}</span>
                        <span className="header_mail">{user?.email || ''}</span>
                        <button className="profile_button" type="button" aria-label="Ouvrir le profile" onClick={() => setIsPanelOpen(!isPanelOpen)} aria-expanded={isPanelOpen}>
                            <img className="header_avatar" src={profileAvatar} alt="Photo de profil"/>
                        </button>
                    </>
                )}
            </div>

            <ServicesPanel
                isOpen={isMenuOpen}
                onWidgetSelect={onWidgetSelect}
                gridShape={gridShape}
                onGridShapeChange={onGridShapeChange}
            />
            <Profile_panel isOpen={isPanelOpen} onLogout={onLogout} onUserUpdated={handleProfileUpdate} />
        </div>
    )
}




export default Header
