import Navbar from '../components/common/Navbar'
import MentorsTab from '../components/admin/MentorsTab'

export default function MentorsPage() {
  return (
    <>
      <Navbar />
      <div className="page-container">
        <h2>Mentors</h2>
        <MentorsTab />
      </div>
    </>
  )
}
