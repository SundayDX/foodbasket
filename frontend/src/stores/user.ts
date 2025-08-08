import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(getToken() || '')
  const name = ref('')
  const avatar = ref('')
  const roles = ref<string[]>([])

  const login = async (userInfo: { username: string; password: string }) => {
    try {
      const { username, password } = userInfo
      const response = await loginApi({ username: username.trim(), password })
      const { access_token } = response.data
      token.value = access_token
      setToken(access_token)
      return true
    } catch (error) {
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
    resetToken
  }
})