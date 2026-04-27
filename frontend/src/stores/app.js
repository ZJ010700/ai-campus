import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const pageTitle = ref('AI+Campus')
  const loading = ref(false)
  const networkStatus = ref(navigator.onLine)
  const currentModule = ref('general')

  function setPageTitle(title) {
    pageTitle.value = title
    document.title = title ? `${title} - AI+Campus` : 'AI+Campus'
  }

  function setLoading(val) {
    loading.value = val
  }

  function setModule(module) {
    currentModule.value = module
  }

  // 监听网络状态
  if (typeof window !== 'undefined') {
    window.addEventListener('online', () => {
      networkStatus.value = true
    })
    window.addEventListener('offline', () => {
      networkStatus.value = false
    })
  }

  return {
    pageTitle,
    loading,
    networkStatus,
    currentModule,
    setPageTitle,
    setLoading,
    setModule
  }
})
