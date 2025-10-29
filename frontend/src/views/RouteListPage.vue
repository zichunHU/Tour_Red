
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { THEME_ICONS } from '../constants/themeIcons.js'
import { resolveThemeTag, resolveDurationTag, isDurationCode } from '../utils/themeTag.js'

const routes = ref([])
const loading = ref(true)
const error = ref(null)

const { locale, t } = useI18n()
const isEn = computed(() => locale.value === 'en-US')

const stripHtml = (s) => (s || '').replace(/<[^>]*>/g, '')
const truncate = (s, n) => {
  if (!s) return ''
  return s.length > n ? s.slice(0, n) + '…' : s
}
const getPrimaryTitle = (r) => (isEn.value ? (r.name_en || r.name) : (r.name || r.name_en || ''))
const getSecondaryTitle = (r) => (isEn.value ? (r.name || '') : (r.name_en || ''))
const getSummary = (r) => {
  const raw = isEn.value
    ? (r.summary_en || r.summary || r.description_en || r.description)
    : (r.summary || r.summary_en || r.description || r.description_en)
  return truncate(stripHtml(raw), 100)
}

const getThemeOnlyTag = (code) => {
  if (!code || isDurationCode(code)) return { icon: '', label: '' }
  return resolveThemeTag(code, t, THEME_ICONS)
}

const getDurationTag = (route) => {
  const durCode = route.duration || (isDurationCode(route.theme) ? route.theme : '')
  return resolveDurationTag(durCode, t)
}

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
      <h2>{{ t('routes.title') }}</h2>
      <p>{{ t('home.subtitle') }}</p>
    </header>

    <div v-if="loading">{{ $t('common.loading') }}</div>
    <div v-if="error" class="error-message">{{ $t('messages.networkError') }}: {{ error }}</div>

    <section v-if="!loading && !error" class="routes-list">
      <router-link v-for="route in routes" :key="route.id" :to="'/routes/' + route.id" class="card-link">
        <div class="card">
          <h3 :class="{ 'title-accent': isEn }">{{ getPrimaryTitle(route) }}</h3>
          <p v-if="getSecondaryTitle(route)" class="name-secondary">{{ getSecondaryTitle(route) }}</p>
          <p class="description">{{ getSummary(route) }}</p>
          <div class="tag-row">
            <small v-if="getThemeOnlyTag(route.theme).label" class="theme-tag">
              <template v-if="getThemeOnlyTag(route.theme).icon">{{ getThemeOnlyTag(route.theme).icon }} </template>{{ getThemeOnlyTag(route.theme).label }}
            </small>
            <small v-if="getDurationTag(route).label" class="duration-tag">
              <template v-if="getDurationTag(route).icon">{{ getDurationTag(route).icon }} </template>{{ getDurationTag(route).label }}
            </small>
          </div>
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

.tag-row { display: flex; gap: 0.5rem; align-items: center; margin-top: 0.75rem; }
.duration-tag {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  background-color: #eef6ff;
  color: #1e3a8a;
  border-radius: 8px;
  font-weight: 500;
}

.error-message {
  text-align: center;
  color: var(--accent-color);
}
</style>
