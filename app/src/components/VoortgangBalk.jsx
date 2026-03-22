export default function VoortgangBalk({ les, goed, totaal }) {
  const pct = totaal > 0 ? Math.round((goed / totaal) * 100) : 0

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', marginBottom: 12 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 4 }}>
        <span style={{ color: '#555' }}>Voortgang {les.titel}</span>
        <span style={{ fontWeight: 700, color: pct === 100 ? '#4CAF50' : '#1a237e' }}>
          {goed}/{totaal} ({pct}%)
        </span>
      </div>
      <div style={{ background: '#E8EAF6', borderRadius: 8, height: 12, overflow: 'hidden' }}>
        <div style={{
          width: `${pct}%`, height: '100%',
          background: pct === 100 ? '#4CAF50' : les.kleur,
          borderRadius: 8, transition: 'width 0.4s ease',
        }} />
      </div>
      {pct === 100 && (
        <div style={{ textAlign: 'center', marginTop: 8, fontSize: 22 }}>
          🏆 Alle steden goed! Geweldig!
        </div>
      )}
    </div>
  )
}
