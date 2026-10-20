import { Link } from 'react-router-dom'
import RegisterForm from '../components/auth/RegisterForm'

export default function RegisterPage() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(circle at top, rgba(139,92,246,0.2), transparent 28%), #050d1a',
      padding: '1.5rem 1rem',
    }}>
      <div className="card" style={{
        width: '100%',
        maxWidth: '520px',
        background: 'rgba(15, 23, 42, 0.95)',
        border: '1px solid rgba(148, 163, 184, 0.18)',
        boxShadow: '0 30px 60px rgba(2, 6, 23, 0.45)',
      }}>
        <h2 style={{ marginBottom: '0.75rem', textAlign: 'center', color: '#a78bfa', fontSize: '2.3rem', letterSpacing: '-0.05em' }}>APEX</h2>
        <h3 style={{ marginBottom: '1.5rem', textAlign: 'center', color: '#edf2ff', fontSize: '1.8rem' }}>Create Account</h3>
        <RegisterForm />
        <p style={{ textAlign: 'center', marginTop: '1rem', color: '#cbd5e1', fontSize: '0.9rem' }}>
          Already have an account? <Link to="/login" style={{ color: '#c4b5fd', fontWeight: 700 }}>Sign in</Link>
        </p>
      </div>
    </div>
  )
}
