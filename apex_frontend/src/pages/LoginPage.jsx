import { Link } from 'react-router-dom'
import LoginForm from '../components/auth/LoginForm'

export default function LoginPage() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem 1rem',
      background: 'radial-gradient(circle at top, rgba(124,58,237,0.18), transparent 28%), #040b1b',
    }}>
      <div style={{
        width: '100%',
        maxWidth: '1100px',
        display: 'grid',
        gridTemplateColumns: '1.15fr 0.85fr',
        background: 'rgba(15, 23, 42, 0.9)',
        border: '1px solid rgba(167,139,250,0.2)',
        borderRadius: '1.75rem',
        overflow: 'hidden',
        boxShadow: '0 32px 80px rgba(2, 6, 23, 0.55)',
      }}>
        <div style={{
          position: 'relative',
          minHeight: '620px',
          padding: '2.3rem',
          display: 'flex',
          alignItems: 'flex-end',
          background: 'linear-gradient(180deg, rgba(10,14,27,0.3), rgba(3,7,18,0.8)), linear-gradient(135deg, #111827, #1f2937 45%, #0f172a)',
        }}>
          <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(circle at 20% 20%, rgba(139,92,246,0.45), transparent 26%), radial-gradient(circle at 75% 25%, rgba(59,130,246,0.16), transparent 22%)', opacity: 0.9 }} />
          <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ color: '#c4b5fd', fontSize: '0.8rem', letterSpacing: '0.14em', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.9rem' }}>
              Welcome back
            </div>
            <h1 style={{ fontSize: '3rem', lineHeight: 1, fontWeight: 900, marginBottom: '1rem' }}>Access the next chapter of your career.</h1>
            <p style={{ maxWidth: '460px', color: '#dbeafe', fontSize: '1.02rem', lineHeight: 1.7 }}>
              Track your merit, compete in cohorts, and unlock real opportunities with trusted vendors and performance data.
            </p>
          </div>
        </div>

        <div style={{ background: 'rgba(15, 23, 42, 0.92)', padding: '2.5rem 2rem', display: 'flex', alignItems: 'center' }}>
          <div style={{ width: '100%' }}>
            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '52px', height: '52px', borderRadius: '16px', background: 'linear-gradient(135deg, #8b5cf6, #4f46e5)', color: '#fff', fontSize: '1.4rem', fontWeight: 900, marginBottom: '0.9rem' }}>A</div>
              <h2 style={{ fontSize: '2.1rem', fontWeight: 800, marginBottom: '0.35rem' }}>Sign in</h2>
              <p style={{ color: '#94a3b8' }}>Continue your Apex journey.</p>
            </div>

            <LoginForm />

            <p style={{ textAlign: 'center', marginTop: '1rem', color: '#dbeafe', fontSize: '0.9rem' }}>
              No account? <Link to="/register" style={{ color: '#c4b5fd', fontWeight: 700 }}>Register</Link>
              {' '}·{' '}
              <Link to="/forgot-password" style={{ color: '#c4b5fd', fontWeight: 700 }}>Forgot password?</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
