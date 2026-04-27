<template>
  <div class="conversation-list">
    <div class="conversation-list__header">
      <h3 class="conversation-list__title">历史对话</h3>
      <button class="conversation-list__new" @click="$emit('new-chat')">
        <van-icon name="plus" size="16" />
        <span>新对话</span>
      </button>
    </div>

    <div class="conversation-list__body" v-if="conversations.length > 0">
      <div
        v-for="conv in conversations"
        :key="conv.id"
        class="conversation-item"
        :class="{ 'conversation-item--active': conv.id === currentId }"
        @click="$emit('select', conv)"
      >
        <div class="conversation-item__icon">
          <van-icon :name="getModuleIcon(conv.module)" size="20" />
        </div>
        <div class="conversation-item__info">
          <div class="conversation-item__title">{{ conv.title || '新对话' }}</div>
          <div class="conversation-item__preview">
            {{ conv.last_message || '暂无消息' }}
          </div>
        </div>
        <div class="conversation-item__meta">
          <span class="conversation-item__time">{{ formatTime(conv.updated_at) }}</span>
          <button
            class="conversation-item__delete"
            @click.stop="$emit('delete', conv.id)"
          >
            <van-icon name="delete-o" size="16" color="var(--text-placeholder)" />
          </button>
        </div>
      </div>
    </div>

    <div class="conversation-list__empty" v-else>
      <van-icon name="chat-o" size="40" color="var(--text-placeholder)" />
      <p>暂无对话记录</p>
    </div>
  </div>
</template>

<script setup>
import { formatTime } from '@/utils/helpers'

defineProps({
  conversations: {
    type: Array,
    default: () => []
  },
  currentId: {
    type: [String, Number],
    default: null
  }
})

defineEmits(['select', 'delete', 'new-chat'])

function getModuleIcon(module) {
  const icons = {
    general: 'chat-o',
    academic: 'records-o',
    campus: 'location-o',
    daily: 'shop-o',
    community: 'friends-o',
    mental: 'smile-o'
  }
  return icons[module] || 'chat-o'
}
</script>

<style scoped>
.conversation-list__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-lg);
}

.conversation-list__title {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.conversation-list__new {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--primary-color);
  font-size: var(--font-sm);
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid var(--border-light);
}

.conversation-item:active {
  background-color: var(--bg-gray);
}

.conversation-item--active {
  background-color: var(--primary-bg);
}

.conversation-item__icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background-color: var(--primary-bg);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
}

.conversation-item__info {
  flex: 1;
  min-width: 0;
}

.conversation-item__title {
  font-size: var(--font-md);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.conversation-item__preview {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-item__meta {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  margin-left: var(--spacing-sm);
}

.conversation-item__time {
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.conversation-item__delete {
  padding: 4px;
}

.conversation-list__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  color: var(--text-placeholder);
  gap: var(--spacing-sm);
}

.conversation-list__empty p {
  font-size: var(--font-sm);
}
</style>
