<template>
  <div class="mental-page">
    <van-nav-bar title="心理伙伴" left-arrow @click-left="router.push('/')" />

    <div class="mental-page__content">
      <!-- 心情卡片 -->
      <div class="mental-page__mood card">
        <h3>今天心情怎么样？</h3>
        <div class="mental-page__mood-list">
          <div
            v-for="mood in moods"
            :key="mood.label"
            class="mental-page__mood-item"
            :class="{ 'mental-page__mood-item--active': selectedMood === mood.label }"
            @click="selectMood(mood.label)"
          >
            <span class="mental-page__mood-emoji">{{ mood.emoji }}</span>
            <span class="mental-page__mood-label">{{ mood.label }}</span>
          </div>
        </div>
      </div>

      <!-- 功能入口 -->
      <div class="mental-page__features">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="mental-page__feature card"
          @click="handleFeature(feature)"
        >
          <div class="mental-page__feature-icon" :style="{ backgroundColor: feature.color }">
            <van-icon :name="feature.icon" size="22" color="white" />
          </div>
          <div class="mental-page__feature-info">
            <span class="mental-page__feature-title">{{ feature.title }}</span>
            <span class="mental-page__feature-desc">{{ feature.desc }}</span>
          </div>
          <van-icon name="arrow" color="var(--text-placeholder)" size="16" />
        </div>
      </div>

      <!-- 每日一言 -->
      <div class="mental-page__quote card">
        <div class="mental-page__quote-icon">
          <van-icon name="chat-o" size="20" color="var(--primary-color)" />
        </div>
        <p class="mental-page__quote-text">{{ dailyQuote }}</p>
        <span class="mental-page__quote-author">-- {{ dailyQuoteAuthor }}</span>
      </div>

      <!-- 心理知识 -->
      <div class="mental-page__tips">
        <h3>心理小贴士</h3>
        <div class="mental-page__tip-list">
          <div
            v-for="tip in tips"
            :key="tip.title"
            class="mental-page__tip card"
          >
            <h4>{{ tip.title }}</h4>
            <p>{{ tip.content }}</p>
          </div>
        </div>
      </div>

      <!-- 紧急求助 -->
      <div class="mental-page__emergency card">
        <div class="mental-page__emergency-icon">
          <van-icon name="phone-o" size="24" color="var(--danger-color)" />
        </div>
        <div class="mental-page__emergency-info">
          <h4>需要帮助？</h4>
          <p>如果你感到情绪困扰，可以随时联系心理咨询中心</p>
          <span class="mental-page__emergency-phone">心理热线：400-xxx-xxxx</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()
const selectedMood = ref('')

const moods = [
  { emoji: '\u{1F60A}', label: '开心' },
  { emoji: '\u{1F610}', label: '平静' },
  { emoji: '\u{1F614}', label: '低落' },
  { emoji: '\u{1F629}', label: '焦虑' },
  { emoji: '\u{1F61E}', label: '难过' },
  { emoji: '\u{1F624}', label: '生气' }
]

const features = [
  {
    title: 'AI 倾听',
    desc: '和 AI 聊聊你的心事',
    icon: 'chat-o',
    color: '#4A90D9',
    action: 'chat'
  },
  {
    title: '情绪记录',
    desc: '记录每天的情绪变化',
    icon: 'records-o',
    color: '#07c160',
    action: 'record'
  },
  {
    title: '放松练习',
    desc: '呼吸练习和冥想引导',
    icon: 'music-o',
    color: '#ff976a',
    action: 'relax'
  },
  {
    title: '心理测评',
    desc: '专业的心理健康评估',
    icon: 'chart-trending-o',
    color: '#1989fa',
    action: 'test'
  }
]

const dailyQuote = ref('每一个不曾起舞的日子，都是对生命的辜负。')
const dailyQuoteAuthor = ref('尼采')

const tips = ref([
  {
    title: '如何缓解考试焦虑？',
    content: '深呼吸、合理规划时间、保持充足睡眠，适当运动也能有效缓解焦虑情绪。'
  },
  {
    title: '改善睡眠的小技巧',
    content: '保持规律的作息时间，睡前避免使用电子设备，可以尝试冥想或阅读来帮助入睡。'
  }
])

function selectMood(label) {
  selectedMood.value = label
  showToast(`已记录今天的心情：${label}`)
}

function handleFeature(feature) {
  if (feature.action === 'chat') {
    router.push({ path: '/chat', query: { module: 'mental' } })
  } else {
    showToast(`${feature.title}功能开发中`)
  }
}
</script>

<style scoped>
.mental-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: calc(60px + var(--safe-bottom));
}

.mental-page__content {
  padding: var(--spacing-lg);
}

.mental-page__mood {
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.mental-page__mood h3 {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.mental-page__mood-list {
  display: flex;
  justify-content: space-around;
}

.mental-page__mood-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.mental-page__mood-item:active {
  transform: scale(0.95);
}

.mental-page__mood-item--active {
  background-color: var(--primary-bg);
}

.mental-page__mood-emoji {
  font-size: 28px;
}

.mental-page__mood-label {
  font-size: var(--font-xs);
  color: var(--text-secondary);
}

.mental-page__features {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.mental-page__feature {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.mental-page__feature:active {
  transform: scale(0.98);
}

.mental-page__feature-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
}

.mental-page__feature-info {
  flex: 1;
}

.mental-page__feature-title {
  display: block;
  font-size: var(--font-md);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.mental-page__feature-desc {
  display: block;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.mental-page__quote {
  text-align: center;
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
  background: linear-gradient(135deg, #f0f7ff, #e8f4fd);
}

.mental-page__quote-icon {
  margin-bottom: var(--spacing-md);
}

.mental-page__quote-text {
  font-size: var(--font-lg);
  color: var(--text-primary);
  line-height: 1.6;
  font-style: italic;
  margin-bottom: var(--spacing-sm);
}

.mental-page__quote-author {
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.mental-page__tips {
  margin-bottom: var(--spacing-xl);
}

.mental-page__tips h3 {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.mental-page__tip-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.mental-page__tip h4 {
  font-size: var(--font-md);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.mental-page__tip p {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  line-height: 1.6;
}

.mental-page__emergency {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #fff5f5, #ffe8e8);
}

.mental-page__emergency-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-round);
  background-color: rgba(238, 10, 36, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
}

.mental-page__emergency-info h4 {
  font-size: var(--font-md);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.mental-page__emergency-info p {
  font-size: var(--font-sm);
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.mental-page__emergency-phone {
  font-size: var(--font-md);
  font-weight: 600;
  color: var(--danger-color);
}
</style>
