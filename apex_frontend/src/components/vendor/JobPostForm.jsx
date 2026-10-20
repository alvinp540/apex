import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { createJob } from '../../api/vendorAPI'
import { required } from '../../utils/validators'

export default function JobPostForm({ onSuccess }) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm()

  const onSubmit = async (data) => {
    try {
      await createJob({
        ...data,
        skills_required: data.skills_required.split(',').map((s) => s.trim()).filter(Boolean),
      })
      toast.success('Job created as draft.')
      onSuccess?.()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create job.')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {[
        ['title', 'Job Title', 'text'],
        ['profession_required', 'Profession Required', 'text'],
        ['skills_required', 'Skills (comma-separated)', 'text'],
        ['budget_min', 'Budget Min (KES)', 'number'],
        ['budget_max', 'Budget Max (KES)', 'number'],
        ['deadline', 'Deadline', 'date'],
        ['location_preference', 'Location Preference (optional)', 'text'],
        ['min_trust_score', 'Minimum Trust Score (0-100)', 'number'],
      ].map(([name, label, type]) => (
        <div key={name}>
          <label>{label}</label>
          <input
            type={type}
            {...register(name, name !== 'location_preference' ? { validate: required } : {})}
            step={name.startsWith('budget') || name === 'min_trust_score' ? '0.01' : undefined}
          />
          {errors[name] && <span style={{ color: 'var(--color-error)', fontSize: '0.8rem' }}>{errors[name].message}</span>}
        </div>
      ))}
      <div>
        <label>Description</label>
        <textarea rows={4} {...register('description', { validate: required })} />
        {errors.description && <span style={{ color: 'var(--color-error)', fontSize: '0.8rem' }}>{errors.description.message}</span>}
      </div>
      <div>
        <label>Priority</label>
        <select {...register('priority')}>
          {['low', 'medium', 'high', 'urgent'].map((p) => <option key={p} value={p}>{p}</option>)}
        </select>
      </div>
      <button type="submit" className="btn-primary" disabled={isSubmitting}>
        {isSubmitting ? 'Creating…' : 'Create Job'}
      </button>
    </form>
  )
}
