import api from './axiosInstance'

export const listPSPRegistrations = (params) => api.get('/cohorts/psp/registrations/', { params }).then(r => r.data)
export const createPSPRegistration = (payload) => api.post('/cohorts/psp/registrations/', payload).then(r => r.data)
export const getPSPRegistration = (id) => api.get(`/cohorts/psp/registrations/${id}/`).then(r => r.data)
export const verifyPSPRegistration = (id, payload) => api.post(`/cohorts/psp/registrations/${id}/verify/`, payload).then(r => r.data)

export default {
  listPSPRegistrations,
  createPSPRegistration,
  getPSPRegistration,
  verifyPSPRegistration,
}
