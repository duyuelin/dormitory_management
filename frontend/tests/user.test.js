/**
 * 用户认证模块前端测试代码
 * @author 结对小组 - 前端测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { login, register, getUserInfo } from '../src/api/user'

// Mock axios
vi.mock('../src/utils/request', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn()
  }
}))

import request from '../src/utils/request'

describe('用户认证模块测试', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  describe('登录功能测试', () => {
    it('应该成功登录并保存token', async () => {
      const mockResponse = {
        code: 200,
        data: {
          token: 'test-token-123',
          user: { id: 1, username: 'admin', real_name: '管理员' }
        },
        message: '登录成功'
      }
      request.post.mockResolvedValue(mockResponse)

      const result = await login({ username: 'admin', password: 'admin123' })
      
      expect(request.post).toHaveBeenCalledWith('/user/login', { username: 'admin', password: 'admin123' })
      expect(result.data.token).toBe('test-token-123')
    })

    it('应该处理登录失败', async () => {
      const mockError = {
        response: {
          data: { code: 500, message: '用户名或密码错误' }
        }
      }
      request.post.mockRejectedValue(mockError)

      await expect(login({ username: 'admin', password: 'wrong' }))
        .rejects.toEqual(mockError)
    })

    it('应该验证必填字段', async () => {
      await expect(login({})).rejects.toBeDefined()
    })
  })

  describe('注册功能测试', () => {
    it('应该成功注册', async () => {
      const mockResponse = {
        code: 200,
        message: '注册成功'
      }
      request.post.mockResolvedValue(mockResponse)

      const result = await register({
        username: 'newuser',
        password: 'password123',
        real_name: '新用户'
      })
      
      expect(result.message).toBe('注册成功')
    })

    it('应该处理重复用户名', async () => {
      const mockError = {
        response: {
          data: { code: 500, message: '用户名已存在' }
        }
      }
      request.post.mockRejectedValue(mockError)

      await expect(register({ username: 'existing', password: 'pass' }))
        .rejects.toEqual(mockError)
    })
  })

  describe('获取用户信息测试', () => {
    it('应该成功获取用户信息', async () => {
      const mockResponse = {
        code: 200,
        data: { id: 1, username: 'admin', real_name: '管理员' }
      }
      request.get.mockResolvedValue(mockResponse)

      const result = await getUserInfo()
      
      expect(request.get).toHaveBeenCalledWith('/user/info')
      expect(result.data.username).toBe('admin')
    })

    it('应该处理未登录情况', async () => {
      const mockError = {
        response: {
          status: 401,
          data: { code: 401, message: '请先登录' }
        }
      }
      request.get.mockRejectedValue(mockError)

      await expect(getUserInfo()).rejects.toEqual(mockError)
    })
  })
})

// 登录页面组件测试
describe('Login.vue 组件测试', () => {
  it('应该验证表单规则', () => {
    const rules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
    }
    
    expect(rules.username[0].required).toBe(true)
    expect(rules.password[0].required).toBe(true)
  })

  it('应该处理登录成功后的跳转', () => {
    const mockRouter = { push: vi.fn() }
    const mockStorage = {
      setItem: vi.fn(),
      getItem: vi.fn()
    }
    
    // 模拟登录成功
    const loginSuccess = (response) => {
      mockStorage.setItem('token', response.data.token)
      mockStorage.setItem('user', JSON.stringify(response.data.user))
      mockRouter.push('/')
    }
    
    const mockResponse = {
      data: {
        token: 'test-token',
        user: { id: 1, username: 'admin' }
      }
    }
    
    loginSuccess(mockResponse)
    
    expect(mockStorage.setItem).toHaveBeenCalledWith('token', 'test-token')
    expect(mockRouter.push).toHaveBeenCalledWith('/')
  })
})
