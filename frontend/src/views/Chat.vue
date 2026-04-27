<template>
  <div class="chat-page">
    <!-- 顶部导航 -->
    <van-nav-bar
      :title="navTitle"
      left-arrow
      @click-left="goBack"
      :border="false"
    >
      <template #right>
        <van-icon name="plus" size="20" @click="showNewChat" />
      </template>
    </van-nav-bar>

    <!-- 功能模块切换 -->
    <div class="chat-page__modules" v-if="!chatStore.currentConversationId">
      <div class="chat-page__module-tabs">
        <div
          v-for="mod in moduleList"
          :key="mod.key"
          class="chat-page__module-tab"
          :class="{ 'chat-page__module-tab--active': currentModule === mod.key }"
          @click="switchModule(mod.key)"
        >
          <van-icon :name="mod.icon" size="18" />
          <span>{{ mod.name }}</span>
        </div>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="chat-page__messages" ref="messagesRef" v-if="chatStore.currentConversationId">
      <div class="chat-page__messages-inner">
        <ChatBubble
          v-for="msg in chatStore.messages"
          :key="msg.id"
          :message="msg"
          :is-streaming="chatStore.isStreaming && msg === chatStore.messages[chatStore.messages.length - 1]"
        />

        <!-- AI 正在输入指示器 -->
        <div class="chat-page__typing" v-if="chatStore.sendingMessage">
          <div class="chat-page__typing-avatar">
            <div class="chat-page__typing-icon">AI</div>
          </div>
          <div class="chat-page__typing-dots">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 欢迎界面（无对话时） -->
    <div class="chat-page__welcome" v-if="!chatStore.currentConversationId">
      <div class="chat-page__welcome-icon">
        <van-icon name="chat-o" size="48" color="var(--primary-color)" />
      </div>
      <h3>你好，我是 AI+Campus 助手</h3>
      <p>选择一个功能模块开始对话，或直接输入你的问题</p>

      <!-- 快捷问题 -->
      <div class="chat-page__suggestions">
        <div
          v-for="sug in suggestions"
          :key="sug"
          class="chat-page__suggestion"
          @click="quickSend(sug)"
        >
          {{ sug }}
        </div>
      </div>

      <!-- 最近对话 -->
      <ConversationList
        :conversations="chatStore.sortedConversations"
        :current-id="chatStore.currentConversationId"
        @select="openConversation"
        @delete="chatStore.removeConversation"
        @new-chat="createNewChat"
      />
    </div>

    <!-- 输入框 -->
    <ChatInput
      v-if="chatStore.currentConversationId"
      :disabled="chatStore.sendingMessage"
      placeholder="输入消息..."
      @send="handleSend"
    />

    <!-- 底部新对话输入框 -->
    <div class="chat-page__bottom-input" v-if="!chatStore.currentConversationId">
      <div class="chat-page__bottom-input-wrap">
        <input
          v-model="quickInput"
          placeholder="输入你想问的问题..."
          @keydown.enter="quickSendFromInput"
        />
        <button class="chat-page__send-btn" @click="quickSendFromInput">
          <van-icon name="guide-o" size="20" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { useAppStore } from '@/stores/app'
import ChatBubble from '@/components/ChatBubble.vue'
import ChatInput from '@/components/ChatInput.vue'
import ConversationList from '@/components/ConversationList.vue'

const router = useRouter()
const route = useRoute()
const chatStore = useChatStore()
const appStore = useAppStore()

const messagesRef = ref(null)
const quickInput = ref('')
const currentModule = ref('general')

const moduleList = [
  { key: 'general', name: '通用', icon: 'chat-o' },
  { key: 'academic', name: '学业', icon: 'records-o' },
  { key: 'campus', name: '校园', icon: 'location-o' },
  { key: 'daily', name: '日常', icon: 'shop-o' },
  { key: 'mental', name: '心理', icon: 'smile-o' }
]

const suggestions = [
  '今天有什么课？',
  '食堂今天吃什么？',
  '图书馆怎么走？',
  '最近有什么校园活动？'
]

const navTitle = computed(() => {
  if (chatStore.currentConversation) {
    return chatStore.currentConversation.title || 'AI 对话'
  }
  return 'AI 对话'
})

function goBack() {
  if (chatStore.currentConversationId) {
    chatStore.clearCurrentChat()
  } else {
    router.push('/')
  }
}

