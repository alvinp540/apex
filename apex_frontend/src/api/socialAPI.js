import api from './axiosInstance'

export const getPosts = () => api.get('/social/posts/')
export const createPost = (body) => api.post('/social/posts/', { body })
export const togglePostLike = (postId) => api.post(`/social/posts/${postId}/like/`)
export const addPostComment = (postId, body) => api.post(`/social/posts/${postId}/comments/`, { body })
