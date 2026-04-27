<template>
  <div class="community-detail-page">
    <van-nav-bar
      title="帖子详情"
      left-arrow
      @click-left="router.back()"
    />

    <div class="community-detail-page__content" v-if="post">
      <!-- 帖子内容 -->
      <div class="community-detail-page__post">
        <div class="community-detail-page__author">
          <van-image round width="40" height="40" :src="post.author_avatar" fit="cover">
            <template #error>
              <div class="community-detail-page__avatar-placeholder">
                <van-icon name="user-o" size="20" />
              </div>
            </template>
          </van-image>
          <div class="community-detail-page__author-info">
            <span class="community-detail-page__author-name">{{ post.author_name }}</span>
            <span class="community-detail-page__time">{{ formatTime(post.created_at) }}</span>
          </div>
        </div>

        <h2 class="community-detail-page__title">{{ post.title }}</h2>
        <div class="community-detail-page__body markdown-content" v-html="renderedContent"></div>

        <div class="community-detail-page__actions">
          <div class="community-detail-page__action" @click="toggleLike">
            <van-icon
              :name="post.is_liked ? 'like' : 'like-o'"
              :color="post.is_liked ? 'var(--danger-color)' : 'var(--text-secondary)'"
              size="20"
            />
            <span>{{ post.like_count }}</span>
          </div>
          <div class="community-detail-page__action">
            <van-icon name="chat-o" color="var(--text-secondary)" size="20" />
            <span>{{ comments.length }}</span>
          </div>
          <div class="community-detail-page__action" @click="handleShare">
            <van-icon name="share-o" color="var(--text-secondary)" size="20" />
            <span>分享</span>
          </div>
        </div>
      </div>

      <!-- 评论区 -->
      <div class="community-detail-page__comments">
        <h3>评论 ({{ comments.length }})</h3>
        <div v-if="comments.length > 0">
          <div
            v-for="comment in comments"
            :key="comment.id"
            class="community-detail-page__comment"
          >
            <van-image round width="32" height="32" :src="comment.author_avatar" fit="cover">
              <template #error>
                <div class="community-detail-page__comment-avatar">
                  <van-icon name="user-o" size="14" />
                </div>
              </template>
            </van-image>
            <div class="community-detail-page__comment-content">
              <div class="community-detail-page__comment-header">
                <span class="community-detail-page__comment-name">{{ comment.author_name }}</span>
                <span class="community-detail-page__comment-time">{{ formatTime(comment.created_at) }}</span>
              </div>
              <p class="community-detail-page__comment-text">{{ comment.content }}</p>
            </div>
          </div>
        </div>
        <div class="empty-state" v-else>
          <p class="empty-state__text">暂无评论，快来抢沙发</p>
        </div>
      </div>
    </div>

    <!-- 底部评论输入 -->
    <div class="community-detail-page__bottom">
      <div class="community-detail-page__input-wrap">
        <input
          v-model="commentText"
          placeholder="写评论..."
          @keydown.enter="submitComment"
        />
        <van-button
          size="small"
          type="primary"
          round
          :disabled="!commentText.trim()"
          @click="submitComment"
        >
          发送
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast } from 'vant'
import { formatTime, simpleMarkdown } from '@/utils/helpers'

const router = useRouter()
const route = useRoute()

const commentText = ref('')

// 模拟帖子数据
const post = ref({
  id: route.params.id,
  title: '期末复习资料分享',
  content: '整理了高数、线代、概率论的复习笔记和历年真题，有需要的同学可以留言获取。\n\n**高数重点：**\n- 极限与连续\n- 导数与微分\n- 积分与应用\n\n**线代重点：**\n- 矩阵运算\n- 特征值与特征向量\n\n祝大家期末考试顺利！',
  author_name: '学霸小王',
  author_avatar: '',
  topic: '学习',
  like_count: 42,
  is_liked: false,
  created_at: '2024-06-15T10:30:00Z'
})

const comments = ref([
  { id: 1, author_name: '同学A', author_avatar: '', content: '太棒了！请问高数笔记可以分享一下吗？', created_at: '2024-06-15T11:00:00Z' },
  { id: 2, author_name: '同学B', author_avatar: '', content: '感谢分享，已收藏！', created_at: '2024-06-15T12:30:00Z' },
  { id: 3, author_name: '同学C', author_avatar: '', content: '线代的历年真题有答案吗？', created_at: '2024-06-15T14:00:00Z' }
])

const renderedContent = computed(() => {
  return simpleMarkdown(post.value.content)
})

function toggleLike() {
  post.value.is_liked = !post.value.is_liked
  post.value.like_count += post.value.is_liked ? 1 : -1
}

function handleShare() {
  showToast('分享功能开发中')
}

function submitComment() {
  const text = commentText.value.trim()
  if (!text) return
  comments.value.push({
    id: Date.now(),
    author_name: '我',
    author_avatar: '',
    content: text,
    created_at: new Date().toISOString()
  })
  commentText.value = ''
  showToast({ message: '评论成功', type: 'success' })
}
</script>

<style scoped>
.community-detail-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: 60px;
}

.community-detail-page__content {
  padding: var(--spacing-lg);
}

.community-detail-page__post {
  background-color: var(--bg-white);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  box-shadow: var(--shadow-sm);
}

.community-detail-page__author {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.community-detail-page__avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-round);
  background-color: var(--bg-gray);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-placeholder);
}

.community-detail-page__author-name {
  display: block;
  font-size: var(--font-md);
  font-weight: 500;
  color: var(--text-primary);
}

.community-detail-page__time {
  display: block;
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.community-detail-page__title {
  font-size: var(--font-xl);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  line-height: 1.4;
}

.community-detail-page__body {
  font-size: var(--font-md);
  color: var(--text-primary);
  line-height: 1.8;
  margin-bottom: var(--spacing-lg);
}

.community-detail-page__actions {
  display: flex;
  align-items: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-light);
}

.community-detail-page__action {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  cursor: pointer;
}

.community-detail-page__comments {
  background-color: var(--bg-white);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.community-detail-page__comments h3 {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.community-detail-page__comment {
  display: flex;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-light);
}

.community-detail-page__comment:last-child {
  border-bottom: none;
}

.community-detail-page__comment-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-round);
  background-color: var(--bg-gray);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-placeholder);
}

.community-detail-page__comment-content {
  flex: 1;
}

.community-detail-page__comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.community-detail-page__comment-name {
  font-size: var(--font-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.community-detail-page__comment-time {
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.community-detail-page__comment-text {
  font-size: var(--font-md);
  color: var(--text-primary);
  line-height: 1.6;
}

.community-detail-page__bottom {
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

.community-detail-page__input-wrap {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  background-color: var(--bg-gray);
  border-radius: 24px;
  padding: var(--spacing-xs) var(--spacing-xs) var(--spacing-xs) var(--spacing-lg);
}

.community-detail-page__input-wrap input {
  flex: 1;
  height: 36px;
  font-size: var(--font-md);
  color: var(--text-primary);
}

.community-detail-page__input-wrap input::placeholder {
  color: var(--text-placeholder);
}
</style>
