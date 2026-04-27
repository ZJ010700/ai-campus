import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chat/:id',
    name: 'ChatDetail',
    component: () => import('@/views/Chat.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/academic',
    name: 'Academic',
    component: () => import('@/views/Academic.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/campus',
    name: 'CampusInfo',
    component: () => import('@/views/CampusInfo.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/daily',
    name: 'DailyService',
    component: () => import('@/views/DailyService.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/community',
    name: 'Community',
    component: () => import('@/views/Community.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/community/publish',
    name: 'CommunityPublish',
    component: () => import('@/views/CommunityPublish.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/community/:id',
    name: 'CommunityDetail',
    component: () => import('@/views/CommunityDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mental',
    name: 'MentalHealth',
    component: () => import('@/views/MentalHealth.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = getToken()
  if (to.meta.requiresAuth !== false && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && token) {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
