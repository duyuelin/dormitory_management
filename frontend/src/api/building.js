import request from '../utils/request'

export const getBuildingList = () => request.get('/building/list')
export const getBuilding = (id) => request.get(`/building/${id}`)
export const addBuilding = (data) => request.post('/building/add', data)
export const updateBuilding = (data) => request.put('/building/update', data)
export const deleteBuilding = (id) => request.delete(`/building/delete/${id}`)
export const getBuildingRooms = (id) => request.get(`/building/${id}/rooms`)
