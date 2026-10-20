import { useCallback, useEffect, useRef, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import Navbar from '../components/common/Navbar'
import { getMyProfile, updateProfile, uploadAvatar } from '../api/profileAPI'
import { required } from '../utils/validators'
import { useTrustScore } from '../hooks/useTrustScore'

const cardStyle = { background: 'rgba(15, 23, 42, 0.72)', border: '1px solid rgba(148, 163, 184, 0.18)', borderRadius: '1.15rem' }
const inputStyle = { width: '100%', boxSizing: 'border-box', borderRadius: '0.7rem', border: '1px solid rgba(148, 163, 184, 0.25)', background: 'rgba(2, 6, 23, 0.35)', color: 'var(--color-text)', padding: '0.72rem 0.8rem' }

export default function ProfileSettingsPage() {
  const [profile, setProfile] = useState({})
  const [cameraStream, setCameraStream] = useState(null)
  const [cameraOpen, setCameraOpen] = useState(false)
  const [photoMenuOpen, setPhotoMenuOpen] = useState(false)
  const [uploading, setUploading] = useState(false)
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const { register, handleSubmit, reset, formState: { isSubmitting, errors } } = useForm()
  const { score } = useTrustScore()

  const loadProfile = useCallback(async () => {
    try {
      const { data } = await getMyProfile()
      setProfile(data)
      reset({
        ...data,
        skills: Array.isArray(data.skills) ? data.skills.join(', ') : '',
        highlights: Array.isArray(data.highlights) ? data.highlights.join('\n') : '',
      })
    } catch {
      toast.error('Unable to load your profile.')
    }
  }, [reset])

  useEffect(() => { loadProfile() }, [loadProfile])
  useEffect(() => { if (cameraStream && videoRef.current) videoRef.current.srcObject = cameraStream }, [cameraStream])
  useEffect(() => () => cameraStream?.getTracks().forEach((track) => track.stop()), [cameraStream])

  const stopCamera = () => {
    cameraStream?.getTracks().forEach((track) => track.stop())
    setCameraStream(null)
    setCameraOpen(false)
  }

  const handleAvatarUpload = async (file) => {
    if (!file) return
    if (!file.type.startsWith('image/')) {
      toast.error('Choose an image file.')
      return
    }
    setUploading(true)
    const form = new FormData()
    form.append('avatar', file)
    try {
      const { data } = await uploadAvatar(form)
      setProfile((current) => ({ ...current, avatar_url: data.avatar_url }))
      toast.success('Profile picture updated.')
    } catch {
      toast.error('Picture upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const startCamera = async () => {
    setPhotoMenuOpen(false)
    if (!navigator.mediaDevices?.getUserMedia) {
      toast.error('Camera access is not available in this browser.')
      return
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false })
      setCameraStream(stream)
      setCameraOpen(true)
    } catch {
      toast.error('Camera permission was not granted.')
    }
  }

  const capturePhoto = () => {
    const video = videoRef.current
    const canvas = canvasRef.current
    if (!video || !canvas || !video.videoWidth) return
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    canvas.getContext('2d').drawImage(video, 0, 0)
    canvas.toBlob(async (blob) => {
      if (!blob) return
      stopCamera()
      await handleAvatarUpload(new File([blob], 'apex-profile-photo.jpg', { type: 'image/jpeg' }))
    }, 'image/jpeg', 0.9)
  }

  const onSubmit = async (data) => {
    try {
      const payload = {
        ...data,
        years_experience: Number(data.years_experience || 0),
        show_whatsapp: Boolean(data.show_whatsapp),
        skills: (data.skills || '').split(',').map((item) => item.trim()).filter(Boolean),
        highlights: (data.highlights || '').split('\n').map((item) => item.trim()).filter(Boolean),
      }
      const { data: updated } = await updateProfile(payload)
      setProfile(updated)
      toast.success('Profile updated.')
    } catch (error) {
      const details = error.response?.data
      toast.error(typeof details === 'object' ? Object.values(details).flat().join(' ') : 'Failed to update profile.')
    }
  }

  const initials = (profile.full_name || 'A').trim().slice(0, 1).toUpperCase()
  const skills = Array.isArray(profile.skills) ? profile.skills : []
  const highlights = Array.isArray(profile.highlights) ? profile.highlights : []

  return (
    <>
      <Navbar />
      <main className="page-container" style={{ maxWidth: '960px', paddingTop: '2rem' }}>
        <section style={{ ...cardStyle, padding: 'clamp(1.25rem, 4vw, 2.5rem)', marginBottom: '1rem', background: 'linear-gradient(145deg, rgba(124, 58, 237, 0.22), rgba(15, 23, 42, 0.9) 44%, rgba(14, 165, 233, 0.12))' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'clamp(1rem, 4vw, 2.3rem)', flexWrap: 'wrap' }}>
            <div style={{ position: 'relative' }}>
              <div style={{ width: '126px', height: '126px', padding: '4px', borderRadius: '50%', background: 'linear-gradient(135deg, #f9a8d4, #a78bfa 50%, #38bdf8)', boxSizing: 'border-box' }}>
                <div style={{ width: '100%', height: '100%', borderRadius: '50%', overflow: 'hidden', display: 'grid', placeItems: 'center', background: '#172033', color: '#fff', fontWeight: 900, fontSize: '2.7rem', border: '4px solid #0f172a' }}>
                  {profile.avatar_url ? <img src={profile.avatar_url} alt={`${profile.full_name || 'Profile'} avatar`} style={{ width: '100%', height: '100%', objectFit: 'cover' }} /> : initials}
                </div>
              </div>
              <button type="button" onClick={() => setPhotoMenuOpen((open) => !open)} aria-label="Edit profile photo" style={{ position: 'absolute', right: '0', bottom: '0', width: '36px', height: '36px', borderRadius: '50%', border: '2px solid #0f172a', background: '#8b5cf6', color: '#fff', cursor: 'pointer', fontSize: '1.15rem', fontWeight: 800 }}>✎</button>
              {photoMenuOpen && <div style={{ position: 'absolute', zIndex: 4, top: 'calc(100% + 0.6rem)', left: 0, width: '190px', padding: '0.45rem', borderRadius: '0.75rem', background: '#172033', border: '1px solid rgba(148, 163, 184, 0.28)', boxShadow: '0 12px 30px rgba(0, 0, 0, 0.3)' }}><button type="button" onClick={startCamera} style={{ display: 'block', width: '100%', padding: '0.65rem', textAlign: 'left', background: 'transparent', color: '#f8fafc', border: 0, cursor: 'pointer' }}>Take photo</button><label style={{ display: 'block', padding: '0.65rem', color: '#f8fafc', cursor: 'pointer' }}>Choose from gallery or files<input type="file" accept="image/*" onChange={(event) => { setPhotoMenuOpen(false); handleAvatarUpload(event.target.files?.[0]) }} hidden /></label></div>}
            </div>
            <div style={{ flex: 1, minWidth: '220px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}><h1 style={{ margin: 0, fontSize: 'clamp(1.65rem, 4vw, 2.35rem)' }}>{profile.full_name || 'Your APEX profile'}</h1>{profile.is_online && <span style={{ color: '#86efac', fontSize: '0.8rem', fontWeight: 800 }}>● ONLINE</span>}</div>
              <p style={{ margin: '0.45rem 0', color: '#cbd5e1', fontSize: '1rem' }}>{profile.headline || profile.profession || 'Add a headline that tells your story.'}</p>
              <p style={{ margin: 0, color: '#94a3b8', fontSize: '0.9rem' }}>{[profile.location, profile.country].filter(Boolean).join(', ') || 'Set your location'} · {profile.years_experience || 0} years experience</p>
              <div style={{ display: 'flex', gap: '1.3rem', marginTop: '1.15rem' }}><span><strong>{skills.length}</strong><small style={{ display: 'block', color: '#94a3b8' }}>skills</small></span><span><strong>{highlights.length}</strong><small style={{ display: 'block', color: '#94a3b8' }}>highlights</small></span><span><strong>{profile.availability || 'offline'}</strong><small style={{ display: 'block', color: '#94a3b8' }}>availability</small></span></div>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.65rem', flexWrap: 'wrap', marginTop: '1.5rem' }}>
            {profile.linkedin_url && <a className="btn-outline" href={profile.linkedin_url} target="_blank" rel="noreferrer">LinkedIn ↗</a>}
            {profile.portfolio_url && <a className="btn-outline" href={profile.portfolio_url} target="_blank" rel="noreferrer">Portfolio ↗</a>}
            {profile.show_whatsapp && profile.whatsapp_chat_url && <a className="btn-primary" href={profile.whatsapp_chat_url} target="_blank" rel="noreferrer">Chat on WhatsApp</a>}
          </div>
        </section>

        <section style={{ ...cardStyle, padding: '1.1rem', marginBottom: '1rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem' }}>
          <div><small style={{ color: '#94a3b8' }}>Current merit score</small><strong style={{ display: 'block', fontSize: '1.8rem', color: '#c4b5fd' }}>{score ? Number(score.overall_merit_score).toFixed(0) : '—'}</strong></div>
          <div><small style={{ color: '#94a3b8' }}>PSP consistency</small><strong style={{ display: 'block', fontSize: '1.8rem', color: '#67e8f9' }}>{score ? `${Number(score.psp_consistency_score || 0).toFixed(0)}%` : '—'}</strong></div>
          <div><small style={{ color: '#94a3b8' }}>Cohort performance</small><strong style={{ display: 'block', fontSize: '1.8rem', color: '#86efac' }}>{score ? `${Number(score.cohort_performance_score || 0).toFixed(0)}%` : '—'}</strong></div>
          <div><small style={{ color: '#94a3b8' }}>Trust tier</small><strong style={{ display: 'block', fontSize: '1.25rem', color: '#fbbf24', marginTop: '0.35rem' }}>{score?.tier || 'Building'}</strong></div>
        </section>

        {highlights.length > 0 && <section style={{ ...cardStyle, padding: '1.1rem', marginBottom: '1rem' }}><strong style={{ display: 'block', marginBottom: '0.8rem' }}>Highlights</strong><div style={{ display: 'flex', gap: '0.8rem', flexWrap: 'wrap' }}>{highlights.map((highlight) => <div key={highlight} style={{ width: '94px', textAlign: 'center' }}><div style={{ width: '62px', height: '62px', margin: '0 auto 0.4rem', borderRadius: '50%', border: '2px solid #a78bfa', display: 'grid', placeItems: 'center', background: 'rgba(139, 92, 246, 0.14)', fontSize: '1.25rem' }}>✦</div><small style={{ color: '#cbd5e1', overflowWrap: 'anywhere' }}>{highlight}</small></div>)}</div></section>}

        <section id="profile-editor" style={{ ...cardStyle, padding: 'clamp(1.1rem, 4vw, 2rem)' }}>
          <div style={{ marginBottom: '1.5rem' }}><p style={{ color: '#a78bfa', fontWeight: 800, fontSize: '0.75rem', letterSpacing: '0.13em', margin: 0 }}>EDIT PROFILE</p><h2 style={{ margin: '0.35rem 0' }}>Make your profile unmistakably yours</h2><p style={{ margin: 0, color: '#94a3b8' }}>Use a photo, your professional links, and a few concise highlights.</p></div>
          {uploading && <p style={{ color: '#94a3b8', margin: '0 0 1.4rem' }}>Uploading your new profile picture…</p>}
          {cameraOpen && <div style={{ marginBottom: '1.4rem', padding: '1rem', borderRadius: '0.9rem', background: '#020617' }}><video ref={videoRef} autoPlay playsInline style={{ display: 'block', width: '100%', maxHeight: '420px', objectFit: 'cover', borderRadius: '0.65rem' }} /><div style={{ display: 'flex', gap: '0.65rem', marginTop: '0.8rem' }}><button type="button" className="btn-primary" onClick={capturePhoto}>Take photo</button><button type="button" className="btn-outline" onClick={stopCamera}>Cancel</button></div></div>}
          <canvas ref={canvasRef} hidden />
          <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'grid', gap: '1rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
              {[['full_name', 'Name', true], ['headline', 'Headline'], ['profession', 'Profession', true], ['location', 'Location'], ['country', 'Country'], ['years_experience', 'Years of experience', false, 'number']].map(([name, label, isRequired, type = 'text']) => <label key={name} style={{ display: 'grid', gap: '0.4rem', fontWeight: 650 }}>{label}<input type={type} min={type === 'number' ? '0' : undefined} style={inputStyle} {...register(name, isRequired ? { validate: required } : {})} />{errors[name] && <small style={{ color: '#fca5a5' }}>{errors[name].message}</small>}</label>)}
            </div>
            <label style={{ display: 'grid', gap: '0.4rem', fontWeight: 650 }}>Bio<textarea rows="4" style={inputStyle} {...register('bio')} /></label>
            <label style={{ display: 'grid', gap: '0.4rem', fontWeight: 650 }}>Skills <small style={{ color: '#94a3b8', fontWeight: 400 }}>Separate with commas</small><input style={inputStyle} {...register('skills')} /></label>
            <label style={{ display: 'grid', gap: '0.4rem', fontWeight: 650 }}>Highlights <small style={{ color: '#94a3b8', fontWeight: 400 }}>One short highlight per line, e.g. “AWS certified”</small><textarea rows="3" style={inputStyle} {...register('highlights')} /></label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}><label style={{ display: 'grid', gap: '0.4rem', fontWeight: 650 }}>LinkedIn URL<input type="url" placeholder="https://linkedin.com/in/your-name" style={inputStyle} {...register('linkedin_url')} /></label><label style={{ display: 'grid', gap: '0.4rem', fontWeight: 650 }}>Portfolio URL<input type="url" placeholder="https://your-site.com" style={inputStyle} {...register('portfolio_url')} /></label></div>
            <div style={{ padding: '1rem', borderRadius: '0.9rem', border: '1px solid rgba(37, 211, 102, 0.3)', background: 'rgba(37, 211, 102, 0.07)' }}><strong>WhatsApp contact</strong><p style={{ color: '#94a3b8', margin: '0.35rem 0 0.8rem', fontSize: '0.9rem' }}>Add your international number so people can open a WhatsApp conversation directly from your profile.</p><input type="tel" placeholder="e.g. +254712345678" style={inputStyle} {...register('phone_number')} /><label style={{ display: 'flex', gap: '0.6rem', alignItems: 'center', marginTop: '0.8rem', color: '#d1fae5' }}><input type="checkbox" {...register('show_whatsapp')} /> Show a “Chat on WhatsApp” link on my public profile</label></div>
            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', flexWrap: 'wrap' }}><Link className="btn-outline" to="/dashboard">Cancel</Link><button type="submit" className="btn-primary" disabled={isSubmitting}>{isSubmitting ? 'Saving…' : 'Save profile'}</button></div>
          </form>
        </section>
      </main>
    </>
  )
}
