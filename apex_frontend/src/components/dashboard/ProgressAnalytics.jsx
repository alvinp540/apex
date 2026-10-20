import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import api from '../../api/axiosInstance'
import LoadingSpinner from '../common/LoadingSpinner'

export default function ProgressAnalytics() {
  const [analytics, setAnalytics] = useState(null)

  useEffect(() => {
    api.get('/analytics/professional/me/').then(({ data }) => setAnalytics(data)).catch(() => {})
  }, [])

  if (!analytics) return <LoadingSpinner />

  const chartData = [
    { name: 'Assessments', value: analytics.total_assessments },
    { name: 'Avg Score', value: parseFloat((analytics.avg_score || 0).toFixed(1)) },
    { name: 'Jobs Done', value: analytics.jobs_completed },
    { name: 'Opportunities', value: analytics.opportunities_received },
  ]

  return (
    <div className="card">
      <h3 style={{ marginBottom: '1rem' }}>My Analytics</h3>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={chartData}>
          <XAxis dataKey="name" tick={{ fontSize: 12 }} />
          <YAxis hide />
          <Tooltip />
          <Bar dataKey="value" fill="var(--color-primary)" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
