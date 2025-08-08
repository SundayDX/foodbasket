import request from '@/utils/request'
import type { LoginParams, LoginResult, UserInfo } from '@/types/auth'

export async function login(data: LoginParams): Promise<LoginResult> {
  const response = await request<LoginResult>({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
  return response.data
}

export async function logout(): Promise<void> {
  const response = await request<void>({
    url: '/api/v1/auth/logout',
    method: 'post'
  })
  return response.data
}

export async function getUserInfo(): Promise<UserInfo> {
  const response = await request<UserInfo>({
    url: '/api/v1/auth/user-info',
    method: 'get'
  })
  return response.data
}
