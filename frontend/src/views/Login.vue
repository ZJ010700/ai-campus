<template>
  <div class="login-page">
    <div class="login-page__header">
      <div class="login-page__logo">
        <div class="login-page__logo-icon">AI</div>
      </div>
      <h1 class="login-page__title">AI+Campus</h1>
      <p class="login-page__subtitle">校园智能服务助手</p>
    </div>

    <div class="login-page__form">
      <van-form @submit="handleLogin" ref="formRef">
        <van-cell-group inset>
          <van-field
            v-model="form.username"
            name="username"
            label="账号"
            placeholder="请输入学号/手机号"
            :rules="[{ required: true, message: '请输入账号' }]"
            left-icon="user-o"
          />
          <van-field
            v-model="form.password"
            name="password"
            label="密码"
            type="password"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请输入密码' }]"
            left-icon="lock"
          />
        </van-cell-group>

        <div class="login-page__actions">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="loading"
            loading-text="登录中..."
            color="var(--primary-color)"
          >
            登录
          </van-button>
        </div>
      </van-form>

      <div class="login-page__links">
        <router-link to="/register">还没有账号？立即注册</router-link>
      </div>
    </div>

    <div class="login-page__footer">
      <p>登录即表示同意 <a href="#">用户协议</a> 和 <a href="#">隐私政策</a></p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast } from 'vant'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

async function handleLogin() {
  loading.value = true
  try {
    await userStore.login(form)
    await userStore.fetchUserInfo()
    userStore.saveToStorage()
    showToast({ message: '登录成功', type: 'success' })
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    showToast({ message: e.message || '登录失败，请重试', type: 'fail' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(180deg, var(--primary-color) 0%, var(--primary-light) 40%, var(--bg-color) 40%);
  display: flex;
  flex-direction: column;
  padding: 0 var(--spacing-xl);
}

.login-page__header {
  text-align: center;
  padding: 60px 0 40px;
}

.login-page__logo {
  margin-bottom: var(--spacing-lg);
}

.login-page__logo-icon {
  width: 72px;
  height: 72px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 28px;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  letter-spacing: -1px;
}

.login-page__title {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin-bottom: var(--spacing-sm);
}

.login-page__subtitle {
  font-size: var(--font-md);
  color: rgba(255, 255, 255, 0.8);
}

.login-page__form {
  background-color: var(--bg-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-lg);
}

.login-page__actions {
  margin-top: var(--spacing-xl);
}

.login-page__links {
  text-align: center;
  margin-top: var(--spacing-lg);
}

.login-page__links a {
  font-size: var(--font-sm);
  color: var(--primary-color);
}

.login-page__footer {
  margin-top: auto;
  padding: var(--spacing-xl) 0;
  text-align: center;
}

.login-page__footer p {
  font-size: var(--font-xs);
  color: var(--text-placeholder);
}

.login-page__footer a {
  color: var(--primary-color);
}
</style>
