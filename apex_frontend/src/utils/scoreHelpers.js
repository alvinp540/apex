export const TIER_COLORS = {
  bronze: '#cd7f32',
  silver: '#c0c0c0',
  gold: '#ffd700',
  platinum: '#e5e4e2',
  apex: '#6c63ff',
}

export const TIER_LABELS = {
  bronze: 'Bronze',
  silver: 'Silver',
  gold: 'Gold',
  platinum: 'Platinum',
  apex: 'APEX',
}

export const getTierFromScore = (score) => {
  if (score >= 80) return 'apex'
  if (score >= 60) return 'platinum'
  if (score >= 40) return 'gold'
  if (score >= 20) return 'silver'
  return 'bronze'
}

export const getRankMovementLabel = (movement) => {
  if (movement > 0) return `+${movement}`
  if (movement < 0) return `${movement}`
  return '—'
}
