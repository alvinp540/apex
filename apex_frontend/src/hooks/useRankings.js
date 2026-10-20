import { useState, useEffect } from 'react'
import { getGlobalRankings, getMyRanking } from '../api/rankingAPI'

export function useRankings() {
  const [rankings, setRankings] = useState([])
  const [myRanking, setMyRanking] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getGlobalRankings(), getMyRanking()])
      .then(([global, my]) => {
        setRankings(global.data.results || global.data)
        setMyRanking(my.data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return { rankings, myRanking, loading }
}
