import Widget_discord_profile from '../widgets/discord/widget_discord_profile'
import Widget_discord_banner from '../widgets/discord/widget_discord_banner'
import Widget_steam_currentgame from '../widgets/steam/widget_steam_currentgame'
import Widget_steam_lastgame from '../widgets/steam/widget_steam_lastgame'
import Widget_steam_profile from '../widgets/steam/widget_steam_profile'
import widget_forecast from '../widgets/weather/widget_forecast'
import widget_air_quality from '../widgets/weather/widget_air_quality'
import { useState, useEffect } from 'react'
import { loadSetting, saveSetting } from '../settings'
import drag_logo from '../assets/drag.svg'
import './cell.css'


const WIDGETS = { discord_profile: Widget_discord_profile, discord_banner: Widget_discord_banner, steam_profile: Widget_steam_profile, steam_currentgame: Widget_steam_currentgame, steam_lastgame: Widget_steam_lastgame, forecast: widget_forecast, air_quality: widget_air_quality }

function onDragOver(e) {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
}

function onCellDragStart(e, name, widgetId, index) {
  e.stopPropagation()
  e.dataTransfer.effectAllowed = 'move'
  e.dataTransfer.setData('text', name)
  e.dataTransfer.setData('widgetId', widgetId)
  e.dataTransfer.setData('from', String(index))
}

function onContextMenu(e, name, index) {
  if (!WIDGETS[name])
    return
  e.preventDefault()
  console.log('Clic droit sur', name, 'case', index)
}

function onDelete(index, setCells) {
  setCells(cells => {
    const next = [...cells]
    next[index] = null
    return next
  })
}

function nextTick(t) {
  return t + 1
}

function startRefresh(Widget, refresh, setTick) {
  if (!Widget || !refresh)
    return

  const id = setInterval(setTick, refresh * 1000, nextTick)

  function stop() {
    clearInterval(id)
  }
  return stop
}

function cellContent(Widget, name, widgetId, tick, index, refresh, setRefresh, setCells, size, sizeOptions, onSizeChange, settingsOpen, setSettingsOpen, avatarSize, setAvatarSize, bannerWidth, setBannerWidth, city, setCity) {
  if (!Widget)
    return null

  return (
    <>
      <Widget key={tick} widgetId={widgetId} avatarSize={avatarSize} bannerWidth={bannerWidth} city={city} />
      <button className="drag_handle" type="button" draggable="true" aria-label="Move widget" title="Drag to move widget"
        onDragStart={e => onCellDragStart(e, name, widgetId, index)}>
        <img src={drag_logo} className="drag_icon" alt="Drag handle"/>
      </button>
      <button
        className="settings_handle"
        type="button"
        aria-label="Widget settings"
        aria-expanded={settingsOpen}
        aria-controls={`cell-settings-${index}`}
        title="Widget settings"
        onClick={() => setSettingsOpen(open => !open)}
      >
        ⚙
      </button>
      {settingsOpen && (
        <div className="cell_settings" id={`cell-settings-${index}`}>
          <label>
            Size
            <select
              aria-label="Widget size"
              value={`${size.width}x${size.height}`}
              onChange={event => {
                const [width, height] = event.target.value.split('x').map(Number)
                onSizeChange(index, { width, height })
              }}
            >
              {sizeOptions.map(option => (
                <option key={`${option.width}x${option.height}`} value={`${option.width}x${option.height}`}>
                  {option.width}x{option.height}
                </option>
              ))}
            </select>
          </label>
          {name === 'discord_profile' && (
            <label>
              Avatar size
              <input type="number" min="1" step="1" defaultValue={avatarSize} onKeyDown={event => saveSetting(event, 'avatar_size', widgetId, setAvatarSize, true)} />
            </label>
          )}
          {name === 'discord_banner' && (
            <label>
              Banner width
              <input type="number" min="1" step="1" defaultValue={bannerWidth} onKeyDown={event => saveSetting(event, 'banner_width', widgetId, setBannerWidth, true)} />
            </label>
          )}
          {name === 'forecast' && (
            <label>
              City
              <input defaultValue={city} onKeyDown={event => saveSetting(event, 'city', widgetId, setCity)} />
            </label>
          )}
          {name === 'air_quality' && (
            <label>
              City
              <input defaultValue={city} onKeyDown={event => saveSetting(event, 'city', widgetId, setCity)} />
            </label>
          )}
          {['discord_profile', 'discord_banner', 'forecast', 'air_quality'].includes(name) && (
            <label>
              Refresh (seconds)
              <input type="number" min="20" max="3600" step="1" defaultValue={refresh} onKeyDown={event => saveSetting(event, 'refresh', widgetId, setRefresh, true)} />
            </label>
          )}
          <p>Press Enter to save changes.</p>
        </div>
      )}
      <button className="delete" aria-label="Supprimer le widget" onClick={() => onDelete(index, setCells)}>×</button>
    </>
  )
}

function Cell({ name, widgetId, index, setCells, size, sizeOptions, onSizeChange, onDrop, style }) {
  const Widget = WIDGETS[name]
  const [refresh, setRefresh] = useState(() => {
    const savedRefresh = Number(loadSetting('refresh', widgetId, 30, true))
    return Number.isFinite(savedRefresh) ? Math.max(20, savedRefresh) : 30
  })
  const [avatarSize, setAvatarSize] = useState(() => loadSetting('avatar_size', widgetId, 64, true))
  const [bannerWidth, setBannerWidth] = useState(() => loadSetting('banner_width', widgetId, 300, true))
  const [city, setCity] = useState(() => loadSetting('city', widgetId, 'Lyon'))
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [tick, setTick] = useState(0)

  useEffect(() => startRefresh(Widget, refresh, setTick), [Widget, refresh])

  return (
    <div
      className={`cell${settingsOpen ? ' cell_settings_open' : ''}`}
      onDragOver={onDragOver}
      onDrop={e => onDrop(e, index)}
      onContextMenu={e => onContextMenu(e, name, index)}
      style={style}
    >
      {cellContent(Widget, name, widgetId, tick, index, refresh, setRefresh, setCells, size, sizeOptions, onSizeChange, settingsOpen, setSettingsOpen, avatarSize, setAvatarSize, bannerWidth, setBannerWidth, city, setCity)}
    </div>
  )
}

export default Cell
