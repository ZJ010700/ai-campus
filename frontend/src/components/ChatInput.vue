<template>
  <div class="chat-input">
    <div class="chat-input__wrapper">
      <div class="chat-input__field">
        <textarea
          ref="textareaRef"
          v-model="inputText"
          :placeholder="placeholder"
          :disabled="disabled"
          rows="1"
          @input="autoResize"
          @keydown.enter.exact="handleEnter"
          @compositionstart="isComposing = true"
          @compositionend="isComposing = false"
        ></textarea>
      </div>
      <button
        class="chat-input__send"
        :class="{ 'chat-input__send--active': canSend }"
        :disabled="!canSend"
        @click="handleSend"
      >
        <van-icon name="guide-o" size="20" />
      </button>
    </div>
    <div class="chat-input__safe" :style="{ height: safeBottom }"></div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: '输入消息...'
  },
  maxLength: {
    type: Number,
    default: 500
  }
})

const emit = defineEmits(['send'])

const inputText = ref('')
const textareaRef = ref(null)
const isComposing = ref(false)
const safeBottom = ref('0px')

const canSend = computed(() => {
  return inputText.value.trim().length > 0 && !props.disabled
})

function autoResize() {
  const textarea = textareaRef.value
  if (!textarea) return
  textarea.style.height = 'auto'
  const maxHeight = 100
  textarea.style.height = Math.min(textarea.scrollHeight, maxHeight) + 'px'
}

function handleEnter(e) {
  if (isComposing.value) return
  e.preventDefault()
  handleSend()
}

function handleSend() {
  if (!canSend.value) return
  const text = inputText.value.trim()
  if (text.length > props.maxLength) return
  emit('send', text)
  inputText.value = ''
  nextTick(() => {
    autoResize()
  })
}

function focus() {
  textareaRef.value?.focus()
}

onMounted(() => {
  // 获取安全区域底部高度
  if (typeof window !== 'undefined') {
    safeBottom.value = `env(safe-area-inset-bottom, 0px)`
  }
})

defineExpose({ focus })
</script>

<style scoped>
.chat-input {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--bg-white);
  border-top: 1px solid var(--border-color);
  z-index: 100;
}

.chat-input__wrapper {
  display: flex;
  align-items: flex-end;
  padding: var(--spacing-sm) var(--spacing-lg);
  gap: var(--spacing-sm);
}

.chat-input__field {
  flex: 1;
  background-color: var(--bg-gray);
  border-radius: 20px;
  padding: var(--spacing-sm) var(--spacing-md);
  max-height: 100px;
  overflow-y: auto;
}

.chat-input__field textarea {
  width: 100%;
  height: 24px;
  line-height: 24px;
  font-size: var(--font-md);
  color: var(--text-primary);
  resize: none;
  overflow: hidden;
}

.chat-input__field textarea::placeholder {
  color: var(--text-placeholder);
}

.chat-input__send {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-round);
  background-color: var(--border-color);
  color: var(--text-placeholder);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.chat-input__send--active {
  background-color: var(--primary-color);
  color: white;
}

.chat-input__send:disabled {
  cursor: not-allowed;
}

.chat-input__safe {
  background-color: var(--bg-white);
}
</style>
