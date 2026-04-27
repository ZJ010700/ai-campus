import request from './request'

export function getPosts(params) {
  return request.get('/community/posts', { params })
}

export function getPostDetail(id) {
  return request.get(`/community/posts/${id}`)
}

export function createPost(data) {
  return request.post('/community/posts', data)
}

export function updatePost(id, data) {
  return request.put(`/community/posts/${id}`, data)
}

export function deletePost(id) {
  return request.delete(`/community/posts/${id}`)
}

export function likePost(id) {
  return request.post(`/community/posts/${id}/like`)
}

export function unlikePost(id) {
  return request.delete(`/community/posts/${id}/like`)
}

export function getComments(postId, params) {
  return request.get(`/community/posts/${postId}/comments`, { params })
}

export function createComment(postId, data) {
  return request.post(`/community/posts/${postId}/comments`, data)
}

export function deleteComment(postId, commentId) {
  return request.delete(`/community/posts/${postId}/comments/${commentId}`)
}

export function getTopics() {
  return request.get('/community/topics')
}
