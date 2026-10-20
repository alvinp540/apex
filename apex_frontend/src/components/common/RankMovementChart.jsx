import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function RankMovementChart({ history = [] }) {
  const data = history.slice().reverse().map((h, i) => ({
    name: `#${i + 1}`,
    score: h.overall_merit_score,
  }))

  return (
    <ResponsiveContainer width="100%" height={160}>
      <LineChart data={data}>
        <XAxis dataKey="name" hide />
        <YAxis domain={[0, 100]} hide />
        <Tooltip formatter={(v) => [`${v.toFixed(1)}`, 'Merit Score']} />
        <Line
          type="monotone" dataKey="score"
          stroke="var(--color-primary)" strokeWidth={2}
          dot={false} animationDuration={800}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
