import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import api from '../../api/axiosInstance'
import { formatTimeAgo } from '../../utils/formatters'
import LoadingSpinner from '../common/LoadingSpinner'

const SEVERITY_COLORS = {
  low: 'var(--color-success)', medium: 'var(--color-warning)',
  high: 'var(--color-error)', critical: '#7c3aed',
}

export default function FraudMonitorPanel() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/admin/fraud-logs/').then(({ data }) => setLogs(data.results || data)).catch(() => {}).finally(() => setLoading(false))
  }, [])

  const resolve = async (id) => {
    try {
      await api.patch(`/admin/fraud-logs/${id}/resolve/`)
      setLogs((l) => l.map((log) => log.id === id ? { ...log, is_resolved: true } : log))
      toast.success('Resolved.')
    } catch { toast.error('Failed.') }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
      {logs.length === 0 && <p style={{ color: 'var(--color-text-muted)' }}>No fraud events.</p>}
      {logs.map((log) => (
        <div key={log.id} className="card" style={{
          borderLeft: `4px solid ${SEVERITY_COLORS[log.severity]}`,
          opacity: log.is_resolved ? 0.6 : 1,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <span style={{ fontWeight: 700, textTransform: 'uppercase', fontSize: '0.8rem', color: SEVERITY_COLORS[log.severity] }}>
                {log.severity}
              </span>
              <span style={{ marginLeft: '0.5rem', fontWeight: 600 }}>{log.event_type}</span>
              <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginTop: '0.2rem' }}>{log.description}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>{formatTimeAgo(log.created_at)}</div>
            </div>
            {!log.is_resolved && (
              <button onClick={() => resolve(log.id)} style={{ background: 'var(--color-success)', color: '#fff', padding: '0.25rem 0.6rem', fontSize: '0.8rem' }}>
                Resolve
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
