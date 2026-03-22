import { useState, useEffect, useCallback } from 'react'
import { lessen } from '../data/provinces'
import { useMobiel } from '../hooks/useMobiel'

const TIMER_SEC = 15
const MAX_VRAGEN = 10

const OPTIE_STIJL = [
  { bg: '#E53935', hover: '#B71C1C', letter: 'A', icon: '🔴' },
  { bg: '#1E88E5', hover: '#0D47A1', letter: 'B', icon: '🔵' },
  { bg: '#F9A825', hover: '#F57F17', letter: 'C', icon: '🟡' },
  { bg: '#43A047', hover: '#1B5E20', letter: 'D', icon: '🟢' },
]

function shuffle(arr) { return [...arr].sort(() => Math.random() - 0.5) }

function genereerVragen(les) {
  const steden = les.plaatsen.filter(p => p.type === 'stad')
  const alleAndereSteden = lessen
    .filter(l => l.id !== les.id)
    .flatMap(l => l.plaatsen.filter(p => p.type === 'stad'))

  const vragen = []

  // Type 1: kaart-vraag — welke stad is de gemarkeerde stip?
  shuffle(steden).slice(0, 6).forEach(stad => {
    const fouten = shuffle(alleAndereSteden).slice(0, 3).map(s => s.naam)
    vragen.push({
      type: 'kaart',
      vraag: 'Welke stad is de gemarkeerde stip?',
      juist: stad.naam,
      opties: shuffle([stad.naam, ...fouten]),
      plaats: stad,
    })
  })

  // Type 2: welke hoort bij deze provincie?
  shuffle(steden).slice(0, 4).forEach(juist => {
    const fouten = shuffle(alleAndereSteden).slice(0, 3).map(s => s.naam)
    vragen.push({
      type: 'keuze',
      vraag: `Welke stad ligt in ${les.titel}?`,
      juist: juist.naam,
      opties: shuffle([juist.naam, ...fouten]),
    })
  })

  // Type 3: hoofdstad van de provincie
  if (steden.length > 0) {
    const hoofdstad = steden[0]
    const fouten = shuffle(alleAndereSteden).slice(0, 3).map(s => s.naam)
    vragen.push({
      type: 'keuze',
      vraag: `Wat is de hoofdstad van ${les.titel}?`,
      juist: hoofdstad.naam,
      opties: shuffle([hoofdstad.naam, ...fouten]),
      hint: `(de eerste stad in de lijst)`,
    })
  }

  return shuffle(vragen).slice(0, MAX_VRAGEN)
}

// ── Mini-kaart met één gemarkeerde stip ──────────────────────────────────────
function MiniKaart({ les, plaats, beantwoord }) {
  const steden = les.plaatsen.filter(p => p.type === 'stad' || p.type === 'eiland')
  return (
    <div style={{ position: 'relative', maxWidth: 420, margin: '0 auto', borderRadius: 8, overflow: 'hidden', border: '3px solid rgba(255,255,255,0.3)' }}>
      <img src={les.afbeeldingBlanco} alt="kaart" style={{ width: '100%', display: 'block' }} draggable={false} />
      {steden.map((p, i) => {
        const isGevraagd = p.naam === plaats.naam
        return (
          <div key={i} style={{
            position: 'absolute', left: `${p.x}%`, top: `${p.y}%`,
            transform: 'translate(-50%,-50%)', zIndex: isGevraagd ? 10 : 2,
          }}>
            <div style={{
              width: isGevraagd ? 18 : 7,
              height: isGevraagd ? 18 : 7,
              borderRadius: '50%',
              background: isGevraagd ? '#FFD600' : 'rgba(200,200,200,0.5)',
              border: isGevraagd ? '3px solid white' : '1px solid rgba(255,255,255,0.4)',
              boxShadow: isGevraagd ? '0 0 0 4px rgba(255,214,0,0.4), 0 2px 8px rgba(0,0,0,0.5)' : 'none',
              animation: isGevraagd && !beantwoord ? 'pulse 1s infinite' : 'none',
            }} />
          </div>
        )
      })}
      <style>{`@keyframes pulse { 0%,100%{transform:translate(-50%,-50%) scale(1)} 50%{transform:translate(-50%,-50%) scale(1.4)} }`}</style>
    </div>
  )
}

// ── Timer-balk ──────────────────────────────────────────────────────────────
function TimerBalk({ seconden, totaal }) {
  const pct = (seconden / totaal) * 100
  const kleur = pct > 60 ? '#4CAF50' : pct > 30 ? '#FF9800' : '#F44336'
  return (
    <div style={{ background: 'rgba(255,255,255,0.2)', borderRadius: 99, height: 8, overflow: 'hidden', margin: '0 0 16px' }}>
      <div style={{
        height: '100%', width: `${pct}%`, background: kleur,
        borderRadius: 99, transition: 'width 1s linear, background 0.5s',
      }} />
    </div>
  )
}

