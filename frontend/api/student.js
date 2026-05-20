import request from '../utils/request'

export const getStudentList = (params) => request.get('/student/list', { params })
export const getStudent = (id) => request.get(`/student/${id}`)
export const addStudent = (data) => request.post('/student/add', data)
export const updateStudent = (data) => request.put('/student/update', data)
export const deleteStudent = (id) => request.delete(`/student/delete/${id}`)
