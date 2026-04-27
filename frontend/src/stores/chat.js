import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getConversations,
  createConversation,
  getMessages,
  sendMessage,
  deleteConversation
} from '@/api/chat'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversationId = ref(null)
  const messages = ref([])
  const loading = ref(false)
  const sendingMessage = ref(false)
  const streamingContent = ref('')
  const isStreaming = ref(false)

  const currentConversation = computed(() => {
    return conversations.value.find(c => c.id === currentConversationId.value) || null
  })

  const sortedConversations = computed(() => {
    return [...conversations.value].sort((a, b) => {
      return new Date(b.updated_at) - new Date(a.updated_at)
    })
  })

  async function loadConversations() {
    loading.value = true
    try {
      const res = await getConversations()
      conversations.value = res.data || []
    } catch (e) {
      console.error('加载对话列表失败:', e)
    } finally {
      loading.value = false
    }
  }

  async function loadMessages(conversationId) {
    loading.value = true
    currentConversationId.value = conversationId
    messages.value = []
    try {
      const res = await getMessages(conversationId)
      messages.value = res.data || []
    } catch (e) {
      console.error('加载消息失败:', e)
    } finally {
      loading.value = false
    }
  }

  async function newConversation(module = 'general') {
    try {
      const res = await createConversation({ module })
      const conv = res.data
      conversations.value.unshift(conv)
      currentConversationId.value = conv.id
      messages.value = []
      return conv
    } catch (e) {
      console.error('创建对话失败:', e)
      throw e
    }
  }

  async function send(content) {
    if (!content.trim() || sendingMessage.value) return

    // 如果没有当前对话，先创建一个
    if (!currentConversationId.value) {
      await newConversation()
    }

    // 添加用户消息到列表
    const userMsg = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      created_at: new Date().toISOString()
    }
    messages.value.push(userMsg)

    sendingMessage.value = true
    isStreaming.value = true
    streamingContent.value = ''

    try {
      const res = await sendMessage(currentConversationId.value, {
        content: content.trim()
      })

      // 处理流式响应
      if (res.data && typeof res.data === 'string') {
        // 简单文本响应
        const aiMsg = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: res.data,
          created_at: new Date().toISOString()
        }
        messages.value.push(aiMsg)
      } else if (res.data && res.data.content) {
        const aiMsg = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: res.data.content,
          created_at: new Date().toISOString()
        }
        messages.value.push(aiMsg)
      }

      // 更新对话列表中的最后消息
      const conv = conversations.value.find(c => c.id === currentConversationId.value)
      if (conv) {
        conv.updated_at = new Date().toISOString()
        conv.last_message = content.trim().slice(0, 50)
      }
    } catch (e) {
      console.error('发送消息失败:', e)
      const errMsg = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '抱歉，我暂时无法回复，请稍后再试。',
        created_at: new Date().toISOString(),
        is_error: true
      }
      messages.value.push(errMsg)
    } finally {
      sendingMessage.value = false
      isStreaming.value = false
      streamingContent.value = ''
    }
  }

  async function removeConversation(id) {
    try {
      await deleteConversation(id)
      conversations.value = conversations.value.filter(c => c.id !== id)
      if (currentConversationId.value === id) {
        currentConversationId.value = null
        messages.value = []
      }
    } catch (e) {
      console.error('删除对话失败:', e)
    }
  }

  function clearCurrentChat() {
    currentConversationId.value = null
    messages.value = []
  }

  return {
    conversations,
    currentConversationId,
    messages,
    loading,
    sendingMessage,
    streamingContent,
    isStreaming,
    currentConversation,
    sortedConversations,
    loadConversations,
    loadMessages,
    newConversation,
    send,
    removeConversation,
    clearCurrentChat
  }
})
