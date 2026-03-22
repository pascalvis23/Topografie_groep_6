import { useState } from 'react'
import MapView from './MapView'
import QuizPanel from './QuizPanel'
import VoortgangBalk from './VoortgangBalk'
import WeetjesPanel from './WeetjesPanel'
import BewerkenTab from './BewerkenTab'
import MentimeterQuiz from './MentimeterQuiz'
import { useMobiel } from '../hooks/useMobiel'

export default function LesPage({ les, onTerug }) {
  const [modus, setModus] = useState('studeren') // 'studeren' | 'oefenen' | 'weetjes'
  const [aangeklikte, setAangeklikte] = useState(null)
  const [goedBeantwoord, setGoedBeantwoord] = useState(new Set())
  const mobiel = useMobiel()

  const steden = les.plaatsen.filter(p => p.type === 'stad')

  const handlePlaatsKlik = (plaats) => {
    if (modus === 'oefenen') setAangeklikte(plaats)
  }

  const handleGoedAntwoord = () => {
    if (aangeklikte) setGoedBeantwoord(prev => new Set([...prev, aangeklikte.naam]))
    setAangeklikte(null)
  }

  const TABS = mobiel
    ? [['studeren','📖'],['oefenen','✏️'],['quiz','🎮'],['weetjes','💡'],['bewerken','🔧']]
    : [['studeren','📖 Bestuderen'],['oefenen','✏️ Oefenen'],['quiz','🎮 Quiz'],['weetjes','💡 Weetjes'],['bewerken','🔧 Bewerken']]

  return (
    <div style={{ minHeight: '100vh', background: '#f0f2ff', fontFamily: 'Arial, sans-serif' }}>

      {/* Top navigatie */}
      <div style={{
        background: '#1a237e', color: 'white',
        padding: mobiel ? '10px 12px' : '12px 20px',
        display: 'flex', alignItems: 'center', gap: mobiel ? 8 : 12,
        flexWrap: mobiel ? 'wrap' : 'nowrap',
      }}>
        <button onClick={onTerug} style={{
          background: 'rgba(255,255,255,0.2)', border: 'none', color: 'white',
          borderRadius: 8, padding: '6px 12px', cursor: 'pointer', fontSize: 14, fontWeight: 700
        }}>
          ← Terug
        </button>
        <div style={{ fontWeight: 700, fontSize: 18 }}>
          Les {les.id}: {les.titel}
        </div>

        {/* Tabbladen */}
        <div style={{
          marginLeft: mobiel ? 0 : 'auto',
          width: mobiel ? '100%' : 'auto',
          display: 'flex', gap: 4,
          background: 'rgba(255,255,255,0.15)', borderRadius: 10, padding: 4,
          overflowX: 'auto',
        }}>
          {TABS.map(([m, label]) => (
            <button key={m} onClick={() => { setModus(m); setAangeklikte(null) }}
              style={{
                padding: mobiel ? '8px 14px' : '7px 16px',
                borderRadius: 7, border: 'none', cursor: 'pointer',
                background: modus === m ? 'white' : 'transparent',
                color: modus === m ? '#1a237e' : 'white',
                fontWeight: 700, fontSize: mobiel ? 18 : 14,
                transition: 'all 0.2s', flexShrink: 0,
              }}>
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: mobiel ? 10 : 20, maxWidth: 1400, margin: '0 auto' }}>

        {/* ── Quiz ── */}
        {modus === 'quiz' && (
          <div style={{ maxWidth: 680, margin: '0 auto' }}>
            <MentimeterQuiz les={les} />
          </div>
        )}

        {/* ── Weetjes ── */}
        {modus === 'weetjes' && (
          <div style={{ maxWidth: 800, margin: '0 auto' }}>
            <WeetjesPanel les={les} />
          </div>
        )}

        {/* ── Bewerken ── */}
        {modus === 'bewerken' && (
          <BewerkenTab les={les} />
        )}

        {/* ── Studeren / Oefenen: kaart + eventueel quizpanel ── */}
        {modus !== 'weetjes' && modus !== 'bewerken' && modus !== 'quiz' && (
          <>
            {modus === 'oefenen' && (
              <VoortgangBalk les={les} goed={goedBeantwoord.size} totaal={steden.length} />
            )}

            <div style={{
              display: 'grid',
              gridTemplateColumns: (modus === 'oefenen' && !mobiel) ? '1fr 360px' : '1fr',
              gap: mobiel ? 10 : 20,
              alignItems: 'start'
            }}>

              {/* Kaart */}
              <div>
                <MapView
                  les={les}
                  modus={modus}
                  onPlaatsKlik={handlePlaatsKlik}
                  actiefPlaats={aangeklikte}
                />

                {modus === 'oefenen' && (
                  <div style={{
                    marginTop: 10, padding: '8px 12px',
                    background: '#E8EAF6', borderRadius: 8,
                    fontSize: 13, color: '#5C6BC0'
                  }}>
                    💡 <strong>Tip:</strong> Klik op een stip, typ dan de naam in het paneel rechts.
                    Goed beantwoord: <strong>{goedBeantwoord.size}/{steden.length}</strong>
                  </div>
                )}
              </div>

              {/* Quiz panel */}
              {modus === 'oefenen' && (
                <div style={{ position: mobiel ? 'static' : 'sticky', top: 20 }}>
                  <QuizPanel
                    les={les}
                    aangeklikte={aangeklikte}
                    onReset={handleGoedAntwoord}
                  />

                  {goedBeantwoord.size > 0 && (
                    <div style={{ marginTop: 16 }}>
                      <div style={{ fontWeight: 700, fontSize: 13, color: '#1a237e', marginBottom: 6 }}>
                        ✅ Goed beantwoord:
                      </div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                        {[...goedBeantwoord].map(naam => (
                          <span key={naam} style={{
                            background: '#E8F5E9', color: '#2E7D32',
                            borderRadius: 12, padding: '3px 10px', fontSize: 12, fontWeight: 600
                          }}>
                            ✓ {naam}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
