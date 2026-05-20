import request from '../utils/request'

export const getCheckInList = (params) => request.get('/checkin/list', { params })
export const checkIn = (data) => request.post('/checkin/check-in', data)
export const checkOut = (id) => request.post(`/checkin/check-out/${id}`)
export const getStudentCheckIn = (id) => request.get(`/checkin/student/${id}`)
