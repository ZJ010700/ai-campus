<template>
  <div class="register-page">
    <van-nav-bar
      title="注册"
      left-arrow
      @click-left="router.push('/login')"
    />

    <div class="register-page__form">
      <van-form @submit="handleRegister" ref="formRef">
        <van-cell-group inset>
          <van-field
            v-model="form.username"
            name="username"
            label="学号"
            placeholder="请输入学号"
            :rules="[
              { required: true, message: '请输入学号' },
              { pattern: /^\d{6,12}$/, message: '学号格式不正确' }
            ]"
          />
          <van-field
            v-model="form.phone"
            name="phone"
            label="手机号"
            placeholder="请输入手机号"
            type="tel"
            :rules="[
              { required: true, message: '请输入手机号' },
              { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确' }
            ]"
          />
          <van-field
            v-model="form.password"
            name="password"
            label="密码"
            type="password"
            placeholder="请输入密码（至少6位）"
            :rules="[
              { required: true, message: '请输入密码' },
              { validator: val => val.length >= 6, message: '密码至少6位' }
            ]"
          />
          <van-field
            v-model="form.confirmPassword"
            name="confirmPassword"
            label="确认密码"
            type="password"
            placeholder="请再次输入密码"
            :rules="[
              { required: true, message: '请确认密码' },
              { validator: val => val === form.password, message: '两次密码不一致' }
            ]"
          />
          <van-field
            v-model="form.name"
            name="name"
            label="姓名"
            placeholder="请输入真实姓名"
            :rules="[{ required: true, message: '请输入姓名' }]"
          />
        </van-cell-group>

        <div class="register-page__agreement">
          <van-checkbox v-model="agreed" shape="square" icon-size="14">
            我已阅读并同意
            <a href="#" @click.prevent>《用户协议》</a>
            和
            <a href="#" @click.prevent>《隐私政策》</a>
          </van-checkbox>
        </div>

        <div class="register-page__actions">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="loading"
            :disabled="!agreed"
            loading-text="注册中..."
            color="var(--primary-color)"
          >
            注册
          </van-button>
        </div>
      </van-form>

      <div class="register-page__links">
        <router-link to="/login">已有账号？返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const agreed = ref(false)

const form = reactive({
  username: '',
  phone: '',
  password: '',
  confirmPassword: '',
  name: ''
})

async function handleRegister() {
  if (!agreed.value) {
    showToast('请先同意用户协议')
    return
  }

  loading.value = true
  try {
    await userStore.register({
      username: form.username,
      phone: form.phone,
      password: form.password,
      name: form.name
    })
    showToast({ message: '注册成功，请登录', type: 'success' })
    router.push('/login')
  } catch (e) {
    showToast({ message: e.message || '注册失败，请重试', type: 'fail' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background-color: var(--bg-color);
}

.register-page__form {
  padding: var(--spacing-lg);
}

.register-page__agreement {
  padding: var(--spacing-md) var(--spacing-lg);
}

.register-page__agreement a {
  color: var(--primary-color);
}

.register-page__actions {
  padding: var(--spacing-lg);
}

.register-page__links {
  text-align: center;
  padding: var(--spacing-md);
}

.register-page__links a {
  font-size: var(--font-sm);
  color: var(--primary-color);
}
</style>
