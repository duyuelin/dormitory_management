/**
 * 入住管理模块前端测试代码
 * @author 结对小组 - 前端测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import {
  getCheckInList,
  checkIn,
  checkOut,
  getStudentCheckIn
} from '../src/api/checkin'

vi.mock('../src/utils/request', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))

import request from '../src/utils/request'

describe('入住管理模块测试', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('获取入住记录', () => {
    it('应该成功获取入住记录列表', async () => {
      const mockResponse = {
        code: 200,
        data: [
          { id: 1, student_name: '张三', room_number: '101', status: 1 },
          { id: 2, student_name: '李四', room_number: '102', status: 0 }
        ]
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getCheckInList()
      
      expect(request.get).toHaveBeenCalledWith('/checkin/list', { params: undefined })
      expect(result.data).toHaveLength(2)
    })
  })

  describe('办理入住', () => {
    it('应该成功办理入住', async () => {
      const mockResponse = {
        code: 200,
        message: '入住成功'
      }
      request.post.mockResolvedValue(mockResponse)

      const checkInData = {
        student_id: 1,
        room_id: 1,
        bed_number: 1
      }
      const result = await checkIn(checkInData)
      
      expect(request.post).toHaveBeenCalledWith('/checkin/check-in', checkInData)
      expect(result.message).toBe('入住成功')
    })
  })

  describe('办理退宿', () => {
    it('应该成功办理退宿', async () => {
      const mockResponse = {
        code: 200,
        message: '退宿成功'
      }
      request.post.mockResolvedValue(mockResponse)

      const result = await checkOut(1)
      
      expect(request.post).toHaveBeenCalledWith('/checkin/check-out/1')
      expect(result.message).toBe('退宿成功')
    })
  })
})
