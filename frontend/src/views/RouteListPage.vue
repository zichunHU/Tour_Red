
<script setup>
import { ref, onMounted } from 'vue'

const routes = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await fetch('/api/routes')
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    routes.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <h2>{{ $t('routes.title') }}</h2>
      <p>{{ $t('home.subtitle') }}</p>
    </header>

    <div v-if="loading">{{ $t('common.loading') }}</div>
    <div v-if="error" class="error-message">{{ $t('messages.networkError') }}: {{ error }}</div>

    <section v-if="!loading && !error" class="routes-list">
      <router-link v-for="route in routes" :key="route.id" :to="'/routes/' + route.id" class="card-link">
        <div class="card">
          <h3>{{ route.name }}</h3>
          <p class="description">{{ route.description }}</p>
          <small class="theme-tag">{{ route.theme }}</small>
        </div>
      </router-link>
    </section>
  </div>
</template>

<style scoped>
/* Using styles from the global design system, with minor adjustments */
.card-link {
  text-decoration: none;
  color: inherit;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--primary-text-color);
}

.page-header p {
  font-size: 1.1rem;
  color: var(--secondary-text-color);
}

.routes-list {
  display: grid;
  gap: 1.5rem;
}

.card {
  background-color: var(--card-background-color);
  padding: 2rem;
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  box-sizing: border-box;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.07);
}

.card h3 {
  margin-top: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--accent-color);
}

.card .description {
  color: var(--secondary-text-color);
  line-height: 1.6;
}

.card .theme-tag {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.25rem 0.75rem;
  background-color: #e5e5ea;
  color: #3c3c43;
  border-radius: 8px;
  font-weight: 500;
}

.error-message {
  text-align: center;
  color: var(--accent-color);
}
</style>
