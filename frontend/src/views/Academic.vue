<template>
  <div class="academic-page">
    <van-nav-bar title="学业助手" left-arrow @click-left="router.push('/')" />

    <div class="academic-page__content">
      <!-- 功能入口 -->
      <div class="academic-page__grid">
        <div
          v-for="item in features"
          :key="item.title"
          class="academic-page__feature"
          @click="handleFeature(item)"
        >
          <div class="academic-page__feature-icon" :style="{ backgroundColor: item.color }">
            <van-icon :name="item.icon" size="22" color="white" />
          </div>
          <span class="academic-page__feature-name">{{ item.title }}</span>
        </div>
      </div>

      <!-- 今日课表 -->
      <div class="academic-page__section">
        <div class="academic-page__section-header">
          <h3>今日课表</h3>
          <span class="academic-page__date">{{ todayStr }}</span>
        </div>
        <div class="card" v-if="todayCourses.length > 0">
          <div
            v-for="course in todayCourses"
            :key="course.id"
            class="academic-page__course"
          >
            <div class="academic-page__course-time">
              <span class="academic-page__course-period">{{ course.period }}</span>
              <span class="academic-page__course-hours">{{ course.time }}</span>
            </div>
            <div class="academic-page__course-divider"></div>
            <div class="academic-page__course-info">
              <span class="academic-page__course-name">{{ course.name }}</span>
              <span class="academic-page__course-location">
                <van-icon name="location-o" size="12" />
                {{ course.location }}
              </span>
            </div>
          </div>
        </div>
        <div class="empty-state" v-else>
          <van-icon name="calendar-o" size="40" color="var(--text-placeholder)" />
          <p class="empty-state__text">今天没有课程</p>
        </div>
      </div>

      <!-- 快捷入口 -->
      <div class="academic-page__section">
        <h3>快捷查询</h3>
        <div class="academic-page__quick-cards">
          <ServiceCard
            v-for="svc in quickServices"
            :key="svc.title"
            :title="svc.title"
            :description="svc.description"
            :icon="svc.icon"
            :icon-bg="svc.color"
            :tag="svc.tag"
            @click="goToChat(svc.title)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import ServiceCard from '@/components/ServiceCard.vue'
import { formatDate } from '@/utils/helpers'

const router = useRouter()
const appStore = useAppStore()

const todayStr = formatDate(new Date(), 'YYYY年MM月DD日')

const features = [
  { title: '课表', icon: 'calendar-o', color: '#4A90D9', action: 'schedule' },
  { title: '成绩', icon: 'chart-trending-o', color: '#07c160', action: 'grades' },
  { title: '考试', icon: 'records-o', color: '#ff976a', action: 'exams' },
  { title: '选课', icon: 'apps-o', color: '#1989fa', action: 'courses' },
  { title: '图书馆', icon: 'shop-o', color: '#ee0a24', action: 'library' },
  { title: 'GPA', icon: 'medal-o', color: '#ff6034', action: 'gpa' }
]

const quickServices = [
  {
    title: '智能课表查询',
    description: '问我今天有什么课、本周安排等',
    icon: 'calendar-o',
    color: '#4A90D9',
    tag: 'AI'
  },
  {
    title: '成绩分析',
    description: '查看各科成绩趋势和排名',
    icon: 'chart-trending-o',
    color: '#07c160',
    tag: 'AI'
  },
  {
    title: '考试安排',
    description: '查看 upcoming 考试时间和地点',
    icon: 'records-o',
    color: '#ff976a',
    tag: 'AI'
  }
]

// 模拟今日课表数据
const todayCourses = ref([
  { id: 1, name: '高等数学', period: '第1-2节', time: '08:00-09:40', location: '教学楼A-301' },
  { id: 2, name: '大学英语', period: '第3-4节', time: '10:00-11:40', location: '外语楼B-205' },
  { id: 3, name: '数据结构', period: '第7-8节', time: '14:00-15:40', location: '计算机楼C-102' }
])

function handleFeature(item) {
  router.push({ path: '/chat', query: { module: 'academic', action: item.action } })
}

function goToChat(title) {
  router.push({ path: '/chat', query: { module: 'academic', prompt: title } })
}
</script>

<style scoped>
.academic-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: calc(60px + var(--safe-bottom));
}

.academic-page__content {
  padding: var(--spacing-lg);
}

.academic-page__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.academic-page__feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  background-color: var(--bg-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: transform 0.2s;
}

.academic-page__feature:active {
  transform: scale(0.95);
}

.academic-page__feature-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.academic-page__feature-name {
  font-size: var(--font-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.academic-page__section {
  margin-bottom: var(--spacing-xl);
}

.academic-page__section h3 {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.academic-page__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.academic-page__section-header h3 {
  margin-bottom: 0;
}

.academic-page__date {
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.academic-page__course {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-light);
}

.academic-page__course:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.academic-page__course:first-child {
  padding-top: 0;
}

.academic-page__course-time {
  width: 80px;
  flex-shrink: 0;
  text-align: center;
}

.academic-page__course-period {
  display: block;
  font-size: var(--font-sm);
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 2px;
}

.academic-page__course-hours {
  display: block;
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.academic-page__course-divider {
  width: 2px;
  height: 40px;
  background-color: var(--primary-color);
  border-radius: 1px;
  margin: 0 var(--spacing-md);
}

.academic-page__course-info {
  flex: 1;
}

.academic-page__course-name {
  display: block;
  font-size: var(--font-md);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.academic-page__course-location {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.academic-page__quick-cards {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}
</style>
