import { useEffect, useState } from 'react'
import './services_panel.css'
import WidgetsPanel from './widgets_panel'
import Auth_discord from '../services/auth_discord'
import Auth_steam from '../services/auth_steam'
import { SERVICE_STATUS_URLS } from '../config'

function ServicesPanel({ isOpen, onWidgetSelect, gridShape, onGridShapeChange }) {
    const [discordUser, setDiscordUser] = useState(null)
    const [steamUser, setSteamUser] = useState(null)
    const [backendStatus, setBackendStatus] = useState({
        discord: 'checking',
        steam: 'checking',
        weather: 'checking',
    })
    const [selectedService, setSelectedService] = useState(null)

    useEffect(() => {
        if (!isOpen)
            setSelectedService(null)
    }, [isOpen])

    useEffect(() => {
        let isCurrent = true

        async function checkServiceStatuses() {
            const statuses = await Promise.all(
                Object.entries(SERVICE_STATUS_URLS).map(async ([service, url]) => {
                    try {
                        const response = await fetch(url)
                        if (!response.ok)
                            return [service, 'unreachable']

                        const result = await response.json()
                        if (result.service !== service || typeof result.status !== 'string')
                            return [service, 'unreachable']

                        if (result.status === 'implemented')
                            return [service, 'ready']
                        if (result.status === 'not implemented')
                            return [service, 'not-implemented']
                        return [service, 'unreachable']
                    } catch {
                        return [service, 'unreachable']
                    }
                }),
            )

            if (isCurrent)
                setBackendStatus(Object.fromEntries(statuses))
        }

        checkServiceStatuses()
        return () => { isCurrent = false }
    }, [])

    function backendStatusLabel(service) {
        switch (backendStatus[service]) {
            case 'checking':
                return 'Checking API...'
            case 'ready':
                return 'API implemented'
            case 'not-implemented':
                return 'API reachable · not implemented'
            default:
                return 'API unavailable'
        }
    }

    function serviceCard(name, connected, detail, authControl, statusLabel) {
        return (
            <section className={`service_card ${connected ? '' : 'service_card_unavailable'}`} key={name}>
                <button
                    className="service_card_header"
                    type="button"
                    disabled={!connected}
                    onClick={() => setSelectedService(name.toLowerCase())}>
                    <span>{name}</span>
                    <span className="service_status">{statusLabel || (connected ? 'Connected' : 'Not connected')}</span>
                </button>
                {detail && <p className="service_detail">{detail}</p>}
                {authControl && <div className="service_auth">{authControl}</div>}
            </section>
        )
    }

    return (
        <>
            <aside className={`services_panel ${isOpen && !selectedService ? 'services_panel_open' : ''}`}>
                <h2>Nos services</h2>
                {serviceCard('Discord', Boolean(discordUser), 'Le service Discord, donne accès aux fonctionnalités Discord', <Auth_discord onConnectionChange={setDiscordUser} />, backendStatusLabel('discord'))}
                {serviceCard('Steam', Boolean(steamUser), 'Le service Steam, donne accès aux fonctionnalités Steam', <Auth_steam onConnectionChange={setSteamUser} />, backendStatusLabel('steam'))}
                {serviceCard('Weather', true, 'Le service Météo, donne accès aux informations météorologiques', null, backendStatusLabel('weather'))}
                {serviceCard('Dashboard', true, 'Les paramètres du tableau de bord local', null, 'Local')}
            </aside>
            <WidgetsPanel
                service={selectedService}
                isOpen={isOpen && Boolean(selectedService)}
                onBack={() => setSelectedService(null)}
                onWidgetSelect={onWidgetSelect}
                gridShape={gridShape}
                onGridShapeChange={onGridShapeChange}
            />
        </>
    )
}

export default ServicesPanel
