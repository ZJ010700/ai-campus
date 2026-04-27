<template>
  <div class="settings-page">
    <van-nav-bar
      title="设置"
      left-arrow
      @click-left="router.back()"
    />

    <div class="settings-page__content">
      <!-- 账号信息 -->
      <van-cell-group inset title="账号信息">
        <van-cell title="头像" center>
          <template #value>
            <van-image round width="40" height="40" :src="userStore.avatar" fit="cover">
              <template #error>
                <div class="settings-page__avatar-small">
                  <van-icon name="user-o" size="18" />
                </div>
              </template>
            </van-image>
          </template>
        </van-cell>
        <van-cell title="昵称" :value="userStore.username || '--'" is-link />
        <van-cell title="学号" :value="userStore.userInfo?.student_id || '--'" />
        <van-cell title="手机号" :value="maskedPhone" is-link />
      </van-cell-group>

      <!-- 通用设置 -->
      <van-cell-group inset title="通用设置" style="margin-top: 12px;">
        <van-cell title="消息通知" center>
          <template #right-icon>
            <van-switch v-model="settings.notification" size="20" />
          </template>
        </van-cell>
        <van-cell title="声音提醒" center>
          <template #right-icon>
            <van-switch v-model="settings.sound" size="20" />
          </template>
        </van-cell>
        <van-cell title="深色模式" center>
          <template #right-icon>
            <van-switch v-model="settings.darkMode" size="20" @change="toggleDarkMode" />
          </template>
        </van-cell>
        <van-cell title="字体大小" is-link :value="fontSizeLabel" @click="showFontPicker = true" />
      </van-cell-group>

      <!-- 隐私设置 -->
      <van-cell-group inset title="隐私设置" style="margin-top: 12px;">
        <van-cell title="在线状态" center>
          <template #right-icon>
            <van-switch v-model="settings.onlineStatus" size="20" />
          </template>
        </van-cell>
        <van-cell title="允许陌生人消息" center>
          <template #right-icon>
            <van-switch v-model="settings.strangerMsg" size="20" />
          </template>
        </van-cell>
      </van-cell-group>

      <!-- 数据管理 -->
      <van-cell-group inset title="数据管理" style="margin-top: 12px;">
        <van-cell title="清除缓存" is-link :value="cacheSize" @click="clearCache" />
        <van-cell title="导出对话记录" is-link @click="exportChats" />
      </van-cell-group>

      <!-- 关于 -->
      <van-cell-group inset title="关于" style="margin-top: 12px;">
        <van-cell title="版本" value="v1.0.0" />
        <van-cell title="用户协议" is-link @click="showToast('用户协议页面开发中')" />
        <van-cell title="隐私政策" is-link @click="showToast('隐私政策页面开发中')" />
        <van-cell title="检查更新" is-link @click="checkUpdate" />
      </van-cell-group>

      <!-- 退出登录 -->
      <div class="settings-page__logout" style="margin-top: 24px;">
        <van-button round block plain type="danger" @click="handleLogout">
          退出登录
        </van-button>
      </div>

      <!-- 字体大小选择 -->
      <van-action-sheet
        v-model:show="showFontPicker"
        :actions="fontActions"
        @select="onFontSelect"
        cancel-text="取消"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showToast } from 'vant'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const showFontPicker = ref(false)

const settings = reactive({
  notification: true,
  sound: true,
  darkMode: false,
  onlineStatus: true,
  strangerMsg: false,
  fontSize: 'medium'
})

const cacheSize = ref('2.3MB')

const fontActions = [
  { name: '小', value: 'small' },
  { name: '标准', value: 'medium' },
  { name: '大', value: 'large' },
  { name: '特大', value: 'xlarge' }
]

const fontSizeLabel = computed(() => {
  const map = { small: '小', medium: '标准', large: '大', xlarge: '特大' }
  return map[settings.fontSize] || '标准'
})

const maskedPhone = computed(() => {
  const phone = userStore.userInfo?.phone
  if (!phone) return '未绑定'
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
})

function onFontSelect(action) {
  settings.fontSize = action.value
  document.documentElement.style.fontSize = {
    small: '14px',
    medium: '16px',
    large: '18px',
    xlarge: '20px'
  }[action.value]
  showToast(`字体已切换为${action.name}`)
}

function toggleDarkMode(val) {
  if (val) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

function clearCache() {
  showDialog({
    title: '清除缓存',
    message: '确定要清除所有缓存数据吗？',
    showCancelButton: true
  }).then(() => {
    cacheSize.value = '0MB'
    showToast({ message: '缓存已清除', type: 'success' })
  }).catch(() => {})
}

function exportChats() {
  showToast('对话记录导出功能开发中')
}

function checkUpdate() {
  showToast({ message: '当前已是最新版本', type: 'success' })
}

async function handleLogout() {
  try {
    await showDialog({
      title: '提示',
      message: '确定要退出登录吗？',
      showCancelButton: true
    })
    userStore.logout()
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background-color: var(--bg-color);
}

.settings-page__content {
  padding: var(--spacing-lg) 0 var(--spacing-xl);
}

.settings-page__avatar-small {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-round);
  background-color: var(--bg-gray);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-placeholder);
}

.settings-page__logout {
  padding: 0 var(--spacing-xl);
}
</style>
