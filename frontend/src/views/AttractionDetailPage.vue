<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MapViewer from '../components/MapViewer.vue' // 导入地图组件
import { THEME_ICONS } from '../constants/themeIcons.js'

const route = useRoute()
const router = useRouter()

const attraction = ref(null)
const loading = ref(true)
const error = ref(null)

const apiUrl = '/api';

onMounted(async () => {
  const attractionId = route.params.id
  try {
    const response = await fetch(`${apiUrl}/attractions/${attractionId}`)
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
    <div v-if="loading">{{ $t('common.loading') }}</div>
    <div v-if="error" class="error-message">{{ $t('messages.networkError') }}: {{ error }}</div>

    <article v-if="attraction" class="detail-card">
      <img v-if="attraction.image_url" :src="attraction.image_url" :alt="attraction.name" class="detail-hero-image">
      
      <header class="detail-header">
        <button @click="goBack" class="back-button">&larr; {{ $t('common.back') }}</button>
        <h1>{{ attraction.name }}</h1>
        <p class="name-en">{{ attraction.name_en }}</p>
      </header>

      <section class="detail-content">
        <div class="tags">
          <span class="tag area-tag">{{ $t(`areas.${attraction.area}`) }}</span>
          <span v-for="theme in attraction.theme" :key="theme" class="tag theme-tag">{{ THEME_ICONS[theme] }} {{ $t(`themes.${theme}`) }}</span>
        </div>

        <div v-if="attraction.address" class="address-section">
          <p><strong>{{ $t('attractions.address') }}:</strong> {{ attraction.address }}</p>
        </div>
        
        <div class="content-grid">
          <div class="description-container">
            <div class="description">
              <h3>{{ $t('attractions.description') }}</h3>
              <div v-html="attraction.description" class="markdown-content"></div>

              <h3>{{ $t('attractions.description') }}</h3>
              <div v-html="attraction.description_en" class="markdown-content"></div>
            </div>
          </div>

          <aside class="map-container">
            <h3>{{ $t('map.loading') }}</h3>
            <MapViewer 
              v-if="attraction.location && attraction.location.latitude && attraction.location.longitude"
              :latitude="attraction.location.latitude" 
              :longitude="attraction.location.longitude"
            />
            <div v-else class="no-location">
              {{ $t('map.noLocation') }}
            </div>
          </aside>
        </div>
      </section>
    </article>
  </div>
</template>

<style scoped>
.page-container {
  max-width: 1200px; /* Widen the container for two columns */
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
  height: 400px; /* Increased height for a more impressive hero image */
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

.address-section {
  padding: 1rem 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.address-section p {
  font-size: 1.1rem;
  color: var(--secondary-text-color);
  margin: 0;
}

.address-section strong {
  color: var(--primary-text-color);
}

/* New Grid Layout */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr; /* 2/3 for description, 1/3 for map */
  gap: 2rem;
  align-items: start;
}

@media (max-width: 992px) {
  .content-grid {
    grid-template-columns: 1fr; /* Stack on smaller screens */
  }
}

.description h3, .map-container h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-text-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.map-container .no-location {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  background-color: var(--background-color);
  color: var(--secondary-text-color);
  border-radius: var(--card-border-radius);
}

.markdown-content ::v-deep(p) {
  line-height: 1.7;
  color: var(--secondary-text-color);
  margin: 1em 0;
}

.markdown-content ::v-deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 12px; /* A slightly smaller radius than the card */
  margin: 1.5rem 0;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.error-message {
  text-align: center;
  color: var(--accent-color);
  padding: 2rem;
}
</style>