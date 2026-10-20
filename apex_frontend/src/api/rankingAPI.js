import api from './axiosInstance'

export const getGlobalRankings = (params) => api.get('/rankings/global/', { params })
export const getProfessionRankings = (profession, params) =>
  api.get(`/rankings/profession/${profession}/`, { params })
export const getCountryRankings = (code, params) =>
  api.get(`/rankings/country/${code}/`, { params })
export const getMyRanking = () => api.get('/rankings/me/')
