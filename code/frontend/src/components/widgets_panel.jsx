import Widget_discord_profile from '../widgets/discord/widget_discord_profile'
import Widget_discord_banner from '../widgets/discord/widget_discord_banner'
import Widget_steam_currentgame from '../widgets/steam/widget_steam_currentgame'
import Widget_steam_lastgame from '../widgets/steam/widget_steam_lastgame'
import Widget_steam_profile from '../widgets/steam/widget_steam_profile'
import widget_forecast from '../widgets/weather/widget_forecast'
import widget_air_quality from '../widgets/weather/widget_air_quality'
import return_logo from '../assets/left_arrow.svg'
import { GRID } from '../config'
import { useState } from 'react'
import './widget_panel.css'

const SERVICE_WIDGETS = {
	discord: [
		['discord_profile', Widget_discord_profile],
		['discord_banner', Widget_discord_banner],
	],
	steam: [
		['steam_profile', Widget_steam_profile],
		['steam_currentgame', Widget_steam_currentgame],
		['steam_lastgame', Widget_steam_lastgame],
	],
	weather: [['forecast', widget_forecast], ['air_quality', widget_air_quality]],
}

const GRID_RATIOS = [
	{ value: '1:1', columns: 10, rows: 10 },
	{ value: '4:3', columns: 8, rows: 6 },
	{ value: '3:2', columns: 9, rows: 6 },
	{ value: '8:5', columns: 8, rows: 5 },
	{ value: '5:4', columns: 10, rows: 8 },
	{ value: '3:4', columns: 6, rows: 8 },
	{ value: '2:3', columns: 6, rows: 9 },
	{ value: '5:9', columns: 5, rows: 9 },
	{ value: '13:6', columns: 26, rows: 12 },
]

function getGridRatio({ columns, rows }) {
	let first = columns
	let second = rows
	while (second) {
		[first, second] = [second, first % second]
	}
	return `${columns / first}:${rows / first}`
}

function onDragStart(event, name, setIsDraggingWidget) {
	event.dataTransfer.setData('text', name)
	setIsDraggingWidget(true)
}

function WidgetsPanel({ service, isOpen, onBack, onWidgetSelect, gridShape, onGridShapeChange }) {
	const [isDraggingWidget, setIsDraggingWidget] = useState(false)
	const widgets = SERVICE_WIDGETS[service] || []
	const title = service === 'dashboard' ? 'Dashboard settings' : service === 'weather' ? 'Weather' : service ? service[0].toUpperCase() + service.slice(1) : ''
	const selectedRatio = getGridRatio(gridShape)
	const hasRatioPreset = GRID_RATIOS.some(ratio => ratio.value === selectedRatio)

	return (
		<aside className={`widgets_panel ${isOpen ? 'widgets_panel_open' : ''}${isDraggingWidget ? ' widgets_panel_dragging' : ''}`} aria-hidden={!isOpen}>
			<div className="widgets_panel_heading">
				<button className="widgets_panel_back" type="button" onClick={onBack} aria-label="Back to services">
					<img src={return_logo} className="widgets_panel_back_icon" alt="Back"/>
				</button>
				<h2>{service === 'dashboard' ? title : `${title} widgets`}</h2>
			</div>
			{service === 'dashboard' ? (
				<section className="dashboard_settings">
					<label>
						Columns
						<select value={gridShape.columns} onChange={event => onGridShapeChange({ ...gridShape, columns: Number(event.target.value) })}>
							{Array.from({ length: GRID.columns }, (_, index) => index + 1).map(value => <option key={value} value={value}>{value}</option>)}
						</select>
					</label>
					<label>
						Rows
						<select value={gridShape.rows} onChange={event => onGridShapeChange({ ...gridShape, rows: Number(event.target.value) })}>
							{Array.from({ length: GRID.rows }, (_, index) => index + 1).map(value => <option key={value} value={value}>{value}</option>)}
						</select>
					</label>
					<label>
						Ratio
						<select
							value={hasRatioPreset ? selectedRatio : 'custom'}
							onChange={event => {
								const ratio = GRID_RATIOS.find(option => option.value === event.target.value)
								if (ratio)
									onGridShapeChange({ columns: ratio.columns, rows: ratio.rows })
							}}
						>
							{!hasRatioPreset && <option value="custom">Custom ({selectedRatio})</option>}
							{GRID_RATIOS.map(ratio => <option key={ratio.value} value={ratio.value}>{ratio.value}</option>)}
						</select>
					</label>
					<p>{gridShape.columns * gridShape.rows} cells · {selectedRatio}</p>
				</section>
			) : widgets.map(([name, Widget]) => (
				<div
					className="widget_option"
					draggable
					key={name}
					onDragStart={event => onDragStart(event, name, setIsDraggingWidget)}
					onDragEnd={() => setIsDraggingWidget(false)}
				>
					<Widget className="widget_component" />
					<button type="button" className="widget_add" onClick={() => onWidgetSelect(name)}>Add widget</button>
				</div>
			))}
		</aside>
	)
}

export default WidgetsPanel
