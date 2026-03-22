import { useState, useRef, useEffect, useCallback } from 'react'

const STORAGE_KEY = (lesId) => `geobas_pos_les${lesId}`

const TYPE_STIJL = {
  stad:   { kleur: '#d32f2f', tekst: 'white',   label: 'Stad'   },
  eiland: { kleur: '#6a1b9a', tekst: 'white',   label: 'Eiland' },
  water:  { kleur: '#1565C0', tekst: 'white',   label: 'Water'  },
  streek: { kleur: '#2e7d32', tekst: 'white',   label: 'Streek' },
}

function laadOverrides(lesId) {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY(lesId)) || '{}') }
  catch { return {} }
}
function slaOverridesOp(lesId, data) {
  localStorage.setItem(STORAGE_KEY(lesId), JSON.stringify(data))
}

export function useOverrides(lesId) {
  const [overrides, setOverrides] = useState(() => laadOverrides(lesId))
  useEffect(() => { setOverrides(laadOverrides(lesId)) }, [lesId])
  return overrides
}

export default function BewerkenTab({ les }) {
  const [overrides, setOverrides] = useState(() => laadOverrides(les.id))
  const [geselecteerd, setGeselecteerd] = useState(null)
  const [sleepInfo, setSleepInfo]       = useState(null) // { naam, startX, startY, origX, origY }
  const [gekopieerd, setGekopieerd]     = useState(false)
  const [filterType, setFilterType]     = useState('alle')
  const kaartRef = useRef(null)

  // Merge provinces.js posities met overrides
  const items = les.plaatsen.map(p => ({
    ...p,
    x: overrides[p.naam]?.x ?? p.x,
    y: overrides[p.naam]?.y ?? p.y,
    aangepast: !!overrides[p.naam],
  }))

  const gefilterd = filterType === 'alle'
    ? items
    : items.filter(p => p.type === filterType)

  const updatePos = useCallback((naam, x, y) => {
    setOverrides(prev => {
      const nieuw = { ...prev, [naam]: { x: Math.round(x * 10) / 10, y: Math.round(y * 10) / 10 } }
      slaOverridesOp(les.id, nieuw)
      return nieuw
    })
  }, [les.id])

  const resetItem = (naam) => {
    setOverrides(prev => {
      const nieuw = { ...prev }
      delete nieuw[naam]
      slaOverridesOp(les.id, nieuw)
      return nieuw
    })
  }

  const resetAlles = () => {
    setOverrides({})
    slaOverridesOp(les.id, {})
  }

  // ── Slepen ────────────────────────────────────────────────────────────────
  const startSleep = (e, naam, huidigX, huidigY) => {
    e.preventDefault()
    e.stopPropagation()
    setGeselecteerd(naam)
    setSleepInfo({ naam, startMouseX: e.clientX, startMouseY: e.clientY, origX: huidigX, origY: huidigY })
  }

  useEffect(() => {
    if (!sleepInfo) return
    const onMove = (e) => {
      const rect = kaartRef.current?.getBoundingClientRect()
      if (!rect) return
      const dx = (e.clientX - sleepInfo.startMouseX) / rect.width  * 100
      const dy = (e.clientY - sleepInfo.startMouseY) / rect.height * 100
      const nx = Math.max(0, Math.min(100, sleepInfo.origX + dx))
      const ny = Math.max(0, Math.min(100, sleepInfo.origY + dy))
      updatePos(sleepInfo.naam, nx, ny)
    }
    const onUp = () => setSleepInfo(null)
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseup', onUp)
    return () => {
      window.removeEventListener('mousemove', onMove)
      window.removeEventListener('mouseup', onUp)
    }
  }, [sleepInfo, updatePos])

  // Klik op kaart → positie instellen voor geselecteerd item
  const handleKaartKlik = (e) => {
    if (sleepInfo || !geselecteerd) return
    const rect = kaartRef.current.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width)  * 100
    const y = ((e.clientY - rect.top)  / rect.height) * 100
    updatePos(geselecteerd, x, y)
  }

  // ── Export Python ─────────────────────────────────────────────────────────
  const exporteer = () => {
    if (Object.keys(overrides).length === 0) {
      alert('Geen aanpassingen om te exporteren.')
      return
    }
    const regels = Object.entries(overrides)
      .map(([naam, pos]) => `        "${naam}": (${pos.x}, ${pos.y}),`)
      .join('\n')
    const code = `# Overrides voor Les ${les.id} — ${les.titel}\n# Voeg toe aan LESSEN in generate_maps.py als extra veld "overrides":\n"overrides": {\n${regels}\n}`
    navigator.clipboard.writeText(code).then(() => {
      setGekopieerd(true)
      setTimeout(() => setGekopieerd(false), 2500)
    })
  }

  const gesItem = items.find(p => p.naam === geselecteerd)

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 20, alignItems: 'start', fontFamily: 'Arial, sans-serif' }}>

      {/* ── Kaart ── */}
      <div>
        <div style={{
          background: '#1a237e', color: 'white', borderRadius: '8px 8px 0 0',
          padding: '8px 14px', fontSize: 13, display: 'flex', alignItems: 'center', gap: 8
        }}>
          <span style={{ fontWeight: 700 }}>🔧 Sleepeditor</span>
          <span style={{ opacity: 0.75 }}>
            {geselecteerd
              ? `Geselecteerd: ${geselecteerd} — sleep de stip of klik op de kaart`
              : 'Selecteer een item uit de lijst, sleep het daarna naar de juiste plek'}
          </span>
        </div>

        <div
          ref={kaartRef}
          onClick={handleKaartKlik}
          style={{
            position: 'relative', border: '2px solid #1a237e', borderTop: 'none',
            borderRadius: '0 0 8px 8px', overflow: 'hidden', background: '#fff',
            cursor: geselecteerd ? 'crosshair' : 'default',
            userSelect: 'none',
          }}
        >
          <img
            src={les.afbeeldingBlanco}
            alt="blanco kaart"
            style={{ width: '100%', display: 'block' }}
            draggable={false}
          />

          {/* Alle items als sleepbare stippen/labels */}
          {items.map((p) => {
            const stijl = TYPE_STIJL[p.type] || TYPE_STIJL.stad
            const isGeselecteerd = geselecteerd === p.naam
            const toonLabel = p.type !== 'stad' && p.type !== 'eiland'

            return (
              <div
                key={p.naam}
                onMouseDown={(e) => startSleep(e, p.naam, p.x, p.y)}
                onClick={(e) => { e.stopPropagation(); setGeselecteerd(p.naam) }}
                style={{
                  position: 'absolute',
                  left: `${p.x}%`, top: `${p.y}%`,
                  transform: 'translate(-50%, -50%)',
                  cursor: 'grab',
                  zIndex: isGeselecteerd ? 30 : (toonLabel ? 10 : 8),
                }}
              >
                {toonLabel ? (
                  /* Water / streek: tekst-label */
                  <div style={{
                    padding: '2px 6px', fontSize: 10, fontWeight: 700,
                    fontStyle: p.type === 'water' ? 'italic' : 'normal',
                    background: stijl.kleur,
                    color: stijl.tekst,
                    borderRadius: 4,
                    boxShadow: isGeselecteerd
                      ? `0 0 0 2px white, 0 0 0 4px ${stijl.kleur}`
                      : '0 1px 3px rgba(0,0,0,0.4)',
                    whiteSpace: 'nowrap',
                    opacity: p.aangepast ? 1 : 0.70,
                  }}>
                    {p.naam}
                  </div>
                ) : (
                  /* Stad / eiland: stip */
                  <div style={{
                    width: isGeselecteerd ? 14 : 10,
                    height: isGeselecteerd ? 14 : 10,
                    borderRadius: '50%',
                    background: stijl.kleur,
                    border: '2px solid white',
                    boxShadow: isGeselecteerd
                      ? `0 0 0 2px ${stijl.kleur}, 0 2px 6px rgba(0,0,0,0.4)`
                      : '0 1px 3px rgba(0,0,0,0.35)',
                  }} />
                )}
              </div>
            )
          })}
        </div>

        {/* Legenda */}
        <div style={{ display: 'flex', gap: 12, padding: '6px 0', flexWrap: 'wrap', fontSize: 12 }}>
          {Object.entries(TYPE_STIJL).map(([t, s]) => (
            <span key={t} style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#555' }}>
              <span style={{ width: 10, height: 10, borderRadius: t === 'stad' || t === 'eiland' ? '50%' : 3, background: s.kleur, display: 'inline-block' }} />
              {s.label}
            </span>
          ))}
          <span style={{ color: '#9e9e9e' }}>◻ = origineel (transparant) · ■ = aangepast</span>
        </div>
      </div>

      {/* ── Zijpaneel ── */}
      <div style={{ position: 'sticky', top: 20 }}>

        {/* Geselecteerd item detail */}
        {gesItem && (
          <div style={{
            background: '#E8EAF6', borderRadius: 10, padding: 14, marginBottom: 12,
            border: `2px solid ${TYPE_STIJL[gesItem.type]?.kleur || '#1a237e'}`
          }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: '#1a237e', marginBottom: 8 }}>
              {TYPE_STIJL[gesItem.type]?.label}: {gesItem.naam}
              {gesItem.aangepast && <span style={{ marginLeft: 6, fontSize: 11, background: '#1a237e', color: 'white', borderRadius: 4, padding: '1px 5px' }}>aangepast</span>}
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
              {['x', 'y'].map(as => (
                <label key={as} style={{ fontSize: 12 }}>
                  <div style={{ color: '#555', marginBottom: 2 }}>{as === 'x' ? 'Links → Rechts (%)' : 'Boven → Onder (%)'}</div>
                  <input
                    type="number" min="0" max="100" step="0.5"
                    value={gesItem[as]}
                    onChange={e => {
                      const v = parseFloat(e.target.value)
                      if (!isNaN(v)) updatePos(gesItem.naam, as === 'x' ? v : gesItem.x, as === 'y' ? v : gesItem.y)
                    }}
                    style={{
                      width: '100%', padding: '6px 8px', fontSize: 13,
                      border: '1px solid #9FA8DA', borderRadius: 6,
                      boxSizing: 'border-box', fontFamily: 'Arial',
                    }}
                  />
                </label>
              ))}
            </div>
            {gesItem.aangepast && (
              <button onClick={() => { resetItem(gesItem.naam); setGeselecteerd(null) }}
                style={{ marginTop: 8, padding: '5px 10px', fontSize: 12, background: '#FFEBEE',
                  color: '#C62828', border: '1px solid #EF9A9A', borderRadius: 6, cursor: 'pointer' }}>
                ↩ Reset naar origineel
              </button>
            )}
          </div>
        )}

        {/* Filter + lijst */}
        <div style={{ background: 'white', borderRadius: 10, border: '1px solid #c5cae9', overflow: 'hidden' }}>
          <div style={{ background: '#E8EAF6', padding: '8px 12px', display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            {['alle', 'water', 'streek', 'stad', 'eiland'].map(t => (
              <button key={t} onClick={() => setFilterType(t)}
                style={{
                  padding: '3px 9px', borderRadius: 12, border: 'none', cursor: 'pointer',
                  fontSize: 12, fontWeight: 600,
                  background: filterType === t ? '#1a237e' : 'white',
                  color: filterType === t ? 'white' : '#555',
                }}>
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>

          <div style={{ maxHeight: 340, overflowY: 'auto' }}>
            {gefilterd.map(p => {
              const stijl = TYPE_STIJL[p.type] || TYPE_STIJL.stad
              const isGes = geselecteerd === p.naam
              return (
                <div key={p.naam} onClick={() => setGeselecteerd(p.naam)}
                  style={{
                    padding: '8px 12px', cursor: 'pointer', borderBottom: '1px solid #f0f0f0',
                    background: isGes ? '#E8EAF6' : 'white',
                    display: 'flex', alignItems: 'center', gap: 8,
                  }}>
                  <span style={{
                    width: 8, height: 8, borderRadius: p.type === 'stad' || p.type === 'eiland' ? '50%' : 2,
                    background: stijl.kleur, flexShrink: 0,
                  }} />
                  <span style={{ fontSize: 13, flex: 1, fontWeight: isGes ? 700 : 400 }}>{p.naam}</span>
                  {p.aangepast && <span style={{ fontSize: 10, color: '#1a237e', fontWeight: 700 }}>✎</span>}
                  <span style={{ fontSize: 11, color: '#999' }}>{p.x},{p.y}</span>
                </div>
              )
            })}
          </div>
        </div>

        {/* Actieknoppen */}
        <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 8 }}>
          <button onClick={exporteer} style={{
            padding: '10px', background: gekopieerd ? '#4CAF50' : '#1a237e', color: 'white',
            border: 'none', borderRadius: 8, fontSize: 14, fontWeight: 700, cursor: 'pointer',
          }}>
            {gekopieerd ? '✓ Gekopieerd naar klembord!' : '📋 Exporteer Python-code'}
          </button>
          {Object.keys(overrides).length > 0 && (
            <button onClick={resetAlles} style={{
              padding: '8px', background: '#FFEBEE', color: '#C62828',
              border: '1px solid #EF9A9A', borderRadius: 8, fontSize: 13, cursor: 'pointer',
            }}>
              ↩ Reset alle aanpassingen ({Object.keys(overrides).length})
            </button>
          )}
        </div>

        <div style={{ marginTop: 8, fontSize: 11, color: '#9e9e9e', lineHeight: 1.5 }}>
          Aanpassingen worden lokaal opgeslagen.<br />
          Exporteer de Python-code en plak die in generate_maps.py om de kaartafbeeldingen te updaten.
        </div>
      </div>
    </div>
  )
}