function switchModule(mod) {
  currentModule.value = mod
  appStore.setModule(mod)
}

async function showNewChat() {
  await createNewChat()
}

async function createNewChat() {
  try {
    await chatStore.newConversation(currentModule.value)
    scrollToBottom()
  } catch (e) {
    console.error(e)
  }
}

async function openConversation(conv) {
  await chatStore.loadMessages(conv.id)
  await nextTick()
  scrollToBottom()
}

async function handleSend(content) {
  await chatStore.send(content)
  await nextTick()
  scrollToBottom()
}

function quickSend(text) {
  quickInput.value = text
  quickSendFromInput()
}

async function quickSendFromInput() {
  const text = quickInput.value.trim()
  if (!text) return
  quickInput.value = ''
  try {
    await chatStore.newConversation(currentModule.value)
    await chatStore.send(text)
    await nextTick()
    scrollToBottom()
  } catch (e) {
    console.error(e)
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

// 监听消息变化自动滚动
watch(
  () => chatStore.messages.length,
  () => {
    scrollToBottom()
  }
)

onMounted(async () => {
  appStore.setPageTitle('AI 对话')
  try {
    await chatStore.loadConversations()
    // 如果路由有 id 参数，打开对应对话
    if (route.params.id) {
      await chatStore.loadMessages(route.params.id)
      await nextTick()
      scrollToBottom()
    }
  } catch (e) {
    console.error('加载对话失败:', e)
  }
})
</script>

<style scoped>
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
}

.chat-page__modules {
  background-color: var(--bg-white);
  border-bottom: 1px solid var(--border-color);
}

.chat-page__module-tabs {
  display: flex;
  overflow-x: auto;
  padding: var(--spacing-sm) var(--spacing-md);
  gap: var(--spacing-sm);
  -webkit-overflow-scrolling: touch;
}

.chat-page__module-tabs::-webkit-scrollbar {
  display: none;
}

.chat-page__module-tab {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border-radius: 16px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  background-color: var(--bg-gray);
  cursor: pointer;
  transition: all 0.2s;
}

.chat-page__module-tab--active {
  background-color: var(--primary-color);
  color: white;
}

.chat-page__messages {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: var(--spacing-md) 0;
}

.chat-page__welcome {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.chat-page__welcome {
  text-align: center;
  padding: 40px var(--spacing-xl) 20px;
}

.chat-page__welcome-icon {
  margin-bottom: var(--spacing-md);
}

.chat-page__welcome h3 {
  font-size: var(--font-xl);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.chat-page__welcome p {
  font-size: var(--font-md);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
}

.chat-page__suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  justify-content: center;
  margin-bottom: var(--spacing-xl);
}

.chat-page__suggestion {
  padding: 8px 16px;
  background-color: var(--bg-white);
  border-radius: 20px;
  font-size: var(--font-sm);
  color: var(--primary-color);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.2s;
}

.chat-page__suggestion:active {
  transform: scale(0.95);
  background-color: var(--primary-bg);
}

/* AI 正在输入动画 */
.chat-page__typing {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
}

.chat-page__typing-avatar {
  margin-right: var(--spacing-sm);
}

.chat-page__typing-icon {
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

.chat-page__typing-dots {
  background-color: var(--bg-white);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  gap: 4px;
  box-shadow: var(--shadow-sm);
}

.chat-page__typing-dots span {
  width: 6px;
  height: 6px;
  border-radius: var(--radius-round);
  background-color: var(--text-placeholder);
  animation: typingBounce 1.4s infinite;
}

.chat-page__typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.chat-page__typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-6px); opacity: 1; }
}

/* 底部输入框 */
.chat-page__bottom-input {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--bg-white);
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-sm) var(--spacing-lg);
  padding-bottom: calc(var(--spacing-sm) + var(--safe-bottom));
  z-index: 100;
}

.chat-page__bottom-input-wrap {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  background-color: var(--bg-gray);
  border-radius: 24px;
  padding: var(--spacing-xs) var(--spacing-xs) var(--spacing-xs) var(--spacing-lg);
}

.chat-page__bottom-input-wrap input {
  flex: 1;
  height: 36px;
  font-size: var(--font-md);
  color: var(--text-primary);
}

.chat-page__bottom-input-wrap input::placeholder {
  color: var(--text-placeholder);
}

.chat-page__send-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-round);
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
