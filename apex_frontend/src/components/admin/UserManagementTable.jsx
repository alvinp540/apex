import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import api from '../../api/axiosInstance'
import { formatDate } from '../../utils/formatters'
import LoadingSpinner from '../common/LoadingSpinner'

export default function UserManagementTable() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/admin/users/').then(({ data }) => setUsers(data.results || data)).catch(() => {}).finally(() => setLoading(false))
  }, [])

  const toggleStatus = async (userId, currentActive) => {
    try {
      await api.patch(`/admin/users/${userId}/status/`, { is_active: !currentActive })
      setUsers((u) => u.map((user) => user.id === userId ? { ...user, is_active: !currentActive } : user))
      toast.success('User status updated.')
    } catch {
      toast.error('Failed to update user.')
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid var(--color-border)' }}>
            {['Email', 'Username', 'Role', 'Verified', 'Joined', 'Active', 'Actions'].map((h) => (
              <th key={h} style={{ textAlign: 'left', padding: '0.6rem 0.75rem', color: 'var(--color-text-muted)' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id} style={{ borderBottom: '1px solid var(--color-border)' }}>
              <td style={{ padding: '0.5rem 0.75rem' }}>{u.email}</td>
              <td style={{ padding: '0.5rem 0.75rem' }}>{u.username}</td>
              <td style={{ padding: '0.5rem 0.75rem', textTransform: 'capitalize' }}>{u.role}</td>
              <td style={{ padding: '0.5rem 0.75rem' }}>{u.is_email_verified ? '✓' : '✗'}</td>
              <td style={{ padding: '0.5rem 0.75rem' }}>{formatDate(u.created_at)}</td>
              <td style={{ padding: '0.5rem 0.75rem', color: u.is_active ? 'var(--color-success)' : 'var(--color-error)', fontWeight: 600 }}>
                {u.is_active ? 'Active' : 'Suspended'}
              </td>
              <td style={{ padding: '0.5rem 0.75rem' }}>
                <button onClick={() => toggleStatus(u.id, u.is_active)} style={{
                  background: u.is_active ? 'var(--color-error)' : 'var(--color-success)',
                  color: '#fff', padding: '0.25rem 0.6rem', fontSize: '0.8rem',
                }}>
                  {u.is_active ? 'Suspend' : 'Activate'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
