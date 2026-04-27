<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
  <TabBar v-if="showTabBar" />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TabBar from '@/components/TabBar.vue'

const route = useRoute()

const showTabBar = computed(() => {
  const hideRoutes = ['/login', '/register', '/chat']
  return !hideRoutes.some(path => route.path.startsWith(path))
})
</script>

<style>
#app {
  width: 100%;
  min-height: 100vh;
  background-color: var(--bg-color);
}
</style>
