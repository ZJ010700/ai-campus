import request from './request'

export function submitFeedback(data) {
  return request.post('/feedback', data)
}

export function getFeedbackList(params) {
  return request.get('/feedback', { params })
}

export function getFeedbackDetail(id) {
  return request.get(`/feedback/${id}`)
}

export function replyFeedback(id, data) {
  return request.post(`/feedback/${id}/reply`, data)
}

export function getFAQ() {
  return request.get('/feedback/faq')
}
