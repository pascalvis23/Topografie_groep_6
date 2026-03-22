import { useState, useEffect } from 'react'

function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5)
}

export default function QuizPanel({ les, aangeklikte, onReset }) {
  const [invoer, setInvoer] = useState('')
  const [status, setStatus] = useState(null) // null | 'goed' | 'fout'
  const [pogingen, setPogingen] = useState(0)
  const [hint, setHint] = useState(false)
  const [opties, setOpties] = useState([])
  const [quizType, setQuizType] = useState('typen') // 'typen' | 'keuze'

  const steden = les.plaatsen.filter(p => p.type === 'stad')

  useEffect(() => {
    if (aangeklikte) {
      setInvoer('')
      setStatus(null)
      setPogingen(0)
      setHint(false)

      // Genereer 4 opties voor multiple choice
      const overige = steden.filter(s => s.naam !== aangeklikte.naam)
      const willekeurig = shuffle(overige).slice(0, 3)
      setOpties(shuffle([aangeklikte, ...willekeurig]))
    }
  }, [aangeklikte])

  if (!aangeklikte) {
    return (
      <div style={{
        background: '#E8EAF6', border: '2px dashed #9FA8DA',
        borderRadius: 12, padding: 24, textAlign: 'center',
        color: '#5C6BC0', fontFamily: 'Arial, sans-serif'
      }}>
        <div style={{ fontSize: 32, marginBottom: 8 }}>👆</div>
        <p style={{ margin: 0, fontWeight: 600 }}>Klik op een stip op de kaart</p>
        <p style={{ margin: '4px 0 0', fontSize: 13 }}>Raad de naam van de stad!</p>
      </div>
    )
  }

  const controleer = (antwoord) => {
    const goed = antwoord.trim().toLowerCase() === aangeklikte.naam.toLowerCase()
    if (goed) {
      setStatus('goed')
    } else {
      const nieuwPogingen = pogingen + 1
      setPogingen(nieuwPogingen)
      setStatus('fout')
      if (nieuwPogingen >= 2) setHint(true)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (status === 'goed') { onReset(); return }
    controleer(invoer)
  }

  return (
    <div style={{ fontFamily: 'Arial, sans-serif' }}>

      {/* Quiz type switcher */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        {['typen', 'keuze'].map(t => (
          <button key={t} onClick={() => { setQuizType(t); setStatus(null); setInvoer('') }}
            style={{
              padding: '6px 14px', borderRadius: 20, border: 'none', cursor: 'pointer',
              background: quizType === t ? '#1a237e' : '#e8eaf6',
              color: quizType === t ? 'white' : '#1a237e',
              fontWeight: 600, fontSize: 13
            }}>
            {t === 'typen' ? '✏️ Typ de naam' : '🎯 Kies het antwoord'}
          </button>
        ))}
      </div>

      {/* Vraag */}
      <div style={{
        background: '#1a237e', color: 'white',
        borderRadius: 10, padding: '14px 18px', marginBottom: 12,
        fontSize: 15, fontWeight: 600
      }}>
        Welke plaats is dit?
        <div style={{ fontSize: 12, fontWeight: 400, marginTop: 4, opacity: 0.8 }}>
          Klik op een stip op de kaart en typ de naam
        </div>
      </div>

      {/* Hint na 2 foute pogingen */}
      {hint && status !== 'goed' && (
        <div style={{
          background: '#FFF9C4', border: '1px solid #F9A825',
          borderRadius: 8, padding: '8px 12px', marginBottom: 10,
          fontSize: 13, color: '#F57F17'
        }}>
          💡 Hint: De naam begint met <strong>"{aangeklikte.naam.slice(0, 2)}"</strong>
        </div>
      )}

      {/* Invoer of keuze */}
      {status !== 'goed' && (
        quizType === 'typen' ? (
          <form onSubmit={handleSubmit}>
            <input
              autoFocus
              value={invoer}
              onChange={e => setInvoer(e.target.value)}
              placeholder="Typ de naam van de stad..."
              style={{
                width: '100%', padding: '10px 12px', fontSize: 15,
                border: `2px solid ${status === 'fout' ? '#F44336' : '#9FA8DA'}`,
                borderRadius: 8, outline: 'none', boxSizing: 'border-box',
                fontFamily: 'Arial, sans-serif',
              }}
            />
            <button type="submit" style={{
              width: '100%', marginTop: 10, padding: '11px',
              background: '#1a237e', color: 'white', border: 'none',
              borderRadius: 8, fontSize: 15, fontWeight: 700, cursor: 'pointer'
            }}>
              Controleer →
            </button>
          </form>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            {opties.map((opt, i) => (
              <button key={i} onClick={() => controleer(opt.naam)}
                style={{
                  padding: '12px 8px', borderRadius: 8, border: '2px solid #9FA8DA',
                  background: 'white', cursor: 'pointer', fontSize: 14,
                  fontWeight: 600, fontFamily: 'Arial, sans-serif',
                  transition: 'all 0.1s',
                }}
                onMouseOver={e => e.currentTarget.style.background = '#E8EAF6'}
                onMouseOut={e => e.currentTarget.style.background = 'white'}
              >
                {opt.naam}
              </button>
            ))}
          </div>
        )
      )}

      {/* Feedback */}
      {status === 'goed' && (
        <div style={{
          background: '#E8F5E9', border: '2px solid #4CAF50',
          borderRadius: 10, padding: 16, textAlign: 'center'
        }}>
          <div style={{ fontSize: 36 }}>🎉</div>
          <div style={{ fontSize: 18, fontWeight: 700, color: '#2E7D32' }}>Super goed!</div>
          <div style={{ fontSize: 15, color: '#388E3C', marginTop: 4 }}>
            <strong>{aangeklikte.naam}</strong> is correct!
          </div>
          <button onClick={onReset} style={{
            marginTop: 12, padding: '10px 20px', background: '#4CAF50',
            color: 'white', border: 'none', borderRadius: 8, fontSize: 14,
            fontWeight: 700, cursor: 'pointer'
          }}>
            Volgende stad →
          </button>
        </div>
      )}

      {status === 'fout' && (
        <div style={{
          background: '#FFEBEE', border: '1px solid #EF9A9A',
          borderRadius: 8, padding: '8px 12px', marginTop: 8,
          fontSize: 13, color: '#C62828', display: 'flex', alignItems: 'center', gap: 6
        }}>
          ❌ Probeer het nog eens!
          {pogingen >= 3 && (
            <button onClick={() => { setStatus('goed') }} style={{
              marginLeft: 'auto', padding: '4px 10px', background: '#EF5350',
              color: 'white', border: 'none', borderRadius: 6, cursor: 'pointer',
              fontSize: 12, fontWeight: 700
            }}>
              Antwoord tonen
            </button>
          )}
        </div>
      )}
    </div>
  )
}
