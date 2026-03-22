import { useState, useEffect } from 'react'

export function useMobiel() {
  const [mobiel, setMobiel] = useState(() => window.innerWidth <= 768)
  useEffect(() => {
    const handler = () => setMobiel(window.innerWidth <= 768)
    window.addEventListener('resize', handler)
    return () => window.removeEventListener('resize', handler)
  }, [])
  return mobiel
}
