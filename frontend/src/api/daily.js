import request from './request'

export function getCanteens() {
  return request.get('/daily/canteens')
}

export function getCanteenMenu(canteenId) {
  return request.get(`/daily/canteens/${canteenId}/menu`)
}

export function getBusSchedule(params) {
  return request.get('/daily/bus', { params })
}

export function getLostFound(params) {
  return request.get('/daily/lost-found', { params })
}

export function createLostFound(data) {
  return request.post('/daily/lost-found', data)
}

export function getRepairService(params) {
  return request.get('/daily/repair', { params })
}

export function submitRepair(data) {
  return request.post('/daily/repair', data)
}

export function getWeather() {
  return request.get('/daily/weather')
}

export function getExpressInfo() {
  return request.get('/daily/express')
}
