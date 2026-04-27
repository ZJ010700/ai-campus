<template>
  <div class="tab-bar">
    <van-tabbar v-model="active" route active-color="var(--primary-color)" inactive-color="var(--text-secondary)">
      <van-tabbar-item to="/" icon="wap-home-o" name="home">首页</van-tabbar-item>
      <van-tabbar-item to="/chat" icon="chat-o" name="chat">对话</van-tabbar-item>
      <van-tabbar-item to="/community" icon="friends-o" name="community">社区</van-tabbar-item>
      <van-tabbar-item to="/profile" icon="user-o" name="profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const tabMap = {
  '/': 'home',
  '/chat': 'chat',
  '/community': 'community',
  '/profile': 'profile'
}

const active = ref(tabMap[route.path] || 'home')
</script>

<style scoped>
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 999;
}
</style>
