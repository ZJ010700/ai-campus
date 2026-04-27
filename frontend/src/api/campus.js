import request from './request'

export function getCampusNews(params) {
  return request.get('/campus/news', { params })
}

export function getCampusNewsDetail(id) {
  return request.get(`/campus/news/${id}`)
}

export function getBuildings() {
  return request.get('/campus/buildings')
}

export function getBuildingDetail(id) {
  return request.get(`/campus/buildings/${id}`)
}

export function getMapLocations(params) {
  return request.get('/campus/map', { params })
}

export function getNotices(params) {
  return request.get('/campus/notices', { params })
}

export function getCalendar(params) {
  return request.get('/campus/calendar', { params })
}

export function searchCampus(keyword) {
  return request.get('/campus/search', { params: { keyword } })
}
