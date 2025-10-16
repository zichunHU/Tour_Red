
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const routeData = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  const routeId = route.params.id
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/routes/${routeId}`)
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Route not found')
      } else {
        throw new Error('Network response was not ok')
      }
    }
    routeData.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const goBack = () => {
  router.push('/routes')
}
</script>

<template>
  <div class="page-container">
    <div v-if="loading">正在加载路线详情...</div>
    <div v-if="error" class="error-message">加载失败: {{ error }}</div>

    <article v-if="routeData" class="detail-card">
      <header class="detail-header">
        <button @click="goBack" class="back-button">&larr; 返回列表</button>
        <h1>{{ routeData.name }}</h1>
        <p class="name-en">{{ routeData.name_en }}</p>
        <span class="tag theme-tag">{{ routeData.theme }}</span>
      </header>

      <section class="detail-content">
        <div class="description">
          <h3>路线介绍</h3>
          <p>{{ routeData.description }}</p>
        </div>

        <div class="attractions-section">
          <h3>包含景点</h3>
          <div class="attractions-container">
            <router-link v-for="attraction in routeData.attractions" :key="attraction.id" :to="'/attractions/' + attraction.id" class="attraction-card-link">
              <div class="attraction-card">
                <h4>{{ attraction.name }}</h4>
                <p>{{ attraction.description.substring(0, 80) }}...</p>
              </div>
            </router-link>
          </div>
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
  overflow: hidden;
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
  margin-bottom: 1rem;
}

.detail-content {
  padding: 2rem;
}

.tag {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
}

.theme-tag {
  background-color: #e5e5ea;
  color: #3c3c43;
}

.description h3, .attractions-section h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-text-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.description p {
  line-height: 1.7;
  color: var(--secondary-text-color);
}

.attractions-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.attraction-card-link {
  text-decoration: none;
  color: inherit;
}

.attraction-card {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.attraction-card:hover {
  background-color: var(--background-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.attraction-card h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--accent-color);
}

.attraction-card p {
  margin: 0;
  color: var(--secondary-text-color);
}

.error-message {
  text-align: center;
  color: var(--accent-color);
  padding: 2rem;
}
</style>
