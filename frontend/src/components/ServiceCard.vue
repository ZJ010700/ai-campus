<template>
  <div class="service-card" @click="$emit('click')">
    <div class="service-card__header">
      <div class="service-card__icon-wrap" :style="{ backgroundColor: iconBg }">
        <van-icon :name="icon" size="20" color="white" />
      </div>
      <span class="service-card__title">{{ title }}</span>
    </div>
    <p class="service-card__desc">{{ description }}</p>
    <div class="service-card__footer" v-if="tag">
      <span class="service-card__tag">{{ tag }}</span>
    </div>
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
  },
  tag: {
    type: String,
    default: ''
  }
})

defineEmits(['click'])
</script>

<style scoped>
.service-card {
  background-color: var(--bg-white);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.service-card:active {
  transform: scale(0.98);
}

.service-card__header {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.service-card__icon-wrap {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-sm);
}

.service-card__title {
  font-size: var(--font-md);
  font-weight: 600;
  color: var(--text-primary);
}

.service-card__desc {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: var(--spacing-sm);
}

.service-card__footer {
  display: flex;
  align-items: center;
}

.service-card__tag {
  display: inline-block;
  padding: 2px 8px;
  font-size: var(--font-xs);
  border-radius: 10px;
  background-color: var(--primary-bg);
  color: var(--primary-color);
}
</style>
