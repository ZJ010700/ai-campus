<template>
  <div class="profile-page">
    <!-- 用户信息头部 -->
    <div class="profile-page__header">
      <div class="profile-page__user">
        <van-image
          round
          width="64"
          height="64"
          :src="userStore.avatar"
          fit="cover"
        >
          <template #error>
            <div class="profile-page__avatar-placeholder">
              <van-icon name="user-o" size="32" />
            </div>
          </template>
        </van-image>
        <div class="profile-page__info">
          <h2 class="profile-page__name">{{ userStore.username || '未登录' }}</h2>
          <p class="profile-page__id" v-if="userStore.userInfo">
            学号：{{ userStore.userInfo.student_id || '--' }}
          </p>
        </div>
        <van-icon name="setting-o" size="22" color="white" @click="router.push('/settings')" />
      </div>

      <!-- 统计 -->
      <div class="profile-page__stats">
        <div class="profile-page__stat">
          <span class="profile-page__stat-num">{{ stats.conversations }}</span>
          <span class="profile-page__stat-label">对话</span>
        </div>
        <div class="profile-page__stat">
          <span class="profile-page__stat-num">{{ stats.posts }}</span>
          <span class="profile-page__stat-label">帖子</span>
        </div>
        <div class="profile-page__stat">
          <span class="profile-page__stat-num">{{ stats.likes }}</span>
          <span class="profile-page__stat-label">获赞</span>
        </div>
      </div>
    </div>

    <!-- 功能菜单 -->
    <div class="profile-page__menu">
      <van-cell-group inset>
        <van-cell
          title="我的对话"
          icon="chat-o"
          is-link
          @click="router.push('/chat')"
        />
        <van-cell
          title="我的帖子"
          icon="records-o"
          is-link
          @click="goToMyPosts"
        />
        <van-cell
          title="我的收藏"
          icon="like-o"
          is-link
          @click="showToast('收藏功能开发中')"
        />
      </van-cell-group>

      <van-cell-group inset style="margin-top: 12px;">
        <van-cell
          title="意见反馈"
          icon="comment-o"
          is-link
          @click="goToFeedback"
        />
        <van-cell
          title="关于我们"
          icon="info-o"
          is-link
          @click="showAbout"
        />
        <van-cell
          title="设置"
          icon="setting-o"
          is-link
          @click="router.push('/settings')"
        />
      </van-cell-group>

      <div class="profile-page__logout" style="margin-top: 24px;">
        <van-button
          round
          block
          plain
          type="danger"
          @click="handleLogout"
        >
          退出登录
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showToast } from 'vant'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const stats = reactive({
  conversations: 12,
  posts: 5,
  likes: 28
})

function goToMyPosts() {
  router.push('/community')
}

function goToFeedback() {
  router.push({ path: '/chat', query: { prompt: '我要提交意见反馈' } })
}

function showAbout() {
  showDialog({
    title: '关于 AI+Campus',
    message: 'AI+Campus 校园智能服务助手 v1.0.0\n\n致力于为大学生提供便捷的校园生活服务。',
    confirmButtonText: '知道了'
  })
}

async function handleLogout() {
  try {
    await showDialog({
      title: '提示',
      message: '确定要退出登录吗？',
      showCancelButton: true,
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    userStore.logout()
    showToast({ message: '已退出登录', type: 'success' })
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: calc(60px + var(--safe-bottom));
}

.profile-page__header {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  padding: calc(var(--safe-top) + 20px) var(--spacing-xl) var(--spacing-xl);
  border-radius: 0 0 var(--radius-xl) var(--radius-xl);
}

.profile-page__user {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.profile-page__avatar-placeholder {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-round);
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: var(--spacing-md);
}

.profile-page__info {
  flex: 1;
}

.profile-page__name {
  font-size: var(--font-xxl);
  font-weight: 700;
  color: white;
  margin-bottom: 2px;
}

.profile-page__id {
  font-size: var(--font-sm);
  color: rgba(255, 255, 255, 0.8);
}

.profile-page__stats {
  display: flex;
  justify-content: space-around;
  background: rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
}

.profile-page__stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-page__stat-num {
  font-size: var(--font-xl);
  font-weight: 700;
  color: white;
}

.profile-page__stat-label {
  font-size: var(--font-xs);
  color: rgba(255, 255, 255, 0.8);
  margin-top: 2px;
}

.profile-page__menu {
  padding: var(--spacing-lg) 0;
}

.profile-page__logout {
  padding: 0 var(--spacing-xl);
}
</style>
