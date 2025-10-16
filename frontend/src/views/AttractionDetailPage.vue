<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const attraction = ref(null)
const loading = ref(true)
const error = ref(null)

const backendUrl = 'http://127.0.0.1:5000';

onMounted(async () => {
  const attractionId = route.params.id
  try {
    const response = await fetch(`${backendUrl}/api/attractions/${attractionId}`)
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Attraction not found')
      } else {
        throw new Error('Network response was not ok')
      }
    }
    attraction.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const goBack = () => {
  router.push('/attractions')
}
</script>

<template>
  <div class="page-container">
    <div v-if="loading">正在加载详情...</div>
    <div v-if="error" class="error-message">加载失败: {{ error }}</div>

    <article v-if="attraction" class="detail-card">
      <img v-if="attraction.image_url" :src="backendUrl + attraction.image_url" :alt="attraction.name" class="detail-hero-image">
      
      <header class="detail-header">
        <button @click="goBack" class="back-button">&larr; 返回列表</button>
        <h1>{{ attraction.name }}</h1>
        <p class="name-en">{{ attraction.name_en }}</p>
      </header>

      <section class="detail-content">
        <div class="tags">
          <span class="tag area-tag">{{ attraction.area }}</span>
          <span v-for="theme in attraction.theme" :key="theme" class="tag theme-tag">{{ theme }}</span>
        </div>
        
        <div class="description">
          <h3>中文介绍</h3>
          <p>{{ attraction.description }}</p>
          <h3>English Introduction</h3>
          <p>{{ attraction.description_en }}</p>
        </div>
      </section>
    </article>
  </div>
</template>

<style scoped>
.page-container {
  max-width: 800px;
  margin: 0 auto;
}

.detail-card {
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  overflow: hidden; /* Ensures child elements respect the border radius */
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.detail-hero-image {
  width: 100%;
  height: 350px;
  object-fit: cover;
}

.detail-header {
  padding: 2rem 2rem 1.5rem 2rem;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  position: relative;
}

.back-button {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-family: var(--system-font);
  font-weight: 500;
  color: var(--secondary-text-color);
  transition: background-color 0.2s ease, color 0.2s ease;
}

.back-button:hover {
  background-color: var(--background-color);
  color: var(--primary-text-color);
}

.detail-header h1 {
  font-size: 2.8rem;
  font-weight: 700;
  margin: 0;
  color: var(--primary-text-color);
}

.detail-header .name-en {
  font-size: 1.2rem;
  color: var(--secondary-text-color);
  margin-top: 0.5rem;
}

.detail-content {
  padding: 2rem;
}

.tags {
  margin-bottom: 2rem;
}

.tag {
  display: inline-block;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.3rem 0.8rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
}

.area-tag {
  background-color: #e5e5ea;
  color: #3c3c43;
}

.theme-tag {
  background-color: #ffe5e5;
  color: var(--accent-color);
}

.description h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-text-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.description p {
  line-height: 1.7;
  color: var(--secondary-text-color);
}

.error-message {
  text-align: center;
  color: var(--accent-color);
  padding: 2rem;
}
</style>