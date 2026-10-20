import { useEffect, useMemo, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import homeHero from '../assets/images/home-hero.jpeg'

const WATCH_KEY = 'apex_intro_watched'
const chapters = [
  {
    eyebrow: '01 / The gap',
    title: 'Talent is everywhere. Trusted proof is not.',
    body: 'Apex gives capable people a fairer way to be seen. Instead of relying on popularity, connections, or a polished CV alone, you build a record of what you can actually do.',
    signal: 'Potential becomes visible',
    color: '#8b5cf6',
  },
  {
    eyebrow: '02 / Your proof',
    title: 'Turn performance into portable credibility.',
    body: 'Your profile grows through completed work, assessments, feedback, consistency, and verified outcomes. Every signal contributes to a living merit record that gets stronger over time.',
    signal: 'Performance earns trust',
    color: '#38bdf8',
  },
  {
    eyebrow: '03 / The engine',
    title: 'Grow inside cohorts that make progress measurable.',
    body: 'Cohorts give you structured challenges, mentors, accountability, and a clear next step. You learn by doing, receive useful feedback, and see exactly how your progress changes your standing.',
    signal: 'Practice compounds',
    color: '#34d399',
  },
  {
    eyebrow: '04 / The bridge',
    title: 'Meet opportunities that fit your capability.',
    body: 'Vendors and teams use trusted performance signals to discover people for real work. Your skills, reliability, and track record help the right opportunities find you.',
    signal: 'Proof opens doors',
    color: '#fbbf24',
  },
  {
    eyebrow: '05 / The reason',
    title: 'A more useful professional economy starts with trust.',
    body: 'Apex reduces guesswork for everyone: professionals get a fair shot, mentors see where to help, and opportunity owners can act on evidence. You are not just joining a platform. You are building leverage.',
    signal: 'Your next move starts here',
    color: '#fb7185',
  },
]

export const introWatched = () => localStorage.getItem(WATCH_KEY) === 'true'

export default function HowItWorksPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const nextPath = new URLSearchParams(location.search).get('next') || '/register'
  const [isPlaying, setIsPlaying] = useState(false)
  const [progress, setProgress] = useState(0)
  const duration = 45
  const currentSecond = Math.floor((progress / 100) * duration)
  const chapterIndex = Math.min(chapters.length - 1, Math.floor(currentSecond / 9))
  const chapter = chapters[chapterIndex]
  const completed = progress >= 100

  useEffect(() => {
    if (!isPlaying || completed) return undefined
    const timer = window.setInterval(() => {
      setProgress((current) => Math.min(100, current + 100 / (duration * 10)))
    }, 100)
    return () => window.clearInterval(timer)
  }, [isPlaying, completed])

  useEffect(() => {
    if (completed) setIsPlaying(false)
  }, [completed])

  const timeLabel = useMemo(() => {
    const seconds = Math.min(duration, currentSecond)
    return `0:${String(seconds).padStart(2, '0')} / 0:45`
  }, [currentSecond])

  const finishIntro = () => {
    if (!completed) return
    localStorage.setItem(WATCH_KEY, 'true')
    navigate(nextPath)
  }

  return (
    <main style={{ minHeight: '100vh', background: '#07111f', color: '#f8fafc', padding: '1.5rem' }}>
      <div style={{ maxWidth: '1180px', margin: '0 auto' }}>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem', marginBottom: '2.5rem' }}>
          <Link to="/" style={{ color: '#f8fafc', fontWeight: 900, fontSize: '1.3rem', letterSpacing: '-0.04em' }}>A / APEX</Link>
          <span style={{ color: '#94a3b8', fontSize: '0.78rem', letterSpacing: '0.14em', textTransform: 'uppercase', fontWeight: 800 }}>Required before entry</span>
        </header>

        <section style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.1fr) minmax(320px, 0.9fr)', gap: '2.5rem', alignItems: 'center' }}>
          <div>
            <p style={{ color: '#a78bfa', fontWeight: 800, letterSpacing: '0.16em', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.8rem' }}>Watch the Apex story</p>
            <h1 style={{ fontSize: 'clamp(2.8rem, 6vw, 5.8rem)', lineHeight: 0.94, letterSpacing: '-0.07em', maxWidth: '720px', marginBottom: '1.2rem' }}>Before you enter, understand what you are building.</h1>
            <p style={{ maxWidth: '650px', color: '#cbd5e1', fontSize: '1.08rem', lineHeight: 1.75 }}>This short walkthrough explains the problem Apex solves, how the system works, and why your performance record matters. Watch it once, then choose your path in.</p>
            <div style={{ display: 'flex', gap: '0.7rem', flexWrap: 'wrap', marginTop: '1.5rem' }}>
              <span style={{ border: '1px solid rgba(148,163,184,0.24)', padding: '0.45rem 0.7rem', borderRadius: '999px', color: '#dbeafe', fontSize: '0.82rem' }}>45 seconds</span>
              <span style={{ border: '1px solid rgba(148,163,184,0.24)', padding: '0.45rem 0.7rem', borderRadius: '999px', color: '#dbeafe', fontSize: '0.82rem' }}>5 chapters</span>
              <span style={{ border: '1px solid rgba(148,163,184,0.24)', padding: '0.45rem 0.7rem', borderRadius: '999px', color: '#dbeafe', fontSize: '0.82rem' }}>One fairer system</span>
            </div>
          </div>

          <div style={{ background: '#0d1b2e', border: '1px solid rgba(148,163,184,0.2)', borderRadius: '1.2rem', padding: '0.7rem', boxShadow: '0 24px 70px rgba(0,0,0,0.32)' }}>
            <div style={{ position: 'relative', aspectRatio: '16 / 10', overflow: 'hidden', borderRadius: '0.8rem', backgroundImage: `linear-gradient(120deg, rgba(7,17,31,0.88), rgba(7,17,31,0.34)), url(${homeHero})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
              <div style={{ position: 'absolute', inset: 0, padding: '1.3rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem' }}><span style={{ color: chapter.color, fontSize: '0.72rem', fontWeight: 900, letterSpacing: '0.14em', textTransform: 'uppercase' }}>{chapter.eyebrow}</span><span style={{ color: '#e2e8f0', fontSize: '0.75rem' }}>APEX / 01</span></div>
                <div><div style={{ color: '#fff', fontSize: 'clamp(1.5rem, 3vw, 2.4rem)', fontWeight: 900, lineHeight: 1.02, letterSpacing: '-0.05em', maxWidth: '420px' }}>{chapter.title}</div><div style={{ marginTop: '0.7rem', color: '#cbd5e1', fontSize: '0.9rem' }}>{chapter.signal}</div></div>
              </div>
            </div>
            <div style={{ padding: '0.75rem 0.35rem 0.2rem' }}>
              <div style={{ height: '5px', background: 'rgba(148,163,184,0.2)', borderRadius: '999px', overflow: 'hidden' }}><div style={{ height: '100%', width: `${progress}%`, background: chapter.color, transition: 'width 100ms linear' }} /></div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.75rem', marginTop: '0.7rem' }}><button aria-label={isPlaying ? 'Pause walkthrough' : 'Play walkthrough'} onClick={() => setIsPlaying((playing) => !playing)} disabled={completed} style={{ background: chapter.color, color: '#07111f', fontWeight: 900, minWidth: '92px' }}>{completed ? 'Watched' : isPlaying ? 'Pause' : 'Play'}</button><span style={{ color: '#94a3b8', fontSize: '0.78rem', fontVariantNumeric: 'tabular-nums' }}>{timeLabel}</span></div>
            </div>
          </div>
        </section>

        <section style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(280px, 0.65fr)', gap: '2rem', marginTop: '4rem', paddingBottom: '3rem' }}>
          <div><p style={{ color: chapter.color, fontWeight: 800, letterSpacing: '0.12em', textTransform: 'uppercase', fontSize: '0.72rem' }}>{chapter.eyebrow}</p><h2 style={{ fontSize: '2rem', lineHeight: 1.05, margin: '0.45rem 0 0.8rem', letterSpacing: '-0.05em' }}>{chapter.title}</h2><p style={{ color: '#cbd5e1', lineHeight: 1.8, maxWidth: '650px' }}>{chapter.body}</p></div>
          <div style={{ borderLeft: '1px solid rgba(148,163,184,0.18)', paddingLeft: '1.4rem' }}><p style={{ color: '#94a3b8', fontSize: '0.78rem', textTransform: 'uppercase', letterSpacing: '0.12em', fontWeight: 800, marginBottom: '0.8rem' }}>Your route in</p><p style={{ color: '#e2e8f0', lineHeight: 1.7, marginBottom: '1rem' }}>{completed ? 'You have the context. Continue to create an account or sign in.' : 'The next step unlocks after the walkthrough reaches the end.'}</p><button onClick={finishIntro} disabled={!completed} className="btn-primary" style={{ width: '100%', opacity: completed ? 1 : 0.45 }}>{nextPath === '/login' ? 'Continue to sign in' : 'Continue to join Apex'} </button></div>
        </section>

        <footer style={{ borderTop: '1px solid rgba(148,163,184,0.14)', paddingTop: '1.2rem', color: '#64748b', fontSize: '0.8rem' }}>Apex is built around evidence, growth, and access to meaningful opportunity.</footer>
      </div>
    </main>
  )
}
