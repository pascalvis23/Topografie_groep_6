import { useState } from 'react'

const typeKleur = {
  stad:   '#d32f2f',
  water:  '#1565C0',
  streek: '#2e7d32',
  eiland: '#6a1b9a',
}

export default function MapView({ les, modus, onPlaatsKlik, actiefPlaats }) {
  const [hover, setHover] = useState(null)

  const afbeelding = modus === 'studeren'
    ? les.afbeeldingNamen
    : les.afbeeldingBlanco

  const steden = les.plaatsen.filter(p => p.type === 'stad' || p.type === 'eiland')

  return (
    <div style={{ position: 'relative', display: 'inline-block', width: '100%', maxWidth: 900 }}>
      {/* Header */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 10,
        background: '#1a237e', color: 'white',
        padding: '8px 14px', borderRadius: '8px 8px 0 0',
        fontSize: 15, fontWeight: 700, fontFamily: 'Arial, sans-serif'
      }}>
        <span style={{
          background: 'white', color: '#1a237e',
          borderRadius: 4, padding: '2px 8px', fontWeight: 900, fontSize: 16
        }}>{les.id}</span>
        <span>{modus === 'studeren' ? 'Topografiekaart met namen' : 'Topografiekaart'}</span>
        <span style={{ marginLeft: 'auto', fontSize: 13, fontWeight: 400 }}>{les.titel}</span>
      </div>

      {/* Kaart */}
      <div style={{
        position: 'relative',
        border: '2px solid #1a237e', borderTop: 'none',
        borderRadius: '0 0 8px 8px', overflow: 'hidden', background: '#fff'
      }}>
        <img
          src={afbeelding}
          alt={`Kaart van ${les.titel}`}
          style={{ width: '100%', display: 'block', userSelect: 'none' }}
          draggable={false}
        />

        {/* Stippen overlay */}
        {steden.map((plaats, i) => {
          const isActief  = actiefPlaats?.naam === plaats.naam
          const isHover   = hover === i
          const isQuiz    = modus !== 'studeren'

          // Studiemodus: kleine gekleurde stip + tooltip
          // Quizmodus:   grotere klikbare stip
          const dotSize = isQuiz
            ? (isHover ? 16 : 12)
            : (isHover ? 12 : 8)

          const dotKleur = isActief
            ? '#FFD600'
            : isQuiz
              ? (isHover ? '#FFD600' : typeKleur[plaats.type])
              : (isHover ? typeKleur[plaats.type] : typeKleur[plaats.type])

          const dotOpacity = modus === 'studeren' ? 0.85 : 1

          return (
            <div
              key={i}
              onClick={() => isQuiz && onPlaatsKlik && onPlaatsKlik(plaats)}
              onMouseEnter={() => setHover(i)}
              onMouseLeave={() => setHover(null)}
              style={{
                position: 'absolute',
                left: `${plaats.x}%`,
                top: `${plaats.y}%`,
                transform: 'translate(-50%, -50%)',
                cursor: isQuiz ? 'pointer' : 'default',
                zIndex: isHover || isActief ? 20 : 5,
              }}
            >
              {/* De stip zelf */}
              <div style={{
                width: dotSize,
                height: dotSize,
                background: dotKleur,
                borderRadius: '50%',
                border: `2px solid ${modus === 'studeren' ? 'rgba(255,255,255,0.9)' : 'white'}`,
                boxShadow: isHover || isActief
                  ? `0 0 0 3px ${dotKleur}66, 0 2px 6px rgba(0,0,0,0.4)`
                  : '0 1px 3px rgba(0,0,0,0.35)',
                transition: 'all 0.15s',
                opacity: dotOpacity,
              }} />

              {/* Tooltip: alleen in studiemodus bij hover — in quizmodus nooit naam tonen */}
              {isHover && !isQuiz && (
                <div style={{
                  position: 'absolute',
                  bottom: dotSize + 6,
                  left: '50%',
                  transform: 'translateX(-50%)',
                  background: 'rgba(26,35,126,0.93)',
                  color: 'white',
                  padding: '3px 8px',
                  borderRadius: 5,
                  fontSize: 12,
                  fontFamily: 'Arial, sans-serif',
                  fontWeight: 700,
                  whiteSpace: 'nowrap',
                  pointerEvents: 'none',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
                }}>
                  {plaats.naam}
                  {/* klein pijltje */}
                  <div style={{
                    position: 'absolute',
                    top: '100%', left: '50%',
                    transform: 'translateX(-50%)',
                    border: '5px solid transparent',
                    borderTopColor: 'rgba(26,35,126,0.93)',
                  }} />
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Legenda (alleen studiemodus) */}
      {modus === 'studeren' && (
        <div style={{
          display: 'flex', gap: 14, padding: '6px 12px',
          background: '#f5f5f5', borderRadius: '0 0 8px 8px',
          borderTop: '1px solid #ddd', flexWrap: 'wrap',
          fontSize: 11, fontFamily: 'Arial, sans-serif'
        }}>
          <span style={{ color: '#555', fontSize: 11 }}>Beweeg over een stip voor de naam</span>
          {Object.entries(typeKleur).filter(([t]) => les.plaatsen.some(p => p.type === t)).map(([type, kleur]) => (
            <span key={type} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <span style={{
                display: 'inline-block', width: 9, height: 9,
                background: kleur, borderRadius: '50%',
                border: '1.5px solid white', boxShadow: '0 1px 2px rgba(0,0,0,0.25)'
              }} />
              <span style={{ color: '#555' }}>{type}</span>
            </span>
          ))}
        </div>
      )}
    </div>
  )
}
