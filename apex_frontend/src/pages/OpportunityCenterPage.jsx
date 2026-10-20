import { useState } from 'react'
import Navbar from '../components/common/Navbar'
import OpportunityFeed from '../components/dashboard/OpportunityFeed'
import AvailabilityToggle from '../components/dashboard/AvailabilityToggle'

export default function OpportunityCenterPage() {
  const [filters, setFilters] = useState({ profession: '', skill: '', min_merit: '' })
  return (
    <>
      <Navbar />
      <div className="page-container">
        <h2 style={{ marginBottom: '1rem' }}>Opportunity Center</h2>
        <div style={{ marginBottom: '1.5rem' }}>
          <AvailabilityToggle />
        </div>
        <div className="card" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem', marginBottom: '1.5rem' }}>
          <input placeholder="Profession" value={filters.profession} onChange={(event) => setFilters({ ...filters, profession: event.target.value })} />
          <input placeholder="Skill" value={filters.skill} onChange={(event) => setFilters({ ...filters, skill: event.target.value })} />
          <input type="number" min="0" placeholder="Minimum merit score" value={filters.min_merit} onChange={(event) => setFilters({ ...filters, min_merit: event.target.value })} />
        </div>
        <OpportunityFeed filters={filters} />
      </div>
    </>
  )
}
