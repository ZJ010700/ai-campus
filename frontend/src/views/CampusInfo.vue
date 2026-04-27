<template>
  <div class="campus-page">
    <van-nav-bar title="校园信息" left-arrow @click-left="router.push('/')" />

    <div class="campus-page__content">
      <!-- 搜索栏 -->
      <div class="campus-page__search">
        <van-search
          v-model="searchKeyword"
          placeholder="搜索校园信息..."
          shape="round"
          @search="handleSearch"
        />
      </div>

      <!-- 功能分类 -->
      <div class="campus-page__categories">
        <div
          v-for="cat in categories"
          :key="cat.name"
          class="campus-page__category"
          @click="handleCategory(cat)"
        >
          <div class="campus-page__category-icon" :style="{ backgroundColor: cat.color }">
            <van-icon :name="cat.icon" size="22" color="white" />
          </div>
          <span class="campus-page__category-name">{{ cat.name }}</span>
        </div>
      </div>

      <!-- 校园公告 -->
      <div class="campus-page__section">
        <div class="campus-page__section-header">
          <h3>校园公告</h3>
          <span class="campus-page__more" @click="loadMore">更多</span>
        </div>
        <div class="campus-page__notice-list">
          <div
            v-for="notice in notices"
            :key="notice.id"
            class="campus-page__notice"
          >
            <div class="campus-page__notice-tag" :class="`campus-page__notice-tag--${notice.type}`">
              {{ notice.tag }}
            </div>
            <div class="campus-page__notice-info">
              <span class="campus-page__notice-title">{{ notice.title }}</span>
              <span class="campus-page__notice-date">{{ notice.date }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 校园地图 -->
      <div class="campus-page__section">
        <h3>校园地图</h3>
        <div class="campus-page__map card">
          <div class="campus-page__map-placeholder">
            <van-icon name="location-o" size="40" color="var(--primary-color)" />
            <p>校园地图功能</p>
            <van-button size="small" round type="primary" @click="openMap">
              打开地图
            </van-button>
          </div>
        </div>
      </div>

      <!-- 校园建筑 -->
      <div class="campus-page__section">
        <h3>主要建筑</h3>
        <div class="campus-page__buildings">
          <div
            v-for="building in buildings"
            :key="building.name"
            class="campus-page__building card"
          >
            <div class="campus-page__building-icon">
              <van-icon :name="building.icon" size="24" color="var(--primary-color)" />
            </div>
            <div class="campus-page__building-info">
              <span class="campus-page__building-name">{{ building.name }}</span>
              <span class="campus-page__building-desc">{{ building.desc }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchKeyword = ref('')

const categories = [
  { name: '新闻', icon: 'newspaper-o', color: '#4A90D9', action: 'news' },
  { name: '通知', icon: 'bell', color: '#ff976a', action: 'notice' },
  { name: '地图', icon: 'location-o', color: '#07c160', action: 'map' },
  { name: '日历', icon: 'calendar-o', color: '#1989fa', action: 'calendar' }
]

const notices = ref([
  { id: 1, title: '关于2024年春季学期期末考试安排的通知', tag: '教务', type: 'academic', date: '2024-06-15' },
  { id: 2, title: '图书馆开放时间调整公告', tag: '后勤', type: 'service', date: '2024-06-14' },
  { id: 3, title: '校园网络升级维护通知', tag: 'IT', type: 'tech', date: '2024-06-13' },
  { id: 4, title: '暑期社会实践报名开始', tag: '活动', type: 'activity', date: '2024-06-12' }
])

const buildings = ref([
  { name: '图书馆', desc: '藏书200万册，自习座位3000+', icon: 'shop-o' },
  { name: '体育馆', desc: '游泳馆、篮球馆、羽毛球馆', icon: 'flag-o' },
  { name: '学生活动中心', desc: '社团活动、文艺演出', icon: 'music-o' },
  { name: '实验楼', desc: '物理、化学、生物实验室', icon: 'records-o' }
])

function handleSearch(keyword) {
  if (!keyword.trim()) return
  router.push({ path: '/chat', query: { module: 'campus', prompt: keyword } })
}

function handleCategory(cat) {
  router.push({ path: '/chat', query: { module: 'campus', action: cat.action } })
}

function loadMore() {
  router.push({ path: '/chat', query: { module: 'campus', prompt: '查看更多校园公告' } })
}

function openMap() {
  router.push({ path: '/chat', query: { module: 'campus', prompt: '打开校园地图' } })
}
</script>

<style scoped>
.campus-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: calc(60px + var(--safe-bottom));
}

.campus-page__content {
  padding: 0 var(--spacing-lg) var(--spacing-lg);
}

.campus-page__search {
  margin-bottom: var(--spacing-lg);
}

.campus-page__categories {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.campus-page__category {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
}

.campus-page__category:active {
  transform: scale(0.95);
}

.campus-page__category-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.campus-page__category-name {
  font-size: var(--font-sm);
  color: var(--text-primary);
}

.campus-page__section {
  margin-bottom: var(--spacing-xl);
}

.campus-page__section h3 {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.campus-page__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.campus-page__section-header h3 {
  margin-bottom: 0;
}

.campus-page__more {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  cursor: pointer;
}

.campus-page__notice {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-light);
}

.campus-page__notice:last-child {
  border-bottom: none;
}

.campus-page__notice-tag {
  flex-shrink: 0;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--font-xs);
  margin-right: var(--spacing-md);
}

.campus-page__notice-tag--academic { background-color: #e8f4fd; color: #1989fa; }
.campus-page__notice-tag--service { background-color: #fff7ed; color: #ff976a; }
.campus-page__notice-tag--tech { background-color: #e8f9f0; color: #07c160; }
.campus-page__notice-tag--activity { background-color: #fde8ef; color: #ee0a24; }

.campus-page__notice-info {
  flex: 1;
  min-width: 0;
}

.campus-page__notice-title {
  display: block;
  font-size: var(--font-md);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 2px;
}

.campus-page__notice-date {
  display: block;
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.campus-page__map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  gap: var(--spacing-sm);
  color: var(--text-secondary);
}

.campus-page__map-placeholder p {
  font-size: var(--font-md);
}

.campus-page__buildings {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.campus-page__building {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.campus-page__building:active {
  transform: scale(0.98);
}

.campus-page__building-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background-color: var(--primary-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
}

.campus-page__building-name {
  display: block;
  font-size: var(--font-md);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.campus-page__building-desc {
  display: block;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}
</style>
