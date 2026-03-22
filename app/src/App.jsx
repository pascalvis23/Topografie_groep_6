import { useState } from 'react'
import { lessen } from './data/provinces'
import LesPage from './components/LesPage'
import KalibratieTool from './components/KalibratieTool'

function LesKaart({ les, onClick }) {
  const [hover, setHover] = useState(false)
  const steden = les.plaatsen.filter(p => p.type === 'stad')

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: 'white', borderRadius: 12,
        border: `3px solid ${hover ? les.kleur : '#e0e0e0'}`,
        overflow: 'hidden', cursor: 'pointer',
        transform: hover ? 'translateY(-4px)' : 'none',
        boxShadow: hover ? `0 8px 24px ${les.kleur}44` : '0 2px 8px rgba(0,0,0,0.08)',
        transition: 'all 0.2s ease',
      }}
    >
      <div style={{ position: 'relative', height: 160, overflow: 'hidden', background: '#f5f5f5' }}>
        <img
          src={les.afbeeldingNamen}
          alt={les.titel}
          style={{
            width: '100%', height: '100%', objectFit: 'cover',
            objectPosition: 'center top',
            filter: hover ? 'brightness(1.05)' : 'brightness(0.97)',
            transition: 'filter 0.2s'
          }}
        />
        <div style={{
          position: 'absolute', top: 8, left: 8,
          background: les.kleur, color: 'white',
          borderRadius: 8, padding: '4px 10px',
          fontWeight: 900, fontSize: 16,
          boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
        }}>
          {les.id}
        </div>
      </div>
      <div style={{ padding: '12px 14px' }}>
        <div style={{ fontWeight: 800, fontSize: 16, color: '#1a237e', marginBottom: 4 }}>
          {les.titel}
        </div>
        <div style={{ fontSize: 12, color: '#666' }}>
          {steden.length} steden te leren
        </div>
        <div style={{ marginTop: 10, display: 'flex', gap: 6 }}>
          <span style={{
            background: '#E8EAF6', color: '#3949AB',
            borderRadius: 6, padding: '4px 8px', fontSize: 11, fontWeight: 600
          }}>📖 Bestuderen</span>
          <span style={{
            background: '#E8F5E9', color: '#2E7D32',
            borderRadius: 6, padding: '4px 8px', fontSize: 11, fontWeight: 600
          }}>✏️ Oefenen</span>
        </div>
      </div>
    </div>
  )
}

function HomeScherm({ onLesKlik, onKalibratie }) {
  return (
    <div style={{ minHeight: '100vh', background: '#f0f2ff', fontFamily: 'Arial, sans-serif' }}>
      <div style={{
        background: 'linear-gradient(135deg, #1a237e 0%, #283593 100%)',
        color: 'white', padding: '28px 24px', textAlign: 'center',
        boxShadow: '0 4px 12px rgba(26,35,126,0.3)'
      }}>
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: 12,
          background: 'rgba(255,255,255,0.1)', borderRadius: 12,
          padding: '8px 20px', marginBottom: 12
        }}>
          <span style={{ fontSize: 28 }}>🗺️</span>
          <div style={{ textAlign: 'left' }}>
            <div style={{ fontSize: 11, opacity: 0.8, letterSpacing: 2, textTransform: 'uppercase' }}>
              Huiswerkboek Groep 6
            </div>
            <div style={{ fontSize: 22, fontWeight: 900, letterSpacing: 1 }}>Topografie</div>
          </div>
        </div>
        <div style={{ fontSize: 14, opacity: 0.8 }}>
          Geobas-methode · 9 lessen · Interactief oefenen
        </div>
        <button onClick={onKalibratie} style={{
          marginTop: 10, padding: '5px 14px', background: 'rgba(255,255,255,0.15)',
          border: '1px solid rgba(255,255,255,0.3)', color: 'white',
          borderRadius: 6, cursor: 'pointer', fontSize: 12
        }}>
          🎯 Coördinaten instellen
        </button>
      </div>
      <div style={{ padding: '24px 20px', maxWidth: 900, margin: '0 auto' }}>
        <div style={{ fontSize: 16, fontWeight: 700, color: '#1a237e', marginBottom: 16 }}>
          Kies een les om te beginnen:
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))',
          gap: 16
        }}>
          {lessen.map(les => (
            <LesKaart key={les.id} les={les} onClick={() => onLesKlik(les)} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [activeLes, setActiveLes] = useState(null)
  const [kalibratie, setKalibratie] = useState(false)

  if (kalibratie) {
    return (
      <div>
        <div style={{ position: 'fixed', top: 8, right: 8, zIndex: 999 }}>
          <button onClick={() => setKalibratie(false)}
            style={{ padding: '6px 14px', background: '#f44336', color: 'white', border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 700 }}>
            ✕ Sluit kalibratietool
          </button>
        </div>
        <KalibratieTool />
      </div>
    )
  }

  if (activeLes) {
    return <LesPage les={activeLes} onTerug={() => setActiveLes(null)} />
  }

  return <HomeScherm onLesKlik={setActiveLes} onKalibratie={() => setKalibratie(true)} />
}
