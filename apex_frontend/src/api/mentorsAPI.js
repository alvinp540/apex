import api from './axiosInstance'

export const listMentors = (params) => api.get('/profiles/mentors/', { params }).then(r => r.data)
export const listMentorOrgs = () => api.get('/profiles/mentors/organizations/').then(r => r.data)

export default { listMentors, listMentorOrgs }
