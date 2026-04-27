import axios from 'axios'
import { getToken, removeToken } from '@/utils/auth'
import router from '@/router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求取消控制器映射
const pendingRequests = new Map()

function generateRequestKey(config) {
  const { method, url, params, data } = config
  return [method, url, JSON.stringify(params), JSON.stringify(data)].join('&')
}

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 自动添加 token
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 请求取消：防止重复请求
    const requestKey = generateRequestKey(config)
    if (pendingRequests.has(requestKey)) {
      const cancel = pendingRequests.get(requestKey)
      cancel('请求已取消：重复请求')
      pendingRequests.delete(requestKey)
    }

    config.cancelToken = new axios.CancelToken((cancel) => {
      pendingRequests.set(requestKey, cancel)
    })

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const requestKey = generateRequestKey(response.config)
    pendingRequests.delete(requestKey)

    const res = response.data

    // 如果后端返回的 code 不是 200/0，则视为错误
    if (res.code !== undefined && res.code !== 200 && res.code !== 0) {
      const errMsg = res.message || '请求失败'
      if (res.code === 401) {
        handleUnauthorized()
      }
      return Promise.reject(new Error(errMsg))
    }

    return res
  },
  (error) => {
    if (axios.isCancel(error)) {
      console.warn(error.message)
      return Promise.reject(error)
    }

    if (error.response) {
      const { status, data } = error.response
      const message = data?.message || getDefaultMessage(status)

      switch (status) {
        case 401:
          handleUnauthorized()
          break
        case 403:
          showToast('没有权限访问')
          break
        case 404:
          showToast('请求的资源不存在')
          break
        case 500:
          showToast('服务器内部错误')
          break
        default:
          showToast(message)
      }
    } else if (error.code === 'ECONNABORTED') {
      showToast('请求超时，请稍后重试')
    } else {
      showToast('网络连接异常，请检查网络')
    }

    return Promise.reject(error)
  }
)

function handleUnauthorized() {
  removeToken()
  router.push({
    name: 'Login',
    query: { redirect: router.currentRoute.value.fullPath }
  })
}

function getDefaultMessage(status) {
  const messages = {
    400: '请求参数错误',
    401: '未授权，请重新登录',
    403: '拒绝访问',
    404: '请求资源不存在',
    408: '请求超时',
    500: '服务器内部错误',
    502: '网关错误',
    503: '服务不可用',
    504: '网关超时'
  }
  return messages[status] || `请求失败 (${status})`
}

function showToast(message) {
  // 使用 Vant 的 Toast（延迟导入避免循环依赖）
  import('vant').then(({ showToast }) => {
    showToast({
      message,
      position: 'bottom',
      duration: 2000
    })
  })
}

export default request
