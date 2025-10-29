
<script setup>
import { ref, onMounted } from 'vue'

// Reactive state for attractions and loading/error
const attractions = ref([])
const loading = ref(true)
const error = ref(null)

// Reactive state for filter inputs
const searchKeyword = ref('')
const selectedArea = ref('')
const selectedTheme = ref('')

// Hardcoded options for filters (in a real app, this might come from an API)
const areaOptions = ['黄浦区', '徐汇区']
const themeOptions = ['革命足迹', '建党伟业', '革命烈士', '抗日战争', '伟人故居', '文化名人']

// Backend API URL
const apiUrl = '/api';

// Reusable function to fetch attractions based on current filters
const fetchAttractions = async () => {
  loading.value = true
  error.value = null
  try {
    // Build the query string
    const params = new URLSearchParams()
    if (searchKeyword.value) params.append('keyword', searchKeyword.value)
    if (selectedArea.value) params.append('area', selectedArea.value)
    if (selectedTheme.value) params.append('theme', selectedTheme.value)
    
    const response = await fetch(`${apiUrl}/attractions?${params.toString()}`)
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    attractions.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

// Fetch initial data when component is mounted
onMounted(() => {
  fetchAttractions()
})

// Handler for the search button
const handleSearch = () => {
  fetchAttractions()
}

// Handler to reset filters
const handleReset = () => {
  searchKeyword.value = ''
  selectedArea.value = ''
  selectedTheme.value = ''
  fetchAttractions()
}

</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <h2>{{ $t('attractions.title') }}</h2>
      <p>{{ $t('attractions.subtitle') }}</p>
    </header>

    <section class="filters">
      <div class="filter-group">
        <input type="text" v-model="searchKeyword" :placeholder="$t('common.searchPlaceholder')" class="search-input" @keyup.enter="handleSearch" />
      </div>
      <div class="filter-group">
        <select v-model="selectedArea">
          <option value="">{{ $t('attractions.allAreas') }}</option>
          <option v-for="area in areaOptions" :key="area" :value="area">{{ $t(`areas.${area}`) }}</option>
        </select>
        <select v-model="selectedTheme">
          <option value="">{{ $t('attractions.allThemes') }}</option>
          <option v-for="theme in themeOptions" :key="theme" :value="theme">{{ $t(`themes.${theme}`) }}</option>
        </select>
      </div>
      <div class="filter-group">
        <button @click="handleSearch" class="button-primary">{{ $t('common.search') }}</button>
        <button @click="handleReset" class="button-secondary">{{ $t('common.clear') }}</button>
      </div>
    </section>

    <div v-if="loading">{{ $t('common.loading') }}</div>
    <div v-if="error" class="error-message">{{ $t('messages.networkError') }}: {{ error }}</div>

    <section v-if="!loading && !error" class="attractions-list">
      <p v-if="attractions.length === 0" class="no-results">{{ $t('attractions.noResults') }}</p>
      <router-link v-else v-for="attraction in attractions" :key="attraction.id" :to="'/attractions/' + attraction.id" class="card-link">
        <div class="card">
          <img v-if="attraction.image_url" :src="attraction.image_url" :alt="attraction.name" class="card-image">
          <div class="card-content">
            <h3>{{ attraction.name }}</h3>
            <p class="description">{{ attraction.description }}</p>
            <small class="area-tag">{{ $t(`areas.${attraction.area}`) }}</small>
          </div>
        </div>
      </router-link>
    </section>
  </div>
</template>

<style scoped>
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

/* Filters Section */
.filters {
  background-color: var(--card-background-color);
  padding: 1.5rem 2rem;
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  margin-bottom: 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}

.filter-group {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input, select {
  font-family: var(--system-font);
  font-size: 1rem;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background-color: var(--background-color);
}

.search-input {
  min-width: 250px;
}

.button-primary, .button-secondary {
  font-family: var(--system-font);
  font-size: 1rem;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-primary {
  background-color: var(--accent-color);
  color: white;
}

.button-primary:hover {
  opacity: 0.85;
}

.button-secondary {
  background-color: var(--background-color);
  color: var(--primary-text-color);
  border: 1px solid var(--border-color);
}

.button-secondary:hover {
  background-color: #e5e5ea; /* A bit darker than background */
}

/* Attractions List */
.attractions-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.no-results {
  text-align: center;
  color: var(--secondary-text-color);
  padding: 3rem;
}

.card {
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  box-sizing: border-box;
  overflow: hidden; /* Ensures image corners are clipped */
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.07);
}

.card-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.card-content {
  padding: 1.5rem;
}

.card h3 {
  margin-top: 0;
  font-size: 1.25rem; /* Slightly smaller to fit better */
  font-weight: 600;
  color: var(--accent-color);
}

.card .description {
  color: var(--secondary-text-color);
  line-height: 1.6;
  font-size: 0.9rem;
  /* Truncate the text for card view */
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* number of lines to show */
  -webkit-box-orient: vertical;
}

.card .area-tag {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.25rem 0.75rem;
  background-color: var(--background-color);
  color: var(--secondary-text-color);
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.8rem;
}

.error-message {
  text-align: center;
  color: var(--accent-color);
}
</style>
