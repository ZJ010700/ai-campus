<template>
  <div class="daily-page">
    <van-nav-bar title="日常服务" left-arrow @click-left="router.push('/')" />

    <div class="daily-page__content">
      <!-- 天气信息 -->
      <div class="daily-page__weather card">
        <div class="daily-page__weather-left">
          <van-icon name="sun-o" size="32" color="#ff976a" />
          <div>
            <span class="daily-page__temp">26°C</span>
            <span class="daily-page__weather-desc">晴转多云</span>
          </div>
        </div>
        <div class="daily-page__weather-right">
          <span>湿度 65%</span>
          <span>微风</span>
        </div>
      </div>

      <!-- 服务入口 -->
      <div class="daily-page__section">
        <h3>生活服务</h3>
        <div class="daily-page__grid">
          <div
            v-for="item in services"
            :key="item.name"
            class="daily-page__service"
            @click="handleService(item)"
          >
            <div class="daily-page__service-icon" :style="{ backgroundColor: item.color }">
              <van-icon :name="item.icon" size="22" color="white" />
            </div>
            <span class="daily-page__service-name">{{ item.name }}</span>
          </div>
        </div>
      </div>

      <!-- 食堂推荐 -->
      <div class="daily-page__section">
        <div class="daily-page__section-header">
          <h3>食堂推荐</h3>
          <span class="daily-page__more" @click="goToChat('查看所有食堂菜单')">全部食堂</span>
        </div>
        <div class="daily-page__canteen-list">
          <div
            v-for="canteen in canteens"
            :key="canteen.name"
            class="daily-page__canteen card"
          >
            <div class="daily-page__canteen-header">
              <span class="daily-page__canteen-name">{{ canteen.name }}</span>
              <van-tag type="primary" plain size="medium">{{ canteen.status }}</van-tag>
            </div>
            <div class="daily-page__canteen-dishes">
              <span v-for="dish in canteen.dishes" :key="dish" class="daily-page__dish-tag">
                {{ dish }}
              </span>
            </div>
            <div class="daily-page__canteen-footer">
              <span class="daily-page__canteen-time">
                <van-icon name="clock-o" size="12" />
                {{ canteen.time }}
              </span>
              <span class="daily-page__canteen-price">人均 {{ canteen.price }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 校车时刻 -->
      <div class="daily-page__section">
        <h3>校车时刻表</h3>
        <div class="daily-page__bus card">
          <div
            v-for="bus in busSchedule"
            :key="bus.route"
            class="daily-page__bus-item"
          >
            <div class="daily-page__bus-route">
              <van-icon name="logistics" size="16" color="var(--primary-color)" />
              <span>{{ bus.route }}</span>
            </div>
            <div class="daily-page__bus-times">
              <span v-for="time in bus.times" :key="time" class="daily-page__bus-time">
                {{ time }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷服务卡片 -->
      <div class="daily-page__section">
        <h3>更多服务</h3>
        <div class="daily-page__more-services">
          <ServiceCard
            v-for="svc in moreServices"
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ServiceCard from '@/components/ServiceCard.vue'

const router = useRouter()

const services = [
  { name: '食堂', icon: 'food-a', color: '#ff976a', action: 'canteen' },
  { name: '校车', icon: 'logistics', color: '#4A90D9', action: 'bus' },
  { name: '快递', icon: 'gift-o', color: '#07c160', action: 'express' },
  { name: '报修', icon: 'setting-o', color: '#1989fa', action: 'repair' },
  { name: '失物', icon: 'search', color: '#ee0a24', action: 'lost' },
  { name: '医疗', icon: 'hospital-o', color: '#ff6034', action: 'medical' }
]

const canteens = ref([
  {
    name: '第一食堂',
    status: '营业中',
    dishes: ['红烧排骨', '番茄炒蛋', '清炒时蔬', '紫菜蛋花汤'],
    time: '11:00-13:00',
    price: '12元'
  },
  {
    name: '第二食堂',
    status: '营业中',
    dishes: ['麻辣香锅', '水煮鱼', '蒜蓉西兰花', '酸梅汤'],
    time: '11:00-13:00',
    price: '15元'
  }
])

const busSchedule = ref([
  { route: '校本部 -> 新校区', times: ['07:30', '08:00', '12:00', '17:30', '21:00'] },
  { route: '新校区 -> 校本部', times: ['07:30', '08:00', '12:00', '17:30', '21:00'] }
])

const moreServices = [
  {
    title: '失物招领',
    description: '发布和查找丢失物品',
    icon: 'search',
    color: '#ee0a24',
    tag: '热门'
  },
  {
    title: '在线报修',
    description: '宿舍设施报修申请',
    icon: 'setting-o',
    color: '#1989fa',
    tag: ''
  },
  {
    title: '快递查询',
    description: '查看快递到达情况',
    icon: 'gift-o',
    color: '#07c160',
    tag: ''
  }
]

function handleService(item) {
  router.push({ path: '/chat', query: { module: 'daily', action: item.action } })
}

function goToChat(title) {
  router.push({ path: '/chat', query: { module: 'daily', prompt: title } })
}
</script>

<style scoped>
.daily-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: calc(60px + var(--safe-bottom));
}

.daily-page__content {
  padding: var(--spacing-lg);
}

.daily-page__weather {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #fff7ed, #fff1e6);
  margin-bottom: var(--spacing-xl);
}

.daily-page__weather-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.daily-page__temp {
  display: block;
  font-size: var(--font-xxl);
  font-weight: 700;
  color: var(--text-primary);
}

.daily-page__weather-desc {
  display: block;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.daily-page__weather-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.daily-page__section {
  margin-bottom: var(--spacing-xl);
}

.daily-page__section h3 {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.daily-page__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.daily-page__section-header h3 {
  margin-bottom: 0;
}

.daily-page__more {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  cursor: pointer;
}

.daily-page__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

.daily-page__service {
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

.daily-page__service:active {
  transform: scale(0.95);
}

.daily-page__service-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.daily-page__service-name {
  font-size: var(--font-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.daily-page__canteen-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.daily-page__canteen-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
}

.daily-page__canteen-name {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.daily-page__canteen-dishes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.daily-page__dish-tag {
  padding: 4px 10px;
  background-color: var(--bg-gray);
  border-radius: 12px;
  font-size: var(--font-sm);
  color: var(--text-primary);
}

.daily-page__canteen-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--border-light);
}

.daily-page__canteen-time {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.daily-page__canteen-price {
  font-size: var(--font-sm);
  color: var(--primary-color);
  font-weight: 500;
}

.daily-page__bus-item {
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-light);
}

.daily-page__bus-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.daily-page__bus-item:first-child {
  padding-top: 0;
}

.daily-page__bus-route {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-md);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.daily-page__bus-times {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.daily-page__bus-time {
  padding: 4px 10px;
  background-color: var(--primary-bg);
  border-radius: 12px;
  font-size: var(--font-sm);
  color: var(--primary-color);
}

.daily-page__more-services {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}
</style>
