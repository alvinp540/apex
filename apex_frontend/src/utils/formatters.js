export const formatScore = (score) => (score ?? 0).toFixed(1)

export const formatCurrency = (amount, currency = 'KES') =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency }).format(amount)

export const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleDateString('en-KE', { year: 'numeric', month: 'short', day: 'numeric' })

export const formatTimeAgo = (dateStr) => {
  const diff = Date.now() - new Date(dateStr).getTime()
  const minutes = Math.floor(diff / 60000)
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  return `${Math.floor(hours / 24)}d ago`
}
