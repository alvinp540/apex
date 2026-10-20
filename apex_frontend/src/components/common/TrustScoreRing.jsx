import { TIER_COLORS } from '../../utils/scoreHelpers'

export default function TrustScoreRing({ score = 0, tier = 'bronze', size = 120 }) {
  const r = (size / 2) - 10
  const circ = 2 * Math.PI * r
  const offset = circ - (score / 100) * circ
  const color = TIER_COLORS[tier] || '#6c63ff'

  return (
    <svg width={size} height={size}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="var(--color-border)" strokeWidth={8} />
      <circle
        cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${size/2} ${size/2})`}
        style={{ transition: 'stroke-dashoffset 0.8s ease' }}
      />
      <text x="50%" y="50%" dominantBaseline="middle" textAnchor="middle"
        fill="var(--color-text)" fontSize={size * 0.2} fontWeight="700">
        {score.toFixed(0)}
      </text>
    </svg>
  )
}
