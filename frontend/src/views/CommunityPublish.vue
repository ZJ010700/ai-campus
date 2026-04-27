<template>
  <div class="publish-page">
    <van-nav-bar
      title="发布帖子"
      left-arrow
      @click-left="router.back()"
      right-text="发布"
      @click-right="handlePublish"
    />

    <div class="publish-page__content">
      <van-cell-group inset>
        <van-field
          v-model="form.title"
          label="标题"
          placeholder="请输入帖子标题"
          maxlength="50"
          show-word-limit
          :rules="[{ required: true, message: '请输入标题' }]"
        />
        <van-field
          v-model="form.content"
          label="内容"
          type="textarea"
          placeholder="分享你的想法..."
          rows="6"
          maxlength="2000"
          show-word-limit
          autosize
          :rules="[{ required: true, message: '请输入内容' }]"
        />
      </van-cell-group>

      <!-- 话题选择 -->
      <div class="publish-page__section">
        <h4>选择话题</h4>
        <div class="publish-page__topics">
          <div
            v-for="topic in topics"
            :key="topic"
            class="publish-page__topic"
            :class="{ 'publish-page__topic--active': form.topic === topic }"
            @click="form.topic = topic"
          >
            {{ topic }}
          </div>
        </div>
      </div>

      <!-- 图片上传 -->
      <div class="publish-page__section">
        <h4>添加图片</h4>
        <van-uploader
          v-model="fileList"
          :max-count="9"
          :max-size="5 * 1024 * 1024"
          @oversize="onOversize"
          multiple
        />
      </div>

      <!-- 发布选项 -->
      <div class="publish-page__section">
        <van-cell title="匿名发布" center>
          <template #right-icon>
            <van-switch v-model="form.anonymous" size="20" />
          </template>
        </van-cell>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()

const form = reactive({
  title: '',
  content: '',
  topic: '',
  anonymous: false
})

const fileList = ref([])

const topics = ['学习', '生活', '求职', '二手', '活动', '吐槽', '求助']

function onOversize() {
  showToast('图片大小不能超过5MB')
}

async function handlePublish() {
  if (!form.title.trim()) {
    showToast('请输入标题')
    return
  }
  if (!form.content.trim()) {
    showToast('请输入内容')
    return
  }

  try {
    // 模拟发布
    await new Promise(resolve => setTimeout(resolve, 500))
    showToast({ message: '发布成功', type: 'success' })
    router.push('/community')
  } catch (e) {
    showToast({ message: '发布失败，请重试', type: 'fail' })
  }
}
</script>

<style scoped>
.publish-page {
  min-height: 100vh;
  background-color: var(--bg-color);
}

.publish-page__content {
  padding: var(--spacing-lg) 0;
}

.publish-page__section {
  padding: var(--spacing-lg);
}

.publish-page__section h4 {
  font-size: var(--font-md);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.publish-page__topics {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.publish-page__topic {
  padding: 6px 16px;
  border-radius: 16px;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  background-color: var(--bg-gray);
  cursor: pointer;
  transition: all 0.2s;
}

.publish-page__topic--active {
  background-color: var(--primary-color);
  color: white;
}
</style>
