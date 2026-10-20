export default function StatCard({ label, value, sub, color }) {
  return (
    <div className="card" style={{ borderTop: `4px solid ${color || 'var(--color-primary)'}` }}>
      <div style={{ fontSize: '2rem', fontWeight: 700, color: color || 'var(--color-primary)' }}>
        {value}
      </div>
      <div style={{ fontWeight: 600, marginTop: '0.25rem' }}>{label}</div>
      {sub && <div style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>{sub}</div>}
    </div>
  )
}
