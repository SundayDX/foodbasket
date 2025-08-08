import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getUserInfo as getUserInfoApi } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/auth'
import type { UserInfo } from '@/types/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(getToken() || '')
  const name = ref('')
  const avatar = ref('')
  const roles = ref<string[]>([])

  // 更新用户信息
  const updateUserInfo = (userInfo: UserInfo) => {
    name.value = userInfo.name
    avatar.value = userInfo.avatar || ''
    roles.value = userInfo.roles
  }

  // 获取用户信息
  const getUserInfo = async () => {
    try {
      const userInfo = await getUserInfoApi()
      updateUserInfo(userInfo)
      return true
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return false
    }
  }

  const login = async (userInfo: { username: string; password: string }) => {
    try {
      const { username, password } = userInfo
      const result = await loginApi({ username: username.trim(), password })
      const { access_token, user } = result
      token.value = access_token
      setToken(access_token)
      updateUserInfo(user)
      return true
    } catch (error) {
      console.error('登录失败:', error)
      return false
    }
  }

  const logout = () => {
    token.value = ''
    name.value = ''
    avatar.value = ''
    roles.value = []
    removeToken()
  }

  const resetToken = () => {
    token.value = ''
    roles.value = []
    removeToken()
  }

  return {
    token,
    name,
    avatar,
    roles,
    login,
    logout,
    resetToken,
    getUserInfo
  }
})