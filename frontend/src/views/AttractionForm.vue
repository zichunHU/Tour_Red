
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import RichTextEditor from '../components/RichTextEditor.vue' // 导入富文本编辑器组件
import SingleImageUpload from '../components/SingleImageUpload.vue' // 导入单图片上传组件
import { useI18n } from 'vue-i18n'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const attraction = ref({
  name: '',
  name_en: '',
  area: '',
  theme: [],
  address: '',
  description: '',
  description_en: '',
  image_url: '' // 初始化为空字符串，而不是默认图片名
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
      // image_url现在直接从后端获取并绑定，无需特殊处理
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

    alert(t('messages.success'))
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
    <h1>{{ isEditMode ? t('attractions.editAttraction') : t('attractions.createAttraction') }}</h1>
    <div v-if="loading && isEditMode">{{ t('common.loading') }}</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="handleSubmit" class="admin-form">
      <div class="form-group">
        <label for="name">{{ t('attractions.nameZh') }}</label>
        <input id="name" v-model="attraction.name" type="text" required>
      </div>
      <div class="form-group">
        <label for="name_en">{{ t('attractions.nameEn') }}</label>
        <input id="name_en" v-model="attraction.name_en" type="text">
      </div>
      <div class="form-group">
        <label for="area">{{ t('attractions.area') }}</label>
        <input id="area" v-model="attraction.area" type="text">
      </div>
      <div class="form-group">
        <label for="theme">{{ t('attractions.themeInput') }}</label>
        <input id="theme" :value="attraction.theme.join(', ')" @input="attraction.theme = $event.target.value.split(',').map(t => t.trim())" type="text">
      </div>
      <div class="form-group">
        <label for="address">{{ t('attractions.address') }}</label>
        <input id="address" v-model="attraction.address" type="text">
      </div>
      <div class="form-group">
        <label>{{ t('attractions.descriptionZh') }}</label>
        <RichTextEditor v-model="attraction.description" :attraction-id="route.params.id || 0" />
      </div>
      <div class="form-group">
        <label>{{ t('attractions.descriptionEn') }}</label>
        <RichTextEditor v-model="attraction.description_en" :attraction-id="route.params.id || 0" />
      </div>
      <div class="form-group">
        <label>{{ t('attractions.mainImage') }}</label>
        <SingleImageUpload v-model="attraction.image_url" :attraction-id="route.params.id || 0" />
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? t('common.loading') : t('common.save') }}</button>
        <router-link to="/admin/attractions" class="btn btn-secondary">{{ t('common.cancel') }}</router-link>
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
