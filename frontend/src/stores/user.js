import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, register as registerApi, getUserInfo } from '@/api/auth'
import { setToken, removeToken, getToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(getToken() || '')
  const userInfo = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => userInfo.value?.username || '')
  const avatar = computed(() => userInfo.value?.avatar || '')

  async function login(credentials) {
    const res = await loginApi(credentials)
    token.value = res.data.token
    setToken(res.data.token)
    return res
  }

  async function register(data) {
    const res = await registerApi(data)
    return res
  }

  async function fetchUserInfo() {
    try {
      const res = await getUserInfo()
      userInfo.value = res.data
      return res.data
    } catch (e) {
      userInfo.value = null
      throw e
    }
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    removeToken()
  }

  function loadFromStorage() {
    const saved = localStorage.getItem('user_info')
    if (saved) {
      try {
        userInfo.value = JSON.parse(saved)
      } catch {
        userInfo.value = null
      }
    }
  }

  function saveToStorage() {
    if (userInfo.value) {
      localStorage.setItem('user_info', JSON.stringify(userInfo.value))
    } else {
      localStorage.removeItem('user_info')
    }
  }

  // 初始化时加载
  loadFromStorage()

  return {
    token,
    userInfo,
    isLoggedIn,
    username,
    avatar,
    login,
    register,
    fetchUserInfo,
    logout,
    saveToStorage
  }
})
