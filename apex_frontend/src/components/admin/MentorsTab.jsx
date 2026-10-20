import { useState, useEffect } from 'react'
import MentorsOrganization from './MentorsOrganization'
import { listMentors, listMentorOrgs } from '../../api/mentorsAPI'
import { useAuth } from '../../context/AuthContext'

export default function MentorsTab() {
  const { user } = useAuth()
  const [view, setView] = useState('mentors')
  const [mentors, setMentors] = useState([])
  const [orgs, setOrgs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    const fetch = async () => {
      setLoading(true)
      try {
        const [m, o] = await Promise.all([listMentors(), listMentorOrgs()])
        if (!mounted) return
        setMentors(m)
        setOrgs(o)
      } catch (e) {
        console.error(e)
      } finally { if (mounted) setLoading(false) }
    }
    fetch()
    return () => { mounted = false }
  }, [])

  return (
    <div>
      <h3>Mentors</h3>
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <button onClick={() => setView('mentors')} style={{ background: view === 'mentors' ? 'var(--color-primary)' : 'var(--color-border)', color: view === 'mentors' ? '#fff' : undefined }}>Mentors</button>
        <button onClick={() => setView('organizations')} style={{ background: view === 'organizations' ? 'var(--color-primary)' : 'var(--color-border)', color: view === 'organizations' ? '#fff' : undefined }}>Organizations</button>
      </div>

      {view === 'mentors' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: '1rem' }}>
          <div>
            <h4>Active Mentors</h4>
            {loading && <div>Loading mentors…</div>}
            {!loading && mentors.length === 0 && <div>No mentors found.</div>}
            {!loading && mentors.map((m) => (
              <div key={m.id} style={{ padding: '0.75rem', border: '1px solid var(--color-border)', borderRadius: '6px', marginBottom: '0.5rem' }}>
                <strong>{m.user?.username || m.user?.email || 'Unknown'}</strong>
                <div>Tier: {m.tier || '—'}</div>
                <div>Consistency: {m.consistency_score != null ? `${m.consistency_score.toFixed(1)}%` : '—'}</div>
                <div>Skills: {(m.skills || []).join(', ')}</div>
                {(user?.is_admin || user?.role === 'admin') && (
                  <div style={{ marginTop: '0.5rem' }}><small style={{ color: 'var(--color-muted)' }}>Admin view: organization — {m.organization?.name}</small></div>
                )}
              </div>
            ))}

            <h4 style={{ marginTop: '1rem' }}>Why 1000 Kes Tier Matters</h4>
            <ol>
              <li>Certification and skills</li>
              <li>Higher deployed opportunities and consortiums</li>
              <li>Higher marketing to bigger mid-sized firms</li>
              <li>Better mentorship and professional tutoring</li>
              <li>Better reputation</li>
              <li>Access to capability graph</li>
            </ol>

            <h4>What Mentors Will Teach</h4>
            <ol>
              <li>Answers informed by student feedback</li>
              <li>How Apex works</li>
              <li>Referral team processes and building referrals for retention</li>
              <li>About Apex capability and offerings</li>
              <li>Apex invitations and community access</li>
            </ol>
          </div>

          <aside style={{ padding: '0.75rem', border: '1px solid var(--color-border)', borderRadius: '6px' }}>
            <h4>Structure & Mentorship Rules</h4>
            <ul>
              <li>Apex cohorts: 20, 50, 100 people</li>
              <li>A mentor may choose up to 20 mentees</li>
              <li>Mentees should include struggling, slow-growth, low participation users</li>
              <li>Mentorship trail registration and active partner growth via Zoom & communities</li>
              <li>Active mentors earn mentorship merit score (affects deployments & payouts)</li>
              <li>Teams/consortiums assemble for deployments under MSAs</li>
            </ul>
          </aside>
        </div>
      )}

      {view === 'organizations' && (
        <div>
          <h4>Mentoring Organizations</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '0.75rem' }}>
            {loading && <div>Loading…</div>}
            {!loading && orgs.map((org) => (
              <MentorsOrganization key={org.id} org={{ id: org.id, name: org.name, mentors: org.mentors || [] }} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
