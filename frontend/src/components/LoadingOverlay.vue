<template>
  <transition name="fade">
    <div class="loading-overlay" v-if="visible">
      <div class="loading-overlay__content">
        <van-loading type="spinner" color="var(--primary-color)" size="36" />
        <p class="loading-overlay__text" v-if="text">{{ text }}</p>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  text: {
    type: String,
    default: '加载中...'
  }
})
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-overlay__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

.loading-overlay__text {
  font-size: var(--font-md);
  color: var(--text-secondary);
}
</style>
