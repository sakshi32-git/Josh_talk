import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getHealth = () => api.get('/health')

// Leaderboard
export const getLeaderboard = (params = {}) => api.get('/leaderboard', { params })

// Models
export const getModels = () => api.get('/models')
export const createModel = (data) => api.post('/models', data)
export const getModelById = (id) => api.get(`/models/${id}`)
export const deleteModel = (id) => api.delete(`/models/${id}`)

// Recordings
export const getRecordings = () => api.get('/recordings')
export const createRecording = (data) => api.post('/recordings', data)

// Evaluations
export const createEvaluation = (formData) =>
  api.post('/evaluations', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
export const getEvaluations = (params = {}) => api.get('/evaluations', { params })
export const getEvaluationById = (id) => api.get(`/evaluations/${id}`)
export const retryEvaluation = (id) => api.post(`/evaluations/${id}/retry`)

export default api

