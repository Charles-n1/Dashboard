import { useEffect, useState } from 'react'
import { METEO_URLS } from '../../config'
import './widget_air_quality.css'

async function get(url, params) {
  const response = await fetch(url + '?' + new URLSearchParams(params))

  if (!response.ok) {
    const details = await response.text()
    throw new Error(`Weather request failed (${response.status}): ${details}`)
  }

  return response.json()
}

async function getWeather(city) {
  try {
    const geo = await get(METEO_URLS.city_location, { name: city, count: 1 })
    const location = geo.results?.[0]
    if (!location)
      throw new Error(`No location found for "${city}".`)
    const data = await get(METEO_URLS.air_quality, {latitude: location.latitude, longitude: location.longitude})
    const time = data.current?.time
    const pm10 = data.current?.pm10
    const pm2_5 = data.current?.pm2_5
    const carbon_monoxide = data.current?.carbon_monoxide
    const nitrogen_dioxide = data.current?.nitrogen_dioxide
    const ozone = data.current?.ozone
    const european_aqi = data.current?.european_aqi
    
    return [time, pm10, pm2_5, carbon_monoxide, nitrogen_dioxide, ozone, european_aqi]
  } catch (error) {
    console.error('Unable to load weather:', error)
    return 'Météo indisponible'
  }
}

function widget_air_quality({ city }) {
  const [time, setTime] = useState('...')
  const [pm10, setPm10] = useState('...')
  const [pm2_5, setPm2_5] = useState('...')
  const [carbon_monoxide, setCarbonMonoxide] = useState('...')
  const [nitrogen_dioxide, setNitrogenDioxide] = useState('...')
  const [ozone, setOzone] = useState('...')
  const [european_aqi, setEuropeanAqi] = useState('...')

  useEffect(() => {
    let active = true
    getWeather(city).then(value => {
      if (active) {
        setTime(value[0])
        setPm10(value[1])
        setPm2_5(value[2])
        setCarbonMonoxide(value[3])
        setNitrogenDioxide(value[4])
        setOzone(value[5])
        setEuropeanAqi(value[6])
      }
    })

    return () => {
      active = false
    }
  }, [city])

  return (
    <div className="widget_air_quality">
      <h2>Qualité de l'air</h2>
      <p>Heure: {time}</p>
      <p>PM10: {pm10}</p>
      <p>PM2.5: {pm2_5}</p>
      <p>Oxyde de carbone: {carbon_monoxide}</p>
      <p>Oxyde d'azote: {nitrogen_dioxide}</p>
      <p>Ozone: {ozone}</p>
      <p>AQI européen: {european_aqi}</p>
    </div>
  )
}

export default widget_air_quality
