import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export const detectDisease = async (file: File) => {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/detect', form)
  return data
}

export const getDetections = async () => {
  const { data } = await api.get('/detections')
  return data
}

export const getDetection = async (id: number) => {
  const { data } = await api.get(`/detections/${id}`)
  return data
}

export const deleteDetection = async (id: number) => {
  const { data } = await api.delete(`/detections/${id}`)
  return data
}