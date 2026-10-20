import api from './axiosInstance'

export const getMyProfile = () => api.get('/profiles/')
export const updateProfile = (data) => api.patch('/profiles/', data)
export const uploadAvatar = (formData) =>
  api.post('/profiles/avatar/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
export const getPublicProfile = (userId) => api.get(`/profiles/${userId}/`)
export const setAvailability = (availability) => api.patch('/profiles/availability/', { availability })
export const sendPresence = (online) => api.post('/profiles/presence/', { online })
