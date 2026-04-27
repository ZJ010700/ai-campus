<template>
  <div class="home-page">
    <!-- 顶部欢迎区 -->
    <div class="home-page__header">
      <div class="home-page__welcome">
        <div>
          <h2 class="home-page__greeting">{{ greeting }}，{{ userName }}</h2>
          <p class="home-page__desc">今天有什么可以帮你的？</p>
        </div>
        <div class="home-page__avatar" @click="router.push('/profile')">
          <van-image
            round
            width="44"
            height="44"
            :src="userStore.avatar"
            fit="cover"
          >
            <template #error>
              <div class="home-page__avatar-placeholder">
                <van-icon name="user-o" size="22" />
              </div>
            </template>
          </van-image>
        </div>
      </div>
    </div>

    <!-- 功能模块入口 -->
    <div class="home-page__modules">
      <div class="home-page__section-title">功能模块</div>
      <div class="home-page__module-grid">
        <div
          v-for="mod in modules"
          :key="mod.name"
          class="home-page__module-item"
          @click="goToModule(mod)"
        >
          <div class="home-page__module-icon" :style="{ backgroundColor: mod.color }">
            <van-icon :name="mod.icon" size="24" color="white" />
          </div>
          <span class="home-page__module-name">{{ mod.name }}</span>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="home-page__quick">
      <div class="home-page__section-title">快捷操作</div>
      <div class="home-page__quick-list">
        <ModuleCard
          v-for="action in quickActions"
          :key="action.title"
          :title="action.title"
          :description="action.description"
          :icon="action.icon"
          :icon-bg="action.color"
          @click="goToModule(action)"
        />
      </div>
    </div>

    <!-- 最近对话 -->
    <div class="home-page__recent">
      <div class="home-page__section-title">
        <span>最近对话</span>
        <span class="home-page__more" @click="router.push('/chat')">查看全部</span>
      </div>
      <div v-if="recentChats.length > 0">
        <div
          v-for="chat in recentChats"
          :key="chat.id"
          class="home-page__chat-item"
          @click="openChat(chat)"
        >
          <van-icon name="chat-o" size="20" color="var(--primary-color)" />
          <div class="home-page__chat-info">
            <span class="home-page__chat-title">{{ chat.title || '新对话' }}</span>
            <span class="home-page__chat-preview">{{ chat.last_message || '点击继续对话' }}</span>
          </div>
          <span class="home-page__chat-time">{{ formatTime(chat.updated_at) }}</span>
        </div>
      </div>
      <div class="home-page__empty" v-else>
        <van-icon name="chat-o" size="32" color="var(--text-placeholder)" />
        <p>暂无对话记录</p>
        <van-button size="small" round type="primary" @click="startNewChat">
          开始新对话
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import { useAppStore } from '@/stores/app'
import { getGreeting, formatTime } from '@/utils/helpers'
import ModuleCard from '@/components/ModuleCard.vue'

const router = useRouter()
const userStore = useUserStore()
const chatStore = useChatStore()
const appStore = useAppStore()

const greeting = getGreeting()
const userName = computed(() => userStore.username || '同学')

const modules = [
  { name: '学业助手', icon: 'records-o', color: '#4A90D9', path: '/academic', module: 'academic' },
  { name: '校园信息', icon: 'location-o', color: '#07c160', path: '/campus', module: 'campus' },
  { name: '日常服务', icon: 'shop-o', color: '#ff976a', path: '/daily', module: 'daily' },
  { name: '社区交流', icon: 'friends-o', color: '#ee0a24', path: '/community', module: 'community' },
  { name: '心理伙伴', icon: 'smile-o', color: '#ff6034', path: '/mental', module: 'mental' }
]

const quickActions = [
  {
    title: '课表查询',
    description: '查看今日课程安排',
    icon: 'calendar-o',
    color: '#4A90D9',
    path: '/academic'
  },
  {
    title: '成绩查询',
    description: '查看各科成绩与GPA',
    icon: 'chart-trending-o',
    color: '#07c160',
    path: '/academic'
  },
  {
    title: '食堂菜单',
    description: '查看今日食堂推荐',
    icon: 'food-a',
    color: '#ff976a',
    path: '/daily'
  },
  {
    title: '校车时刻',
    description: '查看校车发车时间',
    icon: 'logistics',
    color: '#1989fa',
    path: '/daily'
  }
]

const recentChats = computed(() => {
  return chatStore.sortedConversations.slice(0, 5)
})

function goToModule(mod) {
  if (mod.path) {
    router.push(mod.path)
  }
}

function openChat(chat) {
  router.push(`/chat/${chat.id}`)
}

async function startNewChat() {
  try {
    await chatStore.newConversation()
    router.push('/chat')
  } catch (e) {
    console.error(e)
  }
}

onMounted(async () => {
  appStore.setPageTitle('首页')
  try {
    await chatStore.loadConversations()
    if (userStore.isLoggedIn && !userStore.userInfo) {
      await userStore.fetchUserInfo()
      userStore.saveToStorage()
    }
  } catch (e) {
    console.error('加载首页数据失败:', e)
  }
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: calc(60px + var(--safe-bottom));
}

.home-page__header {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  padding: calc(var(--safe-top) + 20px) var(--spacing-xl) var(--spacing-xl);
  border-radius: 0 0 var(--radius-xl) var(--radius-xl);
}

.home-page__welcome {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.home-page__greeting {
  font-size: var(--font-xxl);
  font-weight: 700;
  color: white;
  margin-bottom: var(--spacing-xs);
}

.home-page__desc {
  font-size: var(--font-md);
  color: rgba(255, 255, 255, 0.8);
}

.home-page__avatar {
  cursor: pointer;
}

.home-page__avatar-placeholder {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-round);
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.home-page__section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  padding: 0 var(--spacing-lg);
}

.home-page__more {
  font-size: var(--font-sm);
  font-weight: 400;
  color: var(--text-secondary);
  cursor: pointer;
}

.home-page__modules {
  padding: var(--spacing-xl) 0 var(--spacing-md);
}

.home-page__module-grid {
  display: flex;
  justify-content: space-around;
  padding: 0 var(--spacing-md);
}

.home-page__module-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
}

.home-page__module-item:active {
  transform: scale(0.95);
}

.home-page__module-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.home-page__module-name {
  font-size: var(--font-sm);
  color: var(--text-primary);
  font-weight: 500;
}

.home-page__quick {
  padding: var(--spacing-md) 0;
}

.home-page__quick-list {
  padding: 0 var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.home-page__recent {
  padding: var(--spacing-md) 0;
}

.home-page__chat-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--bg-white);
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
}

.home-page__chat-item:first-of-type {
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.home-page__chat-item:last-of-type {
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  border-bottom: none;
}

.home-page__chat-item:only-of-type {
  border-radius: var(--radius-lg);
}

.home-page__chat-info {
  flex: 1;
  margin: 0 var(--spacing-md);
  min-width: 0;
}

.home-page__chat-title {
  display: block;
  font-size: var(--font-md);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.home-page__chat-preview {
  display: block;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.home-page__chat-time {
  flex-shrink: 0;
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.home-page__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  gap: var(--spacing-md);
  color: var(--text-placeholder);
}

.home-page__empty p {
  font-size: var(--font-sm);
}
</style>
