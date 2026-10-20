import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { requestPasswordReset } from '../../api/authAPI'
import { email } from '../../utils/validators'

export default function PasswordResetForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm()

  const onSubmit = async (values) => {
    try {
      await requestPasswordReset(values.email)
      toast.success('Reset link sent if the email exists.')
    } catch {
      toast.error('Something went wrong.')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div>
        <label>Email</label>
        <input type="email" {...register('email', { validate: email })} />
        {errors.email && <span style={{ color: 'var(--color-error)', fontSize: '0.8rem' }}>{errors.email.message}</span>}
      </div>
      <button type="submit" className="btn-primary" disabled={isSubmitting}>
        {isSubmitting ? 'Sending…' : 'Send Reset Link'}
      </button>
    </form>
  )
}
