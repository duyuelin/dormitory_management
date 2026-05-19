/**
 * 学生管理模块前端测试代码
 * @author 结对小组 - 前端测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import {
  getStudentList,
  getStudent,
  addStudent,
  updateStudent,
  deleteStudent
} from '../src/api/student'

vi.mock('../src/utils/request', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

import request from '../src/utils/request'

describe('学生管理模块测试', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('获取学生列表', () => {
    it('应该成功获取学生列表', async () => {
      const mockResponse = {
        code: 200,
        data: [
          { id: 1, student_id: '2024001001', name: '张三', status: 2 },
          { id: 2, student_id: '2024001002', name: '李四', status: 1 }
        ]
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getStudentList()
      
      expect(result.data).toHaveLength(2)
    })
  })

  describe('添加学生', () => {
    it('应该成功添加学生', async () => {
      const mockResponse = {
        code: 200,
        message: '添加成功'
      }
      request.post.mockResolvedValue(mockResponse)

      const studentData = {
        student_id: '2024001003',
        name: '王五',
        gender: '男'
      }
      const result = await addStudent(studentData)
      
      expect(result.message).toBe('添加成功')
    })
  })
})
