import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { getMe, login as loginApi } from '../../api/authAPI'
import { useAuth } from '../../context/AuthContext'
import { email, required } from '../../utils/validators'

export default function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm()
  const { login } = useAuth()
  const navigate = useNavigate()

  const onSubmit = async (values) => {
    try {
      const { data } = await loginApi(values)
      const tokens = {
        access: data.access ?? data.accessToken ?? data.token ?? data.tokens?.access,
        refresh: data.refresh ?? data.refreshToken ?? data.tokens?.refresh,
      }
      const user = data.user ?? data.profile ?? data.userData ?? data.data?.user ?? null
      const resolvedUser = user ?? (tokens.access ? (await getMe()).data : null)

      login(tokens, resolvedUser)
      const isAdmin = resolvedUser?.is_admin === true || resolvedUser?.isAdmin === true || resolvedUser?.role === 'admin'
      navigate(isAdmin ? '/admin' : '/dashboard')
    } catch (err) {
      const details = err.response?.data
      const message = details?.error || details?.detail || (details && Object.values(details).flat().join(' ')) || 'Login failed.'
      toast.error(message)
    }
  }

  const labelStyle = { display: 'block', marginBottom: '0.45rem', color: '#e2e8f0', fontWeight: 600 }
  const inputStyle = {
    width: '100%',
    padding: '0.75rem 0.9rem',
    borderRadius: '0.8rem',
    border: '1px solid rgba(148,163,184,0.22)',
    background: 'rgba(15, 23, 42, 0.9)',
    color: '#f8fafc',
    fontSize: '0.95rem',
    boxSizing: 'border-box',
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div>
        <label style={labelStyle}>Email</label>
        <input type="email" {...register('email', { validate: email })} style={inputStyle} />
        {errors.email && <span style={{ color: '#fca5a5', fontSize: '0.8rem', display: 'block', marginTop: '0.35rem' }}>{errors.email.message}</span>}
      </div>
      <div>
        <label style={labelStyle}>Password</label>
        <input type="password" {...register('password', { validate: required })} style={inputStyle} />
        {errors.password && <span style={{ color: '#fca5a5', fontSize: '0.8rem', display: 'block', marginTop: '0.35rem' }}>{errors.password.message}</span>}
      </div>
      <button type="submit" className="btn-primary" disabled={isSubmitting} style={{ width: '100%', background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)', color: '#fff', fontWeight: 800, fontSize: '1rem', borderRadius: '0.9rem', padding: '0.9rem 1rem' }}>
        {isSubmitting ? 'Signing in…' : 'Sign In'}
      </button>
    </form>
  )
}
