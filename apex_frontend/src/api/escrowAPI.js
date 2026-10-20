import api from './axiosInstance'

export const fundEscrow = (data) => api.post('/escrow/fund/', data)
export const releaseEscrow = (id) => api.post(`/escrow/release/${id}/`)
export const disputeEscrow = (id) => api.post(`/escrow/dispute/${id}/`)
export const getEscrow = (id) => api.get(`/escrow/${id}/`)
