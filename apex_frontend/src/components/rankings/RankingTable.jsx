import MeritBadge from '../common/MeritBadge'
import { getRankMovementLabel } from '../../utils/scoreHelpers'

export default function RankingTable({ rankings }) {
  if (!rankings?.length) return <p style={{ color: 'var(--color-text-muted)' }}>No rankings yet.</p>

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid var(--color-border)' }}>
            {['Rank', 'Name', 'Profession', 'Score', 'Tier', 'Movement'].map((h) => (
              <th key={h} style={{ textAlign: 'left', padding: '0.6rem 0.75rem', color: 'var(--color-text-muted)' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rankings.map((r) => (
            <tr key={r.id} style={{ borderBottom: '1px solid var(--color-border)' }}>
              <td style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>#{r.global_rank}</td>
              <td style={{ padding: '0.6rem 0.75rem' }}>{r.full_name}</td>
              <td style={{ padding: '0.6rem 0.75rem', color: 'var(--color-text-muted)' }}>{r.profession}</td>
              <td style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>{r.overall_merit_score?.toFixed(1)}</td>
              <td style={{ padding: '0.6rem 0.75rem' }}><MeritBadge tier={r.tier} size="sm" /></td>
              <td style={{
                padding: '0.6rem 0.75rem', fontWeight: 600,
                color: r.rank_movement > 0 ? 'var(--color-success)' : r.rank_movement < 0 ? 'var(--color-error)' : 'var(--color-text-muted)',
              }}>
                {getRankMovementLabel(r.rank_movement)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
