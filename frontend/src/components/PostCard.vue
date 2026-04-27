<template>
  <div class="post-card" @click="$emit('click')">
    <div class="post-card__header">
      <div class="post-card__author">
        <van-image
          round
          width="36"
          height="36"
          :src="post.author_avatar"
          fit="cover"
        >
          <template #error>
            <div class="post-card__avatar-placeholder">
              <van-icon name="user-o" size="18" />
            </div>
          </template>
        </van-image>
        <div class="post-card__author-info">
          <span class="post-card__author-name">{{ post.author_name || '匿名用户' }}</span>
          <span class="post-card__time">{{ formattedTime }}</span>
        </div>
      </div>
      <van-tag v-if="post.topic" plain type="primary" size="medium">
        {{ post.topic }}
      </van-tag>
    </div>

    <div class="post-card__body">
      <h4 class="post-card__title">{{ post.title }}</h4>
      <p class="post-card__content">{{ post.content }}</p>
      <div class="post-card__images" v-if="post.images && post.images.length">
        <van-image
          v-for="(img, idx) in post.images.slice(0, 3)"
          :key="idx"
          width="100"
          height="100"
          :src="img"
          fit="cover"
          radius="8"
        />
      </div>
    </div>

    <div class="post-card__footer">
      <div class="post-card__action" @click.stop="$emit('like', post.id)">
        <van-icon
          :name="post.is_liked ? 'like' : 'like-o'"
          :color="post.is_liked ? 'var(--danger-color)' : 'var(--text-secondary)'"
          size="16"
        />
        <span>{{ post.like_count || 0 }}</span>
      </div>
      <div class="post-card__action">
        <van-icon name="chat-o" color="var(--text-secondary)" size="16" />
        <span>{{ post.comment_count || 0 }}</span>
      </div>
      <div class="post-card__action" @click.stop="$emit('share', post.id)">
        <van-icon name="share-o" color="var(--text-secondary)" size="16" />
        <span>分享</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatTime } from '@/utils/helpers'

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})

defineEmits(['click', 'like', 'share'])

const formattedTime = computed(() => {
  return formatTime(props.post.created_at)
})
</script>

<style scoped>
.post-card {
  background-color: var(--bg-white);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  box-shadow: var(--shadow-sm);
}

.post-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.post-card__author {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.post-card__avatar-placeholder {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-round);
  background-color: var(--bg-gray);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-placeholder);
}

.post-card__author-info {
  display: flex;
  flex-direction: column;
}

.post-card__author-name {
  font-size: var(--font-md);
  font-weight: 500;
  color: var(--text-primary);
}

.post-card__time {
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.post-card__body {
  margin-bottom: var(--spacing-md);
}

.post-card__title {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  line-height: 1.4;
}

.post-card__content {
  font-size: var(--font-md);
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
}

.post-card__images {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
}

.post-card__footer {
  display: flex;
  align-items: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-light);
}

.post-card__action {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  cursor: pointer;
  padding: var(--spacing-xs) 0;
}
</style>
