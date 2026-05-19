/**
 * 报修管理模块前端测试代码
 * @author 结对小组 - 前端测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import {
  getRepairList,
  submitRepair,
  handleRepair,
  deleteRepair
} from '../src/api/repair'

vi.mock('../src/utils/request', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn()
  }
}))

import request from '../src/utils/request'

describe('报修管理模块测试', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('获取报修记录', () => {
    it('应该成功获取报修记录列表', async () => {
      const mockResponse = {
        code: 200,
        data: [
          { id: 1, room_number: '101', repair_type: '水电', status: 0 },
          { id: 2, room_number: '102', repair_type: '空调', status: 1 }
        ]
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getRepairList()
      
      expect(result.data).toHaveLength(2)
    })
  })

  describe('提交报修', () => {
    it('应该成功提交报修', async () => {
      const mockResponse = {
        code: 200,
        message: '报修提交成功'
      }
      request.post.mockResolvedValue(mockResponse)

      const repairData = {
        room_id: 1,
        repair_type: '水电',
        description: '灯不亮了'
      }
      const result = await submitRepair(repairData)
      
      expect(result.message).toBe('报修提交成功')
    })
  })

  describe('处理报修', () => {
    it('应该成功处理报修', async () => {
      const mockResponse = {
        code: 200,
        message: '处理成功'
      }
      request.post.mockResolvedValue(mockResponse)

      const handleData = { status: 2, handle_result: '已修复' }
      const result = await handleRepair(1, handleData)
      
      expect(request.post).toHaveBeenCalledWith('/repair/handle/1', handleData)
      expect(result.message).toBe('处理成功')
    })
  })
})
