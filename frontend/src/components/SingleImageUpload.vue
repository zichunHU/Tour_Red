<template>
  <div class="single-image-upload">
    <div v-if="currentImageUrl" class="image-preview">
      <img :src="currentImageUrl" alt="Current Image" />
    </div>
    <div v-else class="image-placeholder">
      <p>无图片</p>
    </div>

    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      accept="image/*"
      style="display: none;"
    />
    <button type="button" @click="triggerFileInput" :disabled="!attractionId || attractionId === 0 || uploading">
      {{ uploading ? '上传中...' : '选择并上传图片' }}
    </button>
    <p v-if="!attractionId || attractionId === 0" class="upload-hint">请先保存景点以启用图片上传。</p>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  attractionId: {
    type: [Number, String],
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const uploading = ref(false)
const error = ref(null)
const currentImageUrl = ref(props.modelValue)

watch(() => props.modelValue, (newValue) => {
  currentImageUrl.value = newValue
})

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  error.value = null

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await fetch(`/api/attractions/${props.attractionId}/images`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`图片上传失败: ${response.status} ${response.statusText} - ${errorText}`)
    }

    const data = await response.json()
    if (data.imageUrl) {
      currentImageUrl.value = data.imageUrl
      emit('update:modelValue', data.imageUrl)
    }
  } catch (e) {
    error.value = e.message
    console.error('Error uploading main image:', e)
  } finally {
    uploading.value = false
    // Reset file input to allow re-uploading the same file if needed
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}
</script>

<style scoped>
.single-image-upload {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border: 1px dashed var(--border-color);
  border-radius: 10px;
  background-color: var(--background-color);
}

.image-preview,
.image-placeholder {
  width: 100%;
  max-width: 300px; /* Limit preview size */
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--card-background-color);
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.image-placeholder p {
  color: var(--secondary-text-color);
}

.single-image-upload button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  background-color: var(--accent-color);
  color: white;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.2s ease;
}

.single-image-upload button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.upload-hint,
.error-message {
  font-size: 0.9rem;
  color: var(--secondary-text-color);
}

.error-message {
  color: var(--accent-color);
}
</style>