// ── Eindscherm ──────────────────────────────────────────────────────────────
function Eindscherm({ score, totaal, onOpnieuw, les }) {
  const pct = Math.round((score / totaal) * 100)
  const sterren = pct >= 90 ? 3 : pct >= 60 ? 2 : pct >= 30 ? 1 : 0
  const berichten = [
    ['😢', 'Nog even oefenen!', '#E53935'],
    ['😊', 'Goed bezig!', '#FF9800'],
    ['😄', 'Prima gedaan!', '#1E88E5'],
    ['🏆', 'Uitstekend!', '#43A047'],
  ]
  const [emoji, bericht, kleur] = berichten[sterren]

  return (
    <div style={{ textAlign: 'center', padding: '40px 20px', color: 'white' }}>
      <div style={{ fontSize: 72, marginBottom: 8 }}>{emoji}</div>
      <div style={{ fontSize: 28, fontWeight: 900, marginBottom: 4 }}>{bericht}</div>
      <div style={{ fontSize: 16, opacity: 0.85, marginBottom: 24 }}>
        {score} van {totaal} vragen goed — {pct}%
      </div>
      <div style={{ fontSize: 36, marginBottom: 28 }}>
        {'⭐'.repeat(sterren)}{'☆'.repeat(3 - sterren)}
      </div>
      <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
        <button onClick={onOpnieuw} style={{
          padding: '14px 32px', background: 'white', color: '#1a237e',
          border: 'none', borderRadius: 12, fontSize: 16, fontWeight: 900, cursor: 'pointer',
        }}>
          🔄 Opnieuw spelen
        </button>
      </div>
    </div>
  )
}

