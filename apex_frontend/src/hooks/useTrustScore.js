import { useState, useEffect } from 'react'
import api from '../api/axiosInstance'

export function useTrustScore() {
  const [score, setScore] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/trust/score/')
      .then(({ data }) => setScore(data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return { score, loading }
}
