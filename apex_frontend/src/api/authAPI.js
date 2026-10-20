import api from './axiosInstance'

export const register = (data) => api.post('/auth/register/', data)
export const login = (data) => api.post('/auth/login/', data)
export const logout = (refresh) => api.post('/auth/logout/', { refresh })
export const getMe = () => api.get('/auth/me/')
export const refreshToken = (refresh) => api.post('/auth/token/refresh/', { refresh })
export const requestPasswordReset = (email) => api.post('/auth/password/reset/', { email })
export const confirmPasswordReset = (token, new_password) =>
  api.post('/auth/password/reset/confirm/', { token, new_password })
export const verifyEmail = (token) => api.get(`/auth/email/verify/${token}/`)
