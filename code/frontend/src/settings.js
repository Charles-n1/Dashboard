export function loadSetting(name, widgetId, byDefault, toNumber) {
  const value = localStorage.getItem(`${name}_${widgetId}`)

  if (!value)
    return byDefault
  if (toNumber)
    return Number(value)
  return value
}

export function saveSetting(e, name, widgetId, set, toNumber) {
  if (e.key !== 'Enter')
    return

  let value = e.target.value
  if (name === 'refresh') {
    value = String(Math.max(20, Number(value) || 20))
    e.target.value = value
  }

  localStorage.setItem(`${name}_${widgetId}`, value)
  if (toNumber)
    set(Number(value))
  else
    set(value)
}
