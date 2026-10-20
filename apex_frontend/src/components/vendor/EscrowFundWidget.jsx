import { useState } from 'react'
import toast from 'react-hot-toast'
import { fundEscrow } from '../../api/escrowAPI'

export default function EscrowFundWidget({ jobId, onFunded }) {
  const [provider, setProvider] = useState('mpesa')
  const [phone, setPhone] = useState('')
  const [loading, setLoading] = useState(false)

  const handleFund = async () => {
    setLoading(true)
    try {
      const payload = { job_id: jobId, provider }
      if (provider === 'mpesa') payload.phone = phone
      const { data } = await fundEscrow(payload)
      if (provider === 'mpesa') toast.success('STK push sent to your phone.')
      else toast.success('Stripe payment intent created.')
      onFunded?.(data)
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to fund escrow.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <h4>Fund Escrow</h4>
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        {['mpesa', 'stripe'].map((p) => (
          <button key={p} onClick={() => setProvider(p)} style={{
            background: provider === p ? 'var(--color-primary)' : 'var(--color-border)',
            color: provider === p ? '#fff' : 'var(--color-text)',
            textTransform: 'capitalize', padding: '0.4rem 1rem',
          }}>
            {p === 'mpesa' ? 'M-Pesa' : 'Stripe'}
          </button>
        ))}
      </div>
      {provider === 'mpesa' && (
        <input
          type="tel" placeholder="Phone e.g. 254712345678"
          value={phone} onChange={(e) => setPhone(e.target.value)}
        />
      )}
      <button onClick={handleFund} className="btn-primary" disabled={loading}>
        {loading ? 'Processing…' : 'Fund Escrow'}
      </button>
    </div>
  )
}
