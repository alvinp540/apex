import { useState } from 'react'
import Navbar from '../components/common/Navbar'
import RankingTable from '../components/rankings/RankingTable'
import LeaderboardCard from '../components/rankings/LeaderboardCard'
import { useRankings } from '../hooks/useRankings'
import MeritBadge from '../components/common/MeritBadge'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { getRankMovementLabel } from '../utils/scoreHelpers'

export default function RankingsPage() {
  const { rankings, myRanking, loading } = useRankings()
  const [tab, setTab] = useState('global')
  const top3 = rankings.slice(0, 3)

  const topCards = [
    { id: 1, name: 'Brian M.', role: 'Backend Developer', score: '9,152', badge: 'Gold' },
    { id: 2, name: 'Sharon N.', role: 'UI/UX Designer', score: '8,742', badge: 'Silver' },
    { id: 3, name: 'Ian M.', role: 'Mobile Developer', score: '8,215', badge: 'Gold' },
  ]

  return (
    <>
      <Navbar />
      <div className="page-container" style={{ maxWidth: '1280px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 0.8fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
          <div style={{ background: 'rgba(15,23,42,0.82)', border: '1px solid rgba(148,163,184,0.12)', borderRadius: '1.3rem', padding: '1.3rem' }}>
            <div style={{ fontSize: '0.72rem', letterSpacing: '0.14em', color: '#a78bfa', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.55rem' }}>Leaderboard</div>
            <h2 style={{ fontSize: '2.2rem', fontWeight: 800, marginBottom: '0.5rem' }}>APEX Leaderboard</h2>
            <p style={{ color: '#cbd5e1', marginBottom: '1rem' }}>Track your rank, compare your performance, and climb the merit ladder.</p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: '1rem' }}>
              {topCards.map((person) => (
                <div key={person.id} style={{ background: 'rgba(10,14,27,0.7)', border: '1px solid rgba(148,163,184,0.12)', borderRadius: '1rem', padding: '1rem', textAlign: 'center' }}>
                  <div style={{ width: '52px', height: '52px', borderRadius: '50%', background: 'linear-gradient(135deg, #c4b5fd, #8b5cf6)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, color: '#fff', marginBottom: '0.7rem' }}>{person.name.split(' ')[0][0]}{person.name.split(' ')[1][0]}</div>
                  <div style={{ fontWeight: 800 }}>{person.name}</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.78rem', marginBottom: '0.5rem' }}>{person.role}</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 900, color: '#a78bfa' }}>{person.score}</div>
                  <div style={{ fontSize: '0.72rem', color: '#cbd5e1', marginTop: '0.35rem' }}>{person.badge}</div>
                </div>
              ))}
            </div>
          </div>

          {myRanking && (
            <div className="card" style={{ marginBottom: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '1rem', background: 'rgba(15,23,42,0.82)', border: '1px solid rgba(148,163,184,0.12)' }}>
              <div>
                <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>Your Global Rank</div>
                <div style={{ fontSize: '2.8rem', fontWeight: 900, color: '#a78bfa' }}>#{myRanking.global_rank}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>Movement</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: myRanking.rank_movement > 0 ? 'var(--color-success)' : myRanking.rank_movement < 0 ? 'var(--color-error)' : 'var(--color-text-muted)' }}>
                  {getRankMovementLabel(myRanking.rank_movement)}
                </div>
              </div>
              <div><MeritBadge tier={myRanking.tier} size="lg" /></div>
            </div>
          )}
        </div>

        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
          {['global', 'top3'].map((t) => (
            <button key={t} onClick={() => setTab(t)} style={{
              background: tab === t ? 'var(--color-primary)' : 'var(--color-border)',
              color: tab === t ? '#fff' : 'var(--color-text)',
              borderRadius: '0.75rem',
              padding: '0.7rem 1rem',
              fontWeight: 700,
            }}>
              {t === 'global' ? 'Full Rankings' : 'Top 3'}
            </button>
          ))}
        </div>

        {loading ? <LoadingSpinner /> : tab === 'global'
          ? <RankingTable rankings={rankings} />
          : <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {top3.map((r, i) => <LeaderboardCard key={r.id} ranking={r} position={i + 1} />)}
            </div>
        }
      </div>
    </>
  )
}
