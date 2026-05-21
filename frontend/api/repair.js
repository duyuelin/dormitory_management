import request from '../utils/request'

export const getRepairList = (params) => request.get('/repair/list', { params })
export const submitRepair = (data) => request.post('/repair/submit', data)
export const handleRepair = (id, data) => request.post(`/repair/handle/${id}`, data)
export const deleteRepair = (id) => request.delete(`/repair/delete/${id}`)
