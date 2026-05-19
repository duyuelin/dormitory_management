/**
 * 宿舍楼管理模块前端测试代码
 * @author 结对小组 - 前端测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import {
  getBuildingList,
  getBuilding,
  addBuilding,
  updateBuilding,
  deleteBuilding,
  getBuildingRooms
} from '../src/api/building'

vi.mock('../src/utils/request', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

import request from '../src/utils/request'

describe('宿舍楼管理模块测试', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('获取宿舍楼列表', () => {
    it('应该成功获取宿舍楼列表', async () => {
      const mockResponse = {
        code: 200,
        data: [
          { id: 1, name: '1号楼', code: 'B001', floors: 6 },
          { id: 2, name: '2号楼', code: 'B002', floors: 5 }
        ]
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getBuildingList()
      
      expect(request.get).toHaveBeenCalledWith('/building/list')
      expect(result.data).toHaveLength(2)
      expect(result.data[0].name).toBe('1号楼')
    })

    it('应该处理空列表', async () => {
      const mockResponse = {
        code: 200,
        data: []
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getBuildingList()
      
      expect(result.data).toHaveLength(0)
    })
  })

  describe('获取宿舍楼详情', () => {
    it('应该成功获取单个宿舍楼', async () => {
      const mockResponse = {
        code: 200,
        data: { id: 1, name: '1号楼', code: 'B001', floors: 6 }
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getBuilding(1)
      
      expect(request.get).toHaveBeenCalledWith('/building/1')
      expect(result.data.name).toBe('1号楼')
    })

    it('应该处理不存在的宿舍楼', async () => {
      const mockError = {
        response: {
          data: { code: 500, message: '宿舍楼不存在' }
        }
      }
      request.get.mockRejectedValue(mockError