import request from './request'

export function getSchedule(params) {
  return request.get('/academic/schedule', { params })
}

export function getGrades(params) {
  return request.get('/academic/grades', { params })
}

export function getExamSchedule(params) {
  return request.get('/academic/exams', { params })
}

export function getCourses(params) {
  return request.get('/academic/courses', { params })
}

export function getCourseDetail(id) {
  return request.get(`/academic/courses/${id}`)
}

export function getLibraryInfo() {
  return request.get('/academic/library')
}

export function searchLibrary(keyword) {
  return request.get('/academic/library/search', { params: { keyword } })
}

export function getGPA() {
  return request.get('/academic/gpa')
}
