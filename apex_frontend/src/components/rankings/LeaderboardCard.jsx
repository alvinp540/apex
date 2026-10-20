import MeritBadge from '../common/MeritBadge'

export default function LeaderboardCard({ ranking, position }) {
  const medals = { 1: '🥇', 2: '🥈', 3: '🥉' }

  return (
    <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
      <div style={{ fontSize: '1.5rem', minWidth: '2rem', textAlign: 'center' }}>
        {medals[position] || `#${position}`}
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: 700 }}>{ranking.full_name}</div>
        <div style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>{ranking.profession}</div>
      </div>
      <div style={{ textAlign: 'right' }}>
        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{ranking.overall_merit_score?.toFixed(1)}</div>
        <MeritBadge tier={ranking.tier} size="sm" />
      </div>
    </div>
  )
}
