import { useEffect, useState } from 'react'
import { METEO_URLS } from '../../config'
import './widget_forecast.css'
import sun from '../../assets/Meteo/Sun-removebg-preview.png'
import moon from '../../assets/Meteo/Moon-removebg-preview.png'
import cloud from '../../assets/Meteo/Cloud-removebg-preview.png'
import smoke from '../../assets/Meteo/Smoke-removebg-preview.png'
import water from '../../assets/Meteo/Water-removebg-preview.png'
import ice from '../../assets/Meteo/Ice-removebg-preview.png'
import lightning from '../../assets/Meteo/Lightning-removebg-preview.png'


function weatherImage(code, isDay) {
  if (code <= 1)
    return isDay ? sun : moon
  if (code <= 3)
    return cloud
  if (code <= 48)
    return smoke
  if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82))
    return water
  if ((code >= 71 && code <= 77) || code === 85 || code === 86)
    return ice
  if (code >= 95)
    return lightning
  return null
}

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
    const data = await get(METEO_URLS.forecast, {latitude: location.latitude, longitude: location.longitude})
    const temperature = data.current?.temperature_2m
    const humidity = data.current?.relative_humidity_2m
    const wind = data.current?.wind_speed_10m
    const image = weatherImage(data.current?.weather_code, data.current?.is_day)
    if (typeof temperature !== 'number')
      throw new Error('Weather response did not include the current temperature.')

    return [temperature + ' °C', humidity + ' %', wind + ' km/h', image]
  } catch (error) {
    console.error('Unable to load weather:', error)
    return ['Météo indisponible', '-', '-', null]
  }
}

function widget_forecast({ city }) {
  const [temperature, setTemperature] = useState('...')
  const [humidity, setHumidity] = useState('...')
  const [wind, setWind] = useState('...')
  const [image, setImage] = useState(null)

  useEffect(() => {
    let active = true
    getWeather(city).then(value => {
      if (active) {
        setTemperature(value[0])
        setHumidity(value[1])
        setImage(value[3])
        setWind(value[2])
      }
    })

    return () => {
      active = false
    }
  }, [city])

  return (
    <div className="widget_forecast">
      <h2>Météo : {city}</h2>
      {image && <img className="widget_forecast_icon" src={image} alt="" />}
      <strong>Température: {temperature}</strong>
      <p>Humidité: {humidity}</p>
      <p>Vent: {wind}</p>
    </div>
  )
}

export default widget_forecast
