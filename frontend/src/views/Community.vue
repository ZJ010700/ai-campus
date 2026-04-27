<template>
  <div class="community-page">
    <van-nav-bar title="社区">
      <template #right>
        <van-icon name="edit" size="20" @click="router.push('/community/publish')" />
      </template>
    </van-nav-bar>

    <!-- 话题标签 -->
    <div class="community-page__topics">
      <div class="community-page__topics-scroll">
        <div
          v-for="topic in topics"
          :key="topic"
          class="community-page__topic"
          :class="{ 'community-page__topic--active': selectedTopic === topic }"
          @click="selectTopic(topic)"
        >
          {{ topic }}
        </div>
      </div>
    </div>

    <!-- 帖子列表 -->
    <div class="community-page__list">
      <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <van-list
          v-model:loading="loadingMore"
          :finished="finished"
          finished-text="没有更多了"
          @load="loadMorePosts"
        >
          <PostCard
            v-for="post in posts"
            :key="post.id"
            :post="post"
            @click="viewPost(post)"
            @like="toggleLike"
            @share="sharePost"
          />
        </van-list>
      </van-pull-refresh>

      <div class="empty-state" v-if="!loadingMore && posts.length === 0">
        <van-icon name="friends-o" size="48" color="var(--text-placeholder)" />
        <p class="empty-state__text">暂无帖子，快来发布第一篇吧</p>
      </div>
    </div>

    <!-- 浮动发布按钮 -->
    <div class="community-page__fab" @click="router.push('/community/publish')">
      <van-icon name="plus" size="24" color="white" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import PostCard from '@/components/PostCard.vue'

const router = useRouter()

const topics = ['全部', '学习', '生活', '求职', '二手', '活动', '吐槽']
const selectedTopic = ref('全部')
const posts = ref([])
const refreshing = ref(false)
const loadingMore = ref(false)
const finished = ref(false)
const page = ref(1)

// 模拟帖子数据
const mockPosts = [
  {
    id: 1,
    title: '期末复习资料分享',
    content: '整理了高数、线代、概率论的复习笔记和历年真题，有需要的同学可以留言获取。祝大家期末考试顺利！',
    author_name: '学霸小王',
    author_avatar: '',
    topic: '学习',
    like_count: 42,
    comment_count: 15,
    is_liked: false,
    created_at: '2024-06-15T10:30:00Z',
    images: []
  },
  {
    id: 2,
    title: '求推荐附近好吃的餐厅',
    content: '刚来学校不久，想问问大家学校附近有没有什么好吃的餐厅推荐？最好性价比高一点的，谢谢！',
    author_name: '美食爱好者',
    author_avatar: '',
    topic: '生活',
    like_count: 28,
    comment_count: 32,
    is_liked: true,
    created_at: '2024-06-15T09:15:00Z',
    images: []
  },
  {
    id: 3,
    title: '暑期实习经验分享',
    content: '分享一下我在某互联网公司暑期实习的经历和面试经验，希望对正在找实习的同学有所帮助。主要包括简历准备、面试技巧和实习期间的心得。',
    author_name: '实习达人',
    author_avatar: '',
    topic: '求职',
    like_count: 86,
    comment_count: 24,
    is_liked: false,
    created_at: '2024-06-14T16:20:00Z',
    images: []
  }
]

function selectTopic(topic) {
  selectedTopic.value = topic
  posts.value = []
  page.value = 1
  finished.value = false
  loadPosts()
}

function onRefresh() {
  page.value = 1
  finished.value = false
  loadPosts().then(() => {
    refreshing.value = false
  })
}

function loadMorePosts() {
  loadPosts()
}

async function loadPosts() {
  loadingMore.value = true
  try {
    // 模拟加载
    await new Promise(resolve => setTimeout(resolve, 500))
    if (page.value === 1) {
      posts.value = [...mockPosts]
    } else {
      finished.value = true
    }
    page.value++
  } catch (e) {
    console.error(e)
  } finally {
    loadingMore.value = false
  }
}

function viewPost(post) {
  router.push(`/community/${post.id}`)
}

function toggleLike(postId) {
  const post = posts.value.find(p => p.id === postId)
  if (post) {
    post.is_liked = !post.is_liked
    post.like_count += post.is_liked ? 1 : -1
  }
}

function sharePost(postId) {
  showToast('分享功能开发中')
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.community-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: calc(60px + var(--safe-bottom));
}

.community-page__topics {
  background-color: var(--bg-white);
  border-bottom: 1px solid var(--border-color);
}

.community-page__topics-scroll {
  display: flex;
  overflow-x: auto;
  padding: var(--spacing-md) var(--spacing-lg);
  gap: var(--spacing-sm);
  -webkit-overflow-scrolling: touch;
}

.community-page__topics-scroll::-webkit-scrollbar {
  display: none;
}

.community-page__topic {
  flex-shrink: 0;
  padding: 6px 16px;
  border-radius: 16px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  background-color: var(--bg-gray);
  cursor: pointer;
  transition: all 0.2s;
}

.community-page__topic--active {
  background-color: var(--primary-color);
  color: white;
}

.community-page__list {
  padding: var(--spacing-md) var(--spacing-lg);
}

.community-page__fab {
  position: fixed;
  bottom: calc(80px + var(--safe-bottom));
  right: var(--spacing-lg);
  width: 52px;
  height: 52px;
  border-radius: var(--radius-round);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  z-index: 100;
  transition: transform 0.2s;
}

.community-page__fab:active {
  transform: scale(0.9);
}
</style>
