import Header from '../components/header'
import Cell from '../components/cell'
import { useState, useEffect, useRef } from 'react'
import { GRID, GRID_URLS } from '../config'

import './dashboard.css'

const SIZE_OPTIONS = [1, 2, 3].flatMap(width => [1, 2, 3].map(height => ({ width, height })))
const DEFAULT_SIZE = { width: 1, height: 1 }
const WIDGET_NAMES = new Set([
  'discord_profile', 'discord_banner', 'steam_profile', 'steam_currentgame', 'steam_lastgame', 'forecast', 'air_quality',
])

function createWidgetId() {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`
}

function normalizeSize(size) {
  const width = Number(size?.width)
  const height = Number(size?.height)
  if (!Number.isInteger(width) || width < 1 || width > 3 || !Number.isInteger(height) || height < 1 || height > 3)
    return DEFAULT_SIZE
  return { width, height }
}

function normalizeGridShape(shape) {
  const columns = Number(shape?.columns)
  const rows = Number(shape?.rows)
  return {
    columns: Number.isInteger(columns) && columns >= 1 && columns <= GRID.columns ? columns : GRID.columns,
    rows: Number.isInteger(rows) && rows >= 1 && rows <= GRID.rows ? rows : GRID.rows,
  }
}

function gridStateFromResponse(grid) {
  const gridShape = normalizeGridShape(grid)
  const cells = Array(GRID.columns * GRID.rows).fill(null)
  const sizes = Array.from({ length: cells.length }, () => DEFAULT_SIZE)

  for (const cell of grid.cells || []) {
    const index = cell.y * gridShape.columns + cell.x
    if (!Number.isInteger(index) || index < 0 || index >= cells.length ||
      !WIDGET_NAMES.has(cell.widget_type) || cells[index])
      continue
    cells[index] = { id: String(cell.widget_id), name: cell.widget_type }
    sizes[index] = normalizeSize({ width: cell.width, height: cell.height })
  }
  return { cells, sizes, gridShape }
}

function overlaps(index, size, otherIndex, otherSize, columns) {
  const left = index % columns
  const top = Math.floor(index / columns)
  const otherLeft = otherIndex % columns
  const otherTop = Math.floor(otherIndex / columns)
  return left < otherLeft + otherSize.width && left + size.width > otherLeft &&
    top < otherTop + otherSize.height && top + size.height > otherTop
}

function buildLayout(cells, sizes, columns) {
  const rows = Math.ceil(cells.length / columns)
  const covered = Array(cells.length).fill(false)
  const effectiveSizes = sizes.map(normalizeSize)
  const widgets = []

  for (let index = 0; index < cells.length; index += 1) {
    if (!cells[index])
      continue

    const column = index % columns
    const row = Math.floor(index / columns)
    let size = effectiveSizes[index]
    const outOfBounds = column + size.width > columns || row + size.height > rows
    const overlapsExisting = widgets.some(widget => overlaps(index, size, widget.index, widget.size, columns))
    const coversWidget = cells.some((name, otherIndex) => otherIndex !== index && name && overlaps(index, size, otherIndex, DEFAULT_SIZE, columns))

    if (outOfBounds || overlapsExisting || coversWidget)
      size = DEFAULT_SIZE
    effectiveSizes[index] = size
    widgets.push({ index, size })

    for (let rowOffset = 0; rowOffset < size.height; rowOffset += 1) {
      for (let columnOffset = 0; columnOffset < size.width; columnOffset += 1) {
        const coveredIndex = (row + rowOffset) * columns + column + columnOffset
        if (coveredIndex < covered.length)
          covered[coveredIndex] = true
      }
    }
  }

  const placements = widgets.map(({ index, size }) => ({ index, size }))
  for (let index = 0; index < cells.length; index += 1) {
    if (!covered[index])
      placements.push({ index, size: DEFAULT_SIZE })
  }

  return { placements, effectiveSizes, columns, rows }
}

function sameSize(first, second) {
  return first.width === second.width && first.height === second.height
}

function Dashboard({ isVisitor, onSignIn, onLogout }) {
  const [cells, setCells] = useState(() => Array(GRID.columns * GRID.rows).fill(null))
  const [sizes, setSizes] = useState(() => Array.from({ length: GRID.columns * GRID.rows }, () => DEFAULT_SIZE))
  const [gridShape, setGridShape] = useState(GRID)
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [gridReady, setGridReady] = useState(false)
  const [gridLoadError, setGridLoadError] = useState('')
  const [gridLoadAttempt, setGridLoadAttempt] = useState(0)
  const [gridSaveError, setGridSaveError] = useState('')
  const saveQueue = useRef(Promise.resolve())

  useEffect(() => {
    if (isVisitor) {
      return
    }

    const token = localStorage.getItem('access_token')
    let isCurrent = true
    fetch(GRID_URLS.current, { headers: { Authorization: 'Bearer ' + token } })
      .then(async response => {
        if (!response.ok)
          throw new Error(`Unable to load your dashboard (HTTP ${response.status}).`)
        return response.json()
      })
      .then(grid => {
        if (!isCurrent)
          return
        const state = gridStateFromResponse(grid)
        setCells(state.cells)
        setSizes(state.sizes)
        setGridShape(state.gridShape)
        setGridReady(true)
      })
      .catch(error => {
        if (isCurrent)
          setGridLoadError(error.message || 'Unable to load your dashboard.')
      })

    return () => { isCurrent = false }
  }, [isVisitor, gridLoadAttempt])

  useEffect(() => {
    if (isVisitor || !gridReady)
      return
    const token = localStorage.getItem('access_token')
    if (!token)
      return

    const timeout = setTimeout(() => {
      const visibleCount = gridShape.columns * gridShape.rows
      const savedLayout = buildLayout(cells.slice(0, visibleCount), sizes.slice(0, visibleCount), gridShape.columns)
      const payload = {
        ...gridShape,
        cells: cells.flatMap((cell, index) => {
          if (!cell)
            return []
          const size = normalizeSize(index < visibleCount
            ? savedLayout.effectiveSizes[index]
            : sizes[index])
          return [{
            widget_type: cell.name,
            widget_id: cell.id,
            x: index % gridShape.columns,
            y: Math.floor(index / gridShape.columns),
            width: size.width,
            height: size.height,
          }]
        }),
      }

      saveQueue.current = saveQueue.current.then(async () => {
        const response = await fetch(GRID_URLS.current, {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        })
        if (!response.ok)
          throw new Error(`Unable to save your dashboard (HTTP ${response.status}).`)
        setGridSaveError('')
      }).catch(error => {
        setGridSaveError(error.message || 'Unable to save your dashboard.')
      })
    }, 300)

    return () => clearTimeout(timeout)
  }, [cells, sizes, gridShape, gridReady, isVisitor])

  if (!isVisitor && !gridReady)
    return (
      <main className="grid_loading" role={gridLoadError ? 'alert' : 'status'}>
        {gridLoadError ? (
          <>
            <p>{gridLoadError}</p>
            <button
              type="button"
              onClick={() => {
                setGridReady(false)
                setGridLoadError('')
                setGridLoadAttempt(attempt => attempt + 1)
              }}
            >
              Retry
            </button>
          </>
        ) : 'Loading your dashboard…'}
      </main>
    )

  const visibleCellCount = gridShape.columns * gridShape.rows
  const visibleCells = cells.slice(0, visibleCellCount)
  const visibleSizes = sizes.slice(0, visibleCellCount)
  const layout = buildLayout(visibleCells, visibleSizes, gridShape.columns)

  function handleDrop(event, index) {
    event.preventDefault()
    const name = event.dataTransfer.getData('text')
    const rawFrom = event.dataTransfer.getData('from')
    const widgetId = event.dataTransfer.getData('widgetId')
    const from = rawFrom === '' ? null : Number(rawFrom)
    if (!WIDGET_NAMES.has(name) || (from !== null && (!Number.isInteger(from) || from === index ||
      from < 0 || from >= visibleCellCount || cells[from]?.name !== name || cells[from]?.id !== widgetId)))
      return
    if (from === null && cells[index])
      return

    const nextCells = [...cells]
    const nextSizes = sizes.map(normalizeSize)
    const draggedCell = from === null ? { id: createWidgetId(), name } : nextCells[from]
    const draggedSize = from === null ? DEFAULT_SIZE : layout.effectiveSizes[from]

    if (from !== null) {
      const targetCell = nextCells[index]
      const targetSize = targetCell ? layout.effectiveSizes[index] : DEFAULT_SIZE
      nextCells[from] = targetCell || null
      nextCells[index] = draggedCell
      nextSizes[from] = targetSize
      nextSizes[index] = draggedSize
    } else {
      nextCells[index] = draggedCell
      nextSizes[index] = DEFAULT_SIZE
    }

    const nextLayout = buildLayout(nextCells.slice(0, visibleCellCount), nextSizes.slice(0, visibleCellCount), gridShape.columns)
    if (!sameSize(nextLayout.effectiveSizes[index], nextSizes[index]))
      return
    if (from !== null && nextCells[from] && !sameSize(nextLayout.effectiveSizes[from], nextSizes[from]))
      return

    setCells(nextCells)
    setSizes(nextSizes)
    if (from === null)
      setIsMenuOpen(false)
  }

  function addWidget(name) {
    if (!WIDGET_NAMES.has(name))
      return false
    const openSlot = layout.placements.find(({ index }) => !cells[index])
    if (!openSlot)
      return false
    const nextCells = [...cells]
    const nextSizes = sizes.map(normalizeSize)
    nextCells[openSlot.index] = { id: createWidgetId(), name }
    nextSizes[openSlot.index] = DEFAULT_SIZE
    setCells(nextCells)
    setSizes(nextSizes)
    setIsMenuOpen(false)
    return true
  }

  function handleSizeChange(index, size) {
    const nextSizes = sizes.map(normalizeSize)
    nextSizes[index] = size
    const nextLayout = buildLayout(visibleCells, nextSizes.slice(0, visibleCellCount), gridShape.columns)
    if (sameSize(nextLayout.effectiveSizes[index], size))
      setSizes(nextSizes)
  }

  function handleGridShapeChange(shape) {
    setGridShape(normalizeGridShape(shape))
  }

  return (
    <>
      <div className="lava-background dashboard-lava-background" aria-hidden="true">
        <span className="lava-orb orb-1" />
        <span className="lava-orb orb-2" />
        <span className="lava-orb orb-3" />
        <span className="lava-orb orb-4" />
      </div>
      <div className="app">
        {gridSaveError && <p className="grid_save_error" role="alert">{gridSaveError}</p>}
        <Header
          isMenuOpen={isMenuOpen}
          setIsMenuOpen={setIsMenuOpen}
          onWidgetSelect={addWidget}
          gridShape={gridShape}
          onGridShapeChange={handleGridShapeChange}
          isVisitor={isVisitor}
          onSignIn={onSignIn}
          onLogout={onLogout}
        />
        <main
          className="dashboard"
          style={{ '--columns': gridShape.columns, '--rows': gridShape.rows }}
        >
          {layout.placements.map(({ index, size }) => {
            const availableSizes = cells[index] ? SIZE_OPTIONS.filter(option => {
              const candidateSizes = visibleSizes.map(normalizeSize)
              candidateSizes[index] = option
              return sameSize(buildLayout(visibleCells, candidateSizes, gridShape.columns).effectiveSizes[index], option)
            }) : SIZE_OPTIONS

            return (
              <Cell
                key={cells[index] ? `widget:${cells[index].id}` : `cell:${index}`}
                index={index}
                name={cells[index]?.name}
                widgetId={cells[index]?.id}
                size={layout.effectiveSizes[index] || size}
                sizeOptions={availableSizes}
                style={{ gridColumn: `${index % gridShape.columns + 1} / span ${size.width}`, gridRow: `${Math.floor(index / gridShape.columns) + 1} / span ${size.height}` }}
                onDrop={handleDrop}
                onSizeChange={handleSizeChange}
                setCells={setCells}
              />
            )
          })}
        </main>
      </div>
    </>
  )
}

export default Dashboard
