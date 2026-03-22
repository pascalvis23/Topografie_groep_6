import { useState } from 'react'
import { weetjesPerLes } from '../data/weetjes'

export default function WeetjesPanel({ les }) {
  const [zoek, setZoek] = useState('')
  const [actief, setActief] = useState(null)

  const weetjes = weetjesPerLes[les.id] || {}
  const steden  = les.plaatsen.filter(p => p.type === 'stad')

  const gefilterd = steden.filter(p =>
    weetjes[p.naam] &&
    p.naam.toLowerCase().includes(zoek.toLowerCase())
  )

  return (
    <div style={{ fontFamily: 'Arial, sans-serif' }}>

      {/* Header */}
      <div style={{
        background: '#1a237e', color: 'white',
        borderRadius: '10px 10px 0 0', padding: '14px 18px',
        display: 'flex', alignItems: 'center', gap: 10
      }}>
        <span style={{ fontSize: 22 }}>💡</span>
        <div>
          <div style={{ fontWeight: 700, fontSize: 16 }}>Weetjes over {les.titel}</div>
          <div style={{ fontSize: 12, opacity: 0.8 }}>{Object.keys(weetjes).length} plaatsen met een weetje</div>
        </div>
      </div>

      {/* Zoekbalk */}
      <div style={{
        background: '#E8EAF6', padding: '10px 14px',
        borderLeft: '1px solid #c5cae9', borderRight: '1px solid #c5cae9'
      }}>
        <input
          value={zoek}
          onChange={e => { setZoek(e.target.value); setActief(null) }}
          placeholder="Zoek een plaats..."
          style={{
            width: '100%', padding: '8px 12px', fontSize: 14,
            border: '1px solid #9FA8DA', borderRadius: 8,
            outline: 'none', boxSizing: 'border-box', fontFamily: 'Arial, sans-serif'
          }}
        />
      </div>

      {/* Kaarten */}
      <div style={{
        border: '1px solid #c5cae9', borderTop: 'none',
        borderRadius: '0 0 10px 10px',
        maxHeight: '72vh', overflowY: 'auto',
        background: '#fafbff'
      }}>
        {gefilterd.length === 0 && (
          <div style={{ padding: 24, textAlign: 'center', color: '#9FA8DA', fontSize: 14 }}>
            Geen plaatsen gevonden
          </div>
        )}

        {gefilterd.map(p => {
          const w = weetjes[p.naam]
          const isOpen = actief === p.naam
          return (
            <div
              key={p.naam}
              onClick={() => setActief(isOpen ? null : p.naam)}
              style={{
                borderBottom: '1px solid #e8eaf6',
                cursor: 'pointer',
                background: isOpen ? '#E8EAF6' : 'white',
                transition: 'background 0.15s',
              }}
            >
              {/* Titel-rij */}
              <div style={{
                display: 'flex', alignItems: 'center', gap: 10,
                padding: '11px 14px',
              }}>
                <span style={{ fontSize: 20, flexShrink: 0 }}>{w.emoji}</span>
                <span style={{
                  fontWeight: 700, fontSize: 14, color: '#1a237e', flex: 1
                }}>
                  {p.naam}
                </span>
                <span style={{
                  fontSize: 12, color: '#9FA8DA', flexShrink: 0,
                  transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.2s', display: 'inline-block'
                }}>▼</span>
              </div>

              {/* Uitklapbaar weetje */}
              {isOpen && (
                <div style={{
                  padding: '0 14px 14px 44px',
                  fontSize: 13, lineHeight: 1.6, color: '#333',
                }}>
                  {w.feit}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Footer hint */}
      <div style={{ marginTop: 8, fontSize: 12, color: '#9FA8DA', textAlign: 'center' }}>
        Klik op een plaatsnaam om het weetje te lezen
      </div>
    </div>
  )
}
