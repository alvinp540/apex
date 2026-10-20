export default function MentorsOrganization({ org }) {
  return (
    <div style={{ padding: '0.75rem', border: '1px solid var(--color-border)', borderRadius: '6px' }}>
      <strong>{org.name}</strong>
      <div style={{ fontSize: '0.9rem', color: 'var(--color-muted)' }}>{org.mentors.length} mentor(s)</div>
      <div style={{ marginTop: '0.5rem' }}>
        {org.mentors.map((m) => (
          <div key={m.id} style={{ padding: '0.35rem 0', borderBottom: '1px solid rgba(0,0,0,0.04)' }}>
            <div style={{ fontWeight: 600 }}>{m.user?.username || m.user?.email}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--color-muted)' }}>{(m.skills || []).join(', ')}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
