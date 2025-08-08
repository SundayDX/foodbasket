// 登录请求参数
export interface LoginParams {
  username: string
  password: string
}

// 用户信息
export interface UserInfo {
  id: number
  username: string
  name: string
  avatar?: string
  roles: string[]
  permissions: string[]
}

// 登录响应结果
export interface LoginResult {
  access_token: string
  user: UserInfo
}

// API 响应格式
export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}