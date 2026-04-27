<template>
  <div class="chat-bubble" :class="[`chat-bubble--${message.role}`]">
    <div class="chat-bubble__avatar" v-if="message.role === 'assistant'">
      <div class="chat-bubble__avatar-icon">AI</div>
    </div>
    <div class="chat-bubble__content">
      <div
        class="chat-bubble__text"
        :class="{ 'chat-bubble__text--streaming': isStreaming }"
        v-html="renderedContent"
      ></div>
      <div class="chat-bubble__time">{{ formattedTime }}</div>
    </div>
    <div class="chat-bubble__avatar" v-if="message.role === 'user'">
      <div class="chat-bubble__avatar-user">
        <van-icon name="user-o" size="18" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { simpleMarkdown, formatTime } from '@/utils/helpers'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  isStreaming: {
    type: Boolean,
    default: false
  }
})

const renderedContent = computed(() => {
  if (props.message.role === 'user') {
    return escapeHtml(props.message.content)
  }
  return simpleMarkdown(props.message.content)
})

const formattedTime = computed(() => {
  return formatTime(props.message.created_at)
})

function escapeHtml(text) {
  if (!text) return ''
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML.replace(/\n/g, '<br>')
}
</script>

<style scoped>
.chat-bubble {
  display: flex;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
  padding: 0 var(--spacing-lg);
  animation: messageSlideIn 0.3s ease;
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-bubble--user {
  flex-direction: row-reverse;
}

.chat-bubble__avatar {
  flex-shrink: 0;
  margin: 0 var(--spacing-sm);
}

.chat-bubble__avatar-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-round);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-xs);
  font-weight: 700;
}

.chat-bubble__avatar-user {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-round);
  background-color: var(--bg-gray);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-bubble__content {
  max-width: 75%;
  min-width: 40px;
}

.chat-bubble__text {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-lg);
  font-size: var(--font-md);
  line-height: 1.6;
  word-break: break-word;
}

.chat-bubble--user .chat-bubble__text {
  background-color: var(--chat-user-bg);
  color: var(--chat-user-text);
  border-top-right-radius: var(--radius-sm);
}

.chat-bubble--assistant .chat-bubble__text {
  background-color: var(--chat-ai-bg);
  color: var(--chat-ai-text);
  border-top-left-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
}

.chat-bubble__text--streaming::after {
  content: '▊';
  animation: cursorBlink 1s infinite;
  margin-left: 2px;
  color: var(--primary-color);
}

@keyframes cursorBlink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.chat-bubble__time {
  font-size: var(--font-xs);
  color: var(--text-placeholder);
  margin-top: var(--spacing-xs);
  padding: 0 4px;
}

.chat-bubble--user .chat-bubble__time {
  text-align: right;
}
</style>
