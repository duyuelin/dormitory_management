/**
 * 房间管理模块前端测试代码
 * @author 结对小组 - 前端测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import {
  getRoomList,
  getRoom,
  getAvailableRooms,
  addRoom,
  updateRoom,
  deleteRoom
} from '../src/api/room'

vi.mock('../src/utils/request', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

import request from '../src/utils/request'

describe('房间管理模块测试', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('获取房间列表', () => {
    it('应该成功获取房间列表', async () => {
      const mockResponse = {
        code: 200,
        data: [
          { id: 1, room_number: '101', building_id: 1, total_beds: 4, available_beds: 4 },
          { id: 2, room_number: '102', building_id: 1, total_beds: 4, available_beds: 0 }
        ]
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getRoomList()
      
      expect(request.get).toHaveBeenCalledWith('/room/list', { params: undefined })
      expect(result.data).toHaveLength(2)
    })

    it('应该按宿舍楼筛选房间', async () => {
      const mockResponse = {
        code: 200,
        data: [{ id: 1, room_number: '101', building_id: 1 }]
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getRoomList({ building_id: 1 })
      
      expect(request.get).toHaveBeenCalledWith('/room/list', { params: { building_id: 1 } })
      expect(result.data).toHaveLength(1)
    })
  })

  describe('获取可入住房间', () => {
    it('应该成功获取有空床位的房间', async () => {
      const mockResponse = {
        code: 200,
        data: [
          { id: 1, room_number: '101', available_beds: 2 },
          { id: 2, room_number: '103', available_beds: 4 }
        ]
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getAvailableRooms()
      
      expect(request.get).toHaveBeenCalledWith('/room/available')
      expect(result.data.every(room => room.available_beds > 0)).toBe(true)
    })
  })
})
