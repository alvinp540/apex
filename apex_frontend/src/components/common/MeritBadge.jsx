import { TIER_COLORS, TIER_LABELS } from '../../utils/scoreHelpers'

export default function MeritBadge({ tier, size = 'md' }) {
  const sizes = { sm: '0.7rem', md: '0.85rem', lg: '1rem' }
  return (
    <span style={{
      background: TIER_COLORS[tier] || '#ccc',
      color: tier === 'silver' || tier === 'platinum' ? '#111' : '#fff',
      padding: '0.2em 0.7em',
      borderRadius: '99px',
      fontSize: sizes[size],
      fontWeight: 700,
      letterSpacing: '0.05em',
      textTransform: 'uppercase',
    }}>
      {TIER_LABELS[tier] || tier}
    </span>
  )
}