// ── Hoofdcomponent ───────────────────────────────────────────────────────────
export default function MentimeterQuiz({ les }) {
  const mobiel = useMobiel()
  const [fase, setFase] = useState('intro') // intro | vraag | feedback | einde
  const [vragen, setVragen] = useState([])
  const [huidig, setHuidig] = useState(0)
  const [gekozen, setGekozen] = useState(null)
  const [score, setScore] = useState(0)
  const [timer, setTimer] = useState(TIMER_SEC)
  const [hoverOptie, setHoverOptie] = useState(null)

  const vraag = vragen[huidig]

  const startQuiz = () => {
    const q = genereerVragen(les)
    setVragen(q)
    setHuidig(0)
    setScore(0)
    setGekozen(null)
    setTimer(TIMER_SEC)
    setFase('vraag')
  }

  // Timer
  useEffect(() => {
    if (fase !== 'vraag') return
    if (timer <= 0) { verwerkAntwoord(null); return }
    const t = setTimeout(() => setTimer(t => t - 1), 1000)
    return () => clearTimeout(t)
  }, [fase, timer])

  const verwerkAntwoord = useCallback((keuze) => {
    setGekozen(keuze)
    if (keuze === vraag?.juist) setScore(s => s + 1)
    setFase('feedback')
    setTimeout(() => {
      const volgend = huidig + 1
      if (volgend >= vragen.length) {
        setFase('einde')
      } else {
        setHuidig(volgend)
        setGekozen(null)
        setTimer(TIMER_SEC)
        setFase('vraag')
      }
    }, 2000)
  }, [vraag, huidig, vragen.length])

  // ── Intro ──────────────────────────────────────────────────────────────────
  if (fase === 'intro') {
    return (
      <div style={{
        background: 'linear-gradient(135deg, #1a237e 0%, #4527A0 100%)',
        borderRadius: 16, padding: mobiel ? '32px 20px' : '60px 40px',
        textAlign: 'center', color: 'white', fontFamily: 'Arial, sans-serif',
      }}>
        <div style={{ fontSize: mobiel ? 48 : 72, marginBottom: 12 }}>🗺️</div>
        <div style={{ fontSize: mobiel ? 22 : 32, fontWeight: 900, marginBottom: 8 }}>
          Quiztime!
        </div>
        <div style={{ fontSize: 16, opacity: 0.85, marginBottom: 8 }}>
          {les.titel}
        </div>
        <div style={{ fontSize: 14, opacity: 0.7, marginBottom: 32 }}>
          {MAX_VRAGEN} vragen · {TIMER_SEC} seconden per vraag
        </div>
        <button onClick={startQuiz} style={{
          padding: '16px 48px', background: '#FFD600', color: '#1a237e',
          border: 'none', borderRadius: 50, fontSize: 20, fontWeight: 900,
          cursor: 'pointer', boxShadow: '0 4px 20px rgba(255,214,0,0.4)',
          transform: 'scale(1)', transition: 'transform 0.1s',
        }}
          onMouseOver={e => e.currentTarget.style.transform = 'scale(1.05)'}
          onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
        >
          Start Quiz!
        </button>
      </div>
    )
  }

  // ── Eindscherm ──────────────────────────────────────────────────────────────
  if (fase === 'einde') {
    return (
      <div style={{
        background: 'linear-gradient(135deg, #1a237e 0%, #4527A0 100%)',
        borderRadius: 16, fontFamily: 'Arial, sans-serif',
      }}>
        <Eindscherm score={score} totaal={vragen.length} onOpnieuw={() => setFase('intro')} les={les} />
      </div>
    )
  }

  if (!vraag) return null

  const isJuist = gekozen === vraag.juist
  const tijdUm = fase === 'feedback' && gekozen === null

  // ── Vraag + feedback ─────────────────────────────────────────────────────
  return (
    <div style={{
      background: 'linear-gradient(135deg, #1a237e 0%, #4527A0 100%)',
      borderRadius: 16, padding: mobiel ? '16px 12px' : '24px 28px',
      fontFamily: 'Arial, sans-serif', color: 'white',
    }}>

      {/* Header: voortgang + score + timer */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8, fontSize: 13 }}>
        <span style={{ opacity: 0.8 }}>Vraag {huidig + 1} / {vragen.length}</span>
        <div style={{
          background: 'rgba(255,255,255,0.2)', borderRadius: 50,
          width: 44, height: 44, display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 20, fontWeight: 900,
          color: timer <= 5 ? '#FFD600' : 'white',
        }}>
          {fase === 'feedback' ? (isJuist ? '✓' : tijdUm ? '⏱' : '✗') : timer}
        </div>
        <span style={{ opacity: 0.8 }}>Score: {score}</span>
      </div>

      {/* Timer balk */}
      {fase === 'vraag' && <TimerBalk seconden={timer} totaal={TIMER_SEC} />}

      {/* Vraag */}
      <div style={{
        background: 'rgba(255,255,255,0.1)', borderRadius: 12,
        padding: mobiel ? '14px' : '20px 24px', marginBottom: 16,
        fontSize: mobiel ? 16 : 20, fontWeight: 700, textAlign: 'center',
        minHeight: 56, display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        {vraag.vraag}
      </div>

      {/* Kaart (alleen bij kaart-type) */}
      {vraag.type === 'kaart' && (
        <div style={{ marginBottom: 16 }}>
          <MiniKaart les={les} plaats={vraag.plaats} beantwoord={fase === 'feedback'} />
        </div>
      )}

      {/* Feedback banner */}
      {fase === 'feedback' && (
        <div style={{
          background: tijdUm ? '#FF6F00' : isJuist ? '#2E7D32' : '#C62828',
          borderRadius: 10, padding: '10px 16px', marginBottom: 12,
          textAlign: 'center', fontWeight: 700, fontSize: 16,
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
        }}>
          {tijdUm ? '⏱ Tijd om! Het antwoord was:' : isJuist ? '🎉 Goed zo!' : '❌ Helaas! Het juiste antwoord:'}
          {(!isJuist || tijdUm) && (
            <span style={{ background: 'rgba(255,255,255,0.2)', borderRadius: 6, padding: '2px 8px' }}>
              {vraag.juist}
            </span>
          )}
        </div>
      )}

      {/* Antwoordopties */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: mobiel ? '1fr 1fr' : '1fr 1fr',
        gap: mobiel ? 8 : 12,
      }}>
        {vraag.opties.map((opt, i) => {
          const stijl = OPTIE_STIJL[i]
          const isGeselecteerd = gekozen === opt
          const isCorrect = opt === vraag.juist
          let achtergrond = stijl.bg

          if (fase === 'feedback') {
            if (isCorrect) achtergrond = '#2E7D32'
            else if (isGeselecteerd) achtergrond = '#C62828'
            else achtergrond = 'rgba(255,255,255,0.1)'
          } else if (hoverOptie === i) {
            achtergrond = stijl.hover
          }

          return (
            <button
              key={opt}
              disabled={fase === 'feedback'}
              onClick={() => fase === 'vraag' && verwerkAntwoord(opt)}
              onMouseEnter={() => setHoverOptie(i)}
              onMouseLeave={() => setHoverOptie(null)}
              style={{
                background: achtergrond,
                color: 'white', border: 'none', borderRadius: 10,
                padding: mobiel ? '14px 10px' : '18px 16px',
                fontSize: mobiel ? 14 : 16, fontWeight: 700,
                cursor: fase === 'vraag' ? 'pointer' : 'default',
                textAlign: 'left', display: 'flex', alignItems: 'center', gap: 10,
                transition: 'background 0.15s, transform 0.1s',
                transform: isGeselecteerd && fase === 'feedback' ? 'scale(1.03)' : 'scale(1)',
                boxShadow: '0 3px 8px rgba(0,0,0,0.3)',
                opacity: fase === 'feedback' && !isCorrect && !isGeselecteerd ? 0.45 : 1,
              }}
            >
              <span style={{
                minWidth: 28, height: 28, borderRadius: '50%',
                background: 'rgba(255,255,255,0.25)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontWeight: 900, fontSize: 13, flexShrink: 0,
              }}>
                {stijl.letter}
              </span>
              <span style={{ lineHeight: 1.3 }}>{opt}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
