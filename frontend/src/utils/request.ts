import type { ApiResponse } from '@/types/auth'

// 模拟网络延迟
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

// Mock 数据
const MOCK_USER = {
  id: 1,
  username: 'admin',
  name: '管理员',
  avatar: '',
  roles: ['admin'],
  permissions: ['*']
}

// Mock 请求函数
async function mockRequest<T>(config: {
  url: string
  method: string
  data?: any
}): Promise<ApiResponse<T>> {
  // 模拟网络延迟 500-1500ms
  await delay(Math.random() * 1000 + 500)

  // Mock 响应数据
  switch (config.url) {
    case '/api/v1/auth/login':
      const { username, password } = config.data
      if (username === 'admin' && password === '123456') {
        return {
          code: 0,
          data: {
            access_token: 'mock_token_' + Date.now(),
            user: MOCK_USER
          } as T,
          message: '登录成功'
        }
      }
      throw new Error('用户名或密码错误')

    case '/api/v1/auth/user-info':
      return {
        code: 0,
        data: MOCK_USER as T,
        message: '获取用户信息成功'
      }

    case '/api/v1/auth/logout':
      return {
        code: 0,
        data: null as T,
        message: '退出登录成功'
      }

    default:
      throw new Error('接口不存在')
  }
}

export default mockRequest