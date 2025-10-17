
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import RichTextEditor from '../components/RichTextEditor.vue' // 导入富文本编辑器组件

const route = useRoute()
const router = useRouter()

const attraction = ref({
  name: '',
  name_en: '',
  area: '',
  theme: [],
  description: '',
  description_en: '',
  // image_url: 'image.jpg' // 默认图片名不再需要，图片通过富文本编辑器上传
})

const loading = ref(false)
const error = ref(null)

const apiUrl = '/api';
const isEditMode = computed(() => !!route.params.id)

onMounted(async () => {
  if (isEditMode.value) {
    loading.value = true
    try {
      const response = await fetch(`${apiUrl}/attractions/${route.params.id}`)
      if (!response.ok) throw new Error('Failed to fetch attraction data')
      const data = await response.json()
      // 移除image_url的特殊处理，因为现在图片由富文本编辑器管理
      // if (data.image_url) {
      //   data.image_url = data.image_url.split('/').pop()
      // }
      attraction.value = data
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }
})

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  try {
    const url = isEditMode.value 
      ? `${apiUrl}/attractions/${route.params.id}` 
      : `${apiUrl}/attractions`;

    const method = isEditMode.value ? 'PUT' : 'POST';

    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(attraction.value),
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.error || 'Save operation failed')
    }

    alert('保存成功!')
    router.push('/admin/attractions')

  } catch (e) {
    error.value = e.message
  }
  finally {
    loading.value = false
  }
}

</script>

<template>
  <div>
    <h1>{{ isEditMode ? '编辑景点' : '新建景点' }}</h1>
    <div v-if="loading && isEditMode">正在加载数据...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="handleSubmit" class="admin-form">
      <div class="form-group">
        <label for="name">名称 (中文)</label>
        <input id="name" v-model="attraction.name" type="text" required>
      </div>
      <div class="form-group">
        <label for="name_en">名称 (English)</label>
        <input id="name_en" v-model="attraction.name_en" type="text">
      </div>
      <div class="form-group">
        <label for="area">区域</label>
        <input id="area" v-model="attraction.area" type="text">
      </div>
      <div class="form-group">
        <label for="theme">主题 (逗号分隔)</label>
        <input id="theme" :value="attraction.theme.join(', ')" @input="attraction.theme = $event.target.value.split(',').map(t => t.trim())" type="text">
      </div>
      <div class="form-group">
        <label>介绍 (中文)</label>
        <RichTextEditor v-model="attraction.description" :attraction-id="route.params.id || 0" />
      </div>
      <div class="form-group">
        <label>介绍 (English)</label>
        <RichTextEditor v-model="attraction.description_en" :attraction-id="route.params.id || 0" />
      </div>
      <!-- 主图片文件名输入框不再需要，因为图片通过富文本编辑器上传 -->
      <!-- <div class="form-group">
        <label for="image_url">主图片文件名 (例如: image.jpg)</label>
        <input id="image_url" v-model="attraction.image_url" type="text">
      </div> -->

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? '保存中...' : '保存' }}</button>
        <router-link to="/admin/attractions" class="btn btn-secondary">取消</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>
.admin-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  font-family: var(--system-font);
  font-size: 1rem;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background-color: var(--background-color);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  font-weight: 600;
  font-family: var(--system-font);
  transition: opacity 0.2s ease;
  text-align: center;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: var(--accent-color);
  color: white;
}

.btn-secondary {
  background-color: #e5e5ea;
  color: var(--primary-text-color);
}

.error-message {
  color: var(--accent-color);
  margin-bottom: 1rem;
}
</style>
