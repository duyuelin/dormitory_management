/**
 * 前端测试配置
 * @author 结对小组 - 前端测试
 */
import { vi } from 'vitest'

// 模拟 localStorage
global.localStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn()
}

// 模拟 window
Object.defineProperty(window, 'location', {
  value: {
    href: ''
  },
  writable: true
})
