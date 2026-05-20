import request from '../utils/request'

export const getRoomList = (params) => request.get('/room/list', { params })
export const getRoom = (id) => request.get(`/room/${id}`)
export const getAvailableRooms = () => request.get('/room/available')
export const addRoom = (data) => request.post('/room/add', data)
export const updateRoom = (data) => request.put('/room/update', data)
export const deleteRoom = (id) => request.delete(`/room/delete/${id}`)
