import TrustScoreRing from '../common/TrustScoreRing'
import MeritBadge from '../common/MeritBadge'
import RankMovementChart from '../common/RankMovementChart'
import { useTrustScore } from '../../hooks/useTrustScore'
import LoadingSpinner from '../common/LoadingSpinner'
import api from '../../api/axiosInstance'
import { useState, useEffect } from 'react'

export default function MeritScoreWidget() {
  const { score, loading } = useTrustScore()
  const [history, setHistory] = useState([])

  useEffect(() => {
    api.get('/trust/score/history/').then(({ data }) => setHistory(data)).catch(() => {})
  }, [])

  if (loading) return <LoadingSpinner />
  if (!score) return <div className="card">No score yet. Complete an assessment to get started.</div>

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
        <TrustScoreRing score={score.overall_merit_score} tier={score.tier} size={120} />
        <div>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.3rem' }}>Merit Score</div>
          <MeritBadge tier={score.tier} size="lg" />
          <div style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
            {[
              ['PSP Consistency', score.psp_consistency_score],
              ['Cohort Performance', score.cohort_performance_score],
              ['Vendor Rating', score.vendor_rating_score],
              ['Authenticity', score.authenticity_confidence],
            ].map(([label, val]) => (
              <div key={label} style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
                {label}: <strong>{val?.toFixed(1)}</strong>
              </div>
            ))}
          </div>
        </div>
      </div>
      {history.length > 1 && (
        <div>
          <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: '0.5rem' }}>Score trend</div>
          <RankMovementChart history={history} />
        </div>
      )}
    </div>
  )
}
