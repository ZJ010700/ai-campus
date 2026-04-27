<template>
  <div class="module-card" @click="$emit('click')">
    <div class="module-card__icon" :style="{ backgroundColor: iconBg }">
      <van-icon :name="icon" size="24" color="white" />
    </div>
    <div class="module-card__info">
      <span class="module-card__title">{{ title }}</span>
      <span class="module-card__desc">{{ description }}</span>
    </div>
    <van-icon name="arrow" color="var(--text-placeholder)" size="16" />
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: 'apps-o'
  },
  iconBg: {
    type: String,
    default: 'var(--primary-color)'
  }
})

defineEmits(['click'])
</script>

<style scoped>
.module-card {
  display: flex;
  align-items: center;
  padding: var(--spacing-lg);
  background-color: var(--bg-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.module-card:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-md);
}

.module-card__icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
}

.module-card__info {
  flex: 1;
  min-width: 0;
}

.module-card__title {
  display: block;
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.module-card__desc {
  display: block;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}
</style>
