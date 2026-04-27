import request from './request'

export function getConversations(params) {
  return request.get('/chat/conversations', { params })
}

export function createConversation(data) {
  return request.post('/chat/conversations', data)
}

export function getConversation(id) {
  return request.get(`/chat/conversations/${id}`)
}

export function deleteConversation(id) {
  return request.delete(`/chat/conversations/${id}`)
}

export function getMessages(conversationId, params) {
  return request.get(`/chat/conversations/${conversationId}/messages`, { params })
}

export function sendMessage(conversationId, data) {
  return request.post(`/chat/conversations/${conversationId}/messages`, data)
}

export function getStreamResponse(conversationId, data, onChunk) {
  const token = localStorage.getItem('token')
  const baseURL = import.meta.env.VITE_API_BASE_URL

  return fetch(`${baseURL}/chat/conversations/${conversationId}/messages/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  }).then(response => {
    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    function read() {
      return reader.read().then(({ done, value }) => {
        if (done) return
        const text = decoder.decode(value, { stream: true })
        if (onChunk) onChunk(text)
        return read()
      })
    }

    return read()
  })
}
