import { useState, useRef } from 'react'
import { lessen } from '../data/provinces'

export default function KalibratieTool() {
  const [activeLesId, setActiveLesId] = useState(1)
  const [activePlaatsIndex, setActivePlaatsIndex] = useState(0)
  const [coords, setCoords] = useState({}) // { lesId: { plaatsNaam: {x, y} } }
  const [modus, setModus] = useState('namen') // 'namen' | 'blanco'
  const [hoverPos, setHoverPos] = useState(null)
  const imgRef = useRef(null)

  const les = lessen.find(l => l.id === activeLesId)
  const steden = les.plaatsen.filter(p => p.type === 'stad')
  const activePlaats = steden[activePlaatsIndex]

  const handleImgKlik = (e) => {
    const rect = imgRef.current.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(1)
    const y = ((e.clientY - rect.top) / rect.height * 100).toFixed(1)

    setCoords(prev => ({
      ...prev,
      [activeLesId]: {
        ...(prev[activeLesId] || {}),
        [activePlaats.naam]: { x: parseFloat(x), y: parseFloat(y) }
      }
    }))

    // Ga automatisch naar volgende stad
    if (activePlaatsIndex < steden.length - 1) {
      setActivePlaatsIndex(activePlaatsIndex + 1)
    }
  }

  const handleImgHover = (e) => {
    const rect = imgRef.current.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(1)
    const y = ((e.clientY - rect.top) / rect.height * 100).toFixed(1)
    setHoverPos({ x, y })
  }

  const genereerCode = () => {
    let output = '// Gedetecteerde coördinaten — kopieer naar provinces.js\n\n'
    lessen.forEach(les => {
      const lesCoords = coords[les.id] || {}
      output += `// Les ${les.id}: ${les.titel}\n`
      les.plaatsen.forEach(p => {
        if (p.type === 'stad') {
          const c = lesCoords[p.naam]
          if (c) {
            output += `{ naam: "${p.naam}", x: ${c.x}, y: ${c.y}, type: "stad" },\n`
          } else {
            output += `// NIET INGESTELD: ${p.naam}\n`
          }
        }
      })
      output += '\n'
    })
    return output
  }

  const lesCoords = coords[activeLesId] || {}
  const aantalIngesteld = steden.filter(p => lesCoords[p.naam]).length

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial, sans-serif', background: '#1a237e' }}>

      {/* Linker paneel */}
      <div style={{ width: 280, background: '#0d1a6e', color: 'white', padding: 16, overflowY: 'auto', flexShrink: 0 }}>
        <div style={{ fontWeight: 900, fontSize: 16, marginBottom: 12 }}>🎯 Kalibratietool</div>

        {/* Les selectie */}
        <div style={{ marginBottom: 16 }}>
          <div style={{ fontSize: 12, opacity: 0.7, marginBottom: 6 }}>Kies een les:</div>
          {lessen.map(l => {
            const lc = coords[l.id] || {}
            const st = l.plaatsen.filter(p => p.type === 'stad')
            const ingst = st.filter(p => lc[p.naam]).length
            return (
              <div key={l.id}
                onClick={() => { setActiveLesId(l.id); setActivePlaatsIndex(0) }}
                style={{
                  padding: '6px 10px', borderRadius: 6, cursor: 'pointer', marginBottom: 4,
                  background: activeLesId === l.id ? l.kleur : 'rgba(255,255,255,0.1)',
                  fontSize: 13, display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                }}>
                <span>{l.id}. {l.titel}</span>
                <span style={{ fontSize: 11, opacity: 0.8 }}>{ingst}/{st.length}</span>
              </div>
            )
          })}
        </div>

        {/* Steden lijst */}
        <div style={{ fontSize: 12, opacity: 0.7, marginBottom: 6 }}>
          Steden ({aantalIngesteld}/{steden.length} ingesteld):
        </div>
        {steden.map((p, i) => {
          const c = lesCoords[p.naam]
          return (
            <div key={p.naam}
              onClick={() => setActivePlaatsIndex(i)}
              style={{
                padding: '5px 8px', borderRadius: 5, cursor: 'pointer', marginBottom: 2,
                background: i === activePlaatsIndex
                  ? 'rgba(255,255,255,0.3)'
                  : c ? 'rgba(76,175,80,0.3)' : 'rgba(255,255,255,0.05)',
                fontSize: 12, display: 'flex', justifyContent: 'space-between'
              }}>
              <span style={{ fontWeight: i === activePlaatsIndex ? 700 : 400 }}>
                {i === activePlaatsIndex ? '→ ' : ''}{p.naam}
              </span>
              {c && <span style={{ opacity: 0.7 }}>✓ {c.x},{c.y}</span>}
            </div>
          )
        })}
      </div>

      {/* Midden: kaart */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>

        {/* Toolbar */}
        <div style={{
          background: '#283593', color: 'white', padding: '10px 16px',
          display: 'flex', alignItems: 'center', gap: 12
        }}>
          <div style={{ fontWeight: 700 }}>Les {les.id}: {les.titel}</div>
          <div style={{
            marginLeft: 8, background: '#FFD600', color: '#1a237e',
            borderRadius: 8, padding: '4px 12px', fontWeight: 700, fontSize: 14
          }}>
            Klik op: {activePlaats?.naam}
          </div>
          <div style={{ display: 'flex', gap: 6, marginLeft: 'auto' }}>
            {['namen', 'blanco'].map(m => (
              <button key={m} onClick={() => setModus(m)}
                style={{
                  padding: '5px 12px', borderRadius: 6, border: 'none', cursor: 'pointer',
                  background: modus === m ? 'white' : 'rgba(255,255,255,0.2)',
                  color: modus === m ? '#1a237e' : 'white',
                  fontWeight: 600, fontSize: 12
                }}>
                {m === 'namen' ? '📖 Met namen' : '⚫ Blanco'}
              </button>
            ))}
          </div>
          {hoverPos && (
            <div style={{ fontSize: 12, opacity: 0.8, fontFamily: 'monospace' }}>
              x={hoverPos.x}% y={hoverPos.y}%
            </div>
          )}
        </div>

        {/* Kaart */}
        <div style={{ flex: 1, overflow: 'auto', background: '#0d1a6e', display: 'flex', justifyContent: 'center', alignItems: 'flex-start', padding: 16 }}>
          <div style={{ position: 'relative', display: 'inline-block' }}>
            <img
              ref={imgRef}
              src={modus === 'namen' ? les.afbeeldingNamen : les.afbeeldingBlanco}
              alt="Kaart"
              onClick={handleImgKlik}
              onMouseMove={handleImgHover}
              style={{
                maxHeight: 'calc(100vh - 80px)', maxWidth: '100%',
                cursor: 'crosshair', display: 'block',
                border: '3px solid #FFD600'
              }}
            />

            {/* Toon al ingestelde coördinaten */}
            {steden.map((p, i) => {
              const c = lesCoords[p.naam]
              if (!c) return null
              return (
                <div key={p.naam} style={{
                  position: 'absolute',
                  left: `${c.x}%`, top: `${c.y}%`,
                  transform: 'translate(-50%, -50%)',
                  pointerEvents: 'none'
                }}>
                  <div style={{
                    width: 12, height: 12,
                    background: i === activePlaatsIndex ? '#FFD600' : '#4CAF50',
                    borderRadius: '50%', border: '2px solid white',
                    boxShadow: '0 0 4px rgba(0,0,0,0.5)'
                  }} />
                  <div style={{
                    position: 'absolute', top: 14, left: '50%',
                    transform: 'translateX(-50%)',
                    background: 'rgba(0,0,0,0.7)', color: 'white',
                    fontSize: 9, padding: '1px 4px', borderRadius: 3,
                    whiteSpace: 'nowrap', fontWeight: 700
                  }}>
                    {p.naam}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Rechter paneel: code output */}
      <div style={{ width: 300, background: '#0d1a6e', color: '#a5d6a7', padding: 16, overflowY: 'auto', flexShrink: 0 }}>
        <div style={{ fontWeight: 700, color: 'white', marginBottom: 8, fontSize: 13 }}>
          📋 Gegenereerde code:
        </div>
        <button
          onClick={() => navigator.clipboard.writeText(genereerCode())}
          style={{
            width: '100%', padding: '8px', background: '#4CAF50',
            color: 'white', border: 'none', borderRadius: 6,
            fontWeight: 700, cursor: 'pointer', marginBottom: 8, fontSize: 12
          }}>
          📋 Kopieer naar klembord
        </button>
        <pre style={{
          fontSize: 10, lineHeight: 1.4, margin: 0,
          fontFamily: 'Consolas, monospace',
          whiteSpace: 'pre-wrap', wordBreak: 'break-all'
        }}>
          {genereerCode()}
        </pre>
      </div>
    </div>
  )
}
