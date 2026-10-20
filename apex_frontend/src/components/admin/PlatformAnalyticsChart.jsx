import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'
import api from '../../api/axiosInstance'
import LoadingSpinner from '../common/LoadingSpinner'
import { TIER_COLORS } from '../../utils/scoreHelpers'

export default function PlatformAnalyticsChart() {
  const [data, setData] = useState(null)

  useEffect(() => {
    api.get('/analytics/platform/').then(({ data }) => setData(data)).catch(() => {})
  }, [])

  if (!data) return <LoadingSpinner />

  const barData = [
    { name: 'Total Users', value: data.total_users },
    { name: 'New (30d)', value: data.new_users_30d },
    { name: 'Active Subs', value: data.active_subscriptions },
    { name: 'Jobs', value: data.total_jobs },
    { name: 'Completed', value: data.completed_jobs },
    { name: 'Assessments', value: data.total_assessments_taken },
    { name: 'Flagged', value: data.flagged_attempts },
  ]

  const tierData = Object.entries(data.tier_breakdown || {}).map(([tier, count]) => ({
    name: tier, value: count, fill: TIER_COLORS[tier] || '#ccc',
  }))

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="card">
        <h4 style={{ marginBottom: '1rem' }}>Platform KPIs</h4>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={barData}>
            <XAxis dataKey="name" tick={{ fontSize: 11 }} />
            <YAxis hide />
            <Tooltip />
            <Bar dataKey="value" fill="var(--color-primary)" radius={[4,4,0,0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      {tierData.length > 0 && (
        <div className="card">
          <h4 style={{ marginBottom: '1rem' }}>Tier Distribution</h4>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={tierData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {tierData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
              </Pie>
              <Legend />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
