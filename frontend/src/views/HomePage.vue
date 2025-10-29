<script setup>
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router';

// Import Swiper Vue.js components
import { Swiper, SwiperSlide } from 'swiper/vue';

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import 'swiper/css/autoplay';

// import required modules
import { Autoplay, Pagination, Navigation } from 'swiper/modules';
import { THEME_KEYS } from '../constants/catalog.js'
import { THEME_ICONS } from '../constants/themeIcons.js'

const router = useRouter();
const { t, locale } = useI18n()

// --- STATE & DATA FETCHING ---
const attractions = ref([]);
const routes = ref([]);
const loading = ref(true);
const error = ref(null);
const heroCurrentSlideIndex = ref(0);

// THEME_ICONS imported from constants to keep mapping reusable

// Drive theme cards from THEME_KEYS to avoid duplication
const interestTags = computed(() => THEME_KEYS.map(code => ({ code, icon: THEME_ICONS[code] || '🏷️' })))

// Collapse/expand theme section
const showAllThemes = ref(false)
const displayedThemes = computed(() => showAllThemes.value ? interestTags.value : interestTags.value.slice(0, 6))
function toggleThemes() { showAllThemes.value = !showAllThemes.value }

const swiperModules = [Autoplay, Pagination, Navigation];

// Locale-aware bilingual titles for attraction cards
const isEn = computed(() => locale.value === 'en-US')
const getPrimaryTitle = (a) => (isEn.value ? (a.name_en || a.name) : a.name)
const getSecondaryTitle = (a) => (isEn.value ? (a.name || '') : '')

onMounted(async () => {
  try {
    const [attractionsRes, routesRes] = await Promise.all([
      fetch('/api/attractions'),
      fetch('/api/routes'),
    ]);
    if (!attractionsRes.ok || !routesRes.ok) {
      throw new Error('Failed to fetch initial data');
    }
    attractions.value = await attractionsRes.json();
    routes.value = await routesRes.json();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
});

// --- HELPERS ---
const stripHtml = (html) => {
  if (!html) return '';
  let doc = new DOMParser().parseFromString(html, 'text/html');
  return doc.body.textContent || "";
}

const truncate = (text, length) => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '…' : text;
}

// --- ROUTE CARD LOCALIZATION HELPERS ---
// Bilingual title and summary with graceful fallback
const getRoutePrimaryTitle = (r) => (isEn.value ? (r.name_en || r.name) : (r.name || r.name_en || ''))
const getRouteSecondaryTitle = (r) => (isEn.value ? (r.name || '') : (r.name_en || ''))
const getRouteSummary = (r) => {
  const raw = isEn.value
    ? (r.summary_en || r.summary || r.description_en || r.description)
    : (r.summary || r.summary_en || r.description || r.description_en)
  const clean = stripHtml(raw)
  return truncate(clean, 100)
}

// --- COMPUTED PROPERTIES ---

const heroSlides = computed(() => attractions.value.filter(a => a.image_url).slice(0, 5));
const featuredAttractions = computed(() => attractions.value.slice(0, 8));
const featuredRoutes = computed(() => routes.value.slice(0, 4));

const dynamicSubtitle = computed(() => {
  if (!heroSlides.value.length) return t('home.subtitle');
  const a = heroSlides.value[heroCurrentSlideIndex.value];
  if (!a) return t('home.subtitle');
  const raw = locale.value === 'en-US'
    ? (a.summary_en || a.summary || a.description_en || a.description)
    : (a.summary || a.summary_en || a.description || a.description_en);
  const clean = stripHtml(raw);
  return clean ? truncate(clean, 80) : t('home.subtitle');
});

// --- METHODS ---

function onHeroSlideChange(swiper) {
  heroCurrentSlideIndex.value = swiper.realIndex;
}

function navigateToPersonalization() {
  router.push('/customize');
}

function exploreTheme(themeCode) {
  router.push({ path: '/attractions', query: { theme: themeCode } });
}

</script>

<template>
  <div class="home-page">
    <!-- 1. Hero Section with Swiper -->
    <section class="hero-section">
      <Swiper
        class="hero-swiper"
        :modules="swiperModules"
        :slides-per-view="1"
        :loop="true"
        :autoplay="{ delay: 5000, disableOnInteraction: false }"
        :pagination="{ clickable: true }"
        @slideChange="onHeroSlideChange"
      >
        <SwiperSlide v-for="slide in heroSlides" :key="slide.id">
          <div class="hero-slide-background" :style="{ backgroundImage: `url(${slide.image_url})` }"></div>
        </SwiperSlide>
      </Swiper>
      
      <div class="hero-content-overlay">
        <h1 class="hero-title">{{ $t('home.subtitle') }}</h1>
        <p class="hero-subtitle">{{ dynamicSubtitle }}</p>
        <button @click="navigateToPersonalization" class="hero-cta-button">{{ $t('home.startJourney') }}</button>
      </div>
    </section>

    <div class="page-content">
      <!-- 2. Thematic Exploration Section -->
      <section class="content-section">
        <h2 class="section-title">{{ $t('home.exploreByTheme') }}</h2>
        <div class="theme-grid">
          <div v-for="theme in displayedThemes" :key="theme.code" class="theme-card" @click="exploreTheme(theme.code)">
            <div class="theme-icon">{{ theme.icon }}</div>
            <h3 class="theme-name">{{ $t(`themes.${theme.code}`) }}</h3>
          </div>
        </div>
        <div class="theme-actions">
          <button class="theme-toggle-btn" @click="toggleThemes">
            {{ showAllThemes ? $t('common.showLess') : $t('common.showMore') }}
          </button>
        </div>
      </section>

      <!-- 3. Featured Attractions Section with Swiper -->
      <section class="content-section">
        <h2 class="section-title">{{ $t('home.popularAttractions') }}</h2>
        <div v-if="loading">{{ $t('common.loading') }}</div>
        <div v-if="error">{{ error }}</div>
        <Swiper
          v-if="featuredAttractions.length"
          class="card-swiper"
          :modules="swiperModules"
          :centered-slides="true"
          :loop="true"
          :navigation="true"
          :breakpoints="{
            700: { slidesPerView: 2.5, spaceBetween: 20 },
            1024: { slidesPerView: 4, spaceBetween: 30 }
          }"
        >
          <SwiperSlide v-for="attraction in featuredAttractions" :key="attraction.id">
            <router-link :to="'/attractions/' + attraction.id" class="attraction-card-link">
              <div class="attraction-card">
                <img :src="attraction.image_url" :alt="attraction.name" class="attraction-card-image">
                <div class="attraction-card-content">
                  <h3 class="attraction-card-title" :class="{ 'title-accent': isEn }">{{ getPrimaryTitle(attraction) }}</h3>
                  <p v-if="getSecondaryTitle(attraction)" class="name-secondary">{{ getSecondaryTitle(attraction) }}</p>
                  <p class="attraction-card-area">{{ $t(`areas.${attraction.area}`) }}</p>
                </div>
              </div>
            </router-link>
          </SwiperSlide>
        </Swiper>
      </section>

      <!-- 4. Featured Routes Section with Swiper -->
      <section class="content-section">
        <h2 class="section-title">{{ $t('home.featuredRoutes') }}</h2>
         <Swiper
          v-if="featuredRoutes.length"
          class="card-swiper"
          :modules="swiperModules"
          :slides-per-view="1"
          :space-between="30"
          :loop="true"
          :navigation="true"
          :breakpoints="{
            700: { slidesPerView: 2 },
            1024: { slidesPerView: 3 }
          }"
        >
          <SwiperSlide v-for="route in featuredRoutes" :key="route.id">
             <router-link :to="'/routes/' + route.id" class="route-card-link">
              <div class="route-card">
                <div class="route-card-content">
                  <h3 class="route-card-title" :class="{ 'title-accent': isEn }">{{ getRoutePrimaryTitle(route) }}</h3>
                  <p v-if="getRouteSecondaryTitle(route)" class="name-secondary">{{ getRouteSecondaryTitle(route) }}</p>
                  <p class="route-card-description">{{ getRouteSummary(route) }}</p>
                  <span class="route-card-tag">{{ $t('routes.includesAttractionCount', { count: route.attraction_ids.length }) }}</span>
                </div>
              </div>
            </router-link>
          </SwiperSlide>
        </Swiper>
      </section>
    </div>

  </div>
</template>

<style scoped>
.home-page {
  background-color: #f9f9f9;
}

/* --- Hero Section --- */
.hero-section {
  position: relative;
  height: 60vh;
  min-height: 400px;
  color: white;
  overflow: hidden;
}

.hero-swiper, .hero-slide-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.hero-slide-background {
  background-size: cover;
  background-position: center;
  filter: brightness(0.6);
}

.hero-content-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  z-index: 3;
  background: transparent;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.hero-subtitle {
  font-size: 1.25rem;
  max-width: 600px;
  margin-bottom: 2.5rem;
  text-shadow: 0 1px 8px rgba(0,0,0,0.7);
  min-height: 50px; /* Reserve space for subtitle */
}

.hero-cta-button {
  font-family: var(--system-font);
  font-size: 1.2rem;
  font-weight: 600;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  background-color: var(--accent-color);
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.hero-cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
  background-color: #d63031;
}

/* --- General Content Layout --- */
.page-content {
  max-width: 100%;
  margin: 0 auto;
  padding: 4rem 0;
}

.content-section {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2.5rem;
  color: var(--primary-text-color);
}

/* --- Theme Section --- */
.theme-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.theme-card {
  background: var(--card-background-color);
  padding: 1.5rem;
  border-radius: var(--card-border-radius);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--card-shadow);
}

.theme-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
  color: var(--accent-color);
}

.theme-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.theme-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.theme-actions {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.theme-toggle-btn {
  font-family: var(--system-font);
  font-size: 0.95rem;
  font-weight: 600;
  padding: 0.6rem 1.1rem;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  background: var(--card-background-color);
  color: var(--primary-text-color);
  cursor: pointer;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.theme-toggle-btn:hover {
  background: var(--background-color);
  box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

/* --- Card Carousel Sections --- */
.card-swiper {
  padding: 10px 0;
}

.swiper-slide {
  height: auto; /* Let content define height */
  display: flex; /* Use flexbox */
  flex-direction: column; /* Stack items vertically */
  align-items: stretch; /* Stretch children to fill width */
  justify-content: center;
}

.attraction-card-link, .route-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
  width: 100%;
}

.attraction-card {
  background: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.attraction-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.attraction-card-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  flex-shrink: 0;
}

.attraction-card-content {
  padding: 1.5rem;
  flex-grow: 1;
}

.attraction-card-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.attraction-card-area {
  font-size: 0.9rem;
  color: var(--secondary-text-color);
  margin: 0;
}

.name-secondary {
  margin: 0.1rem 0 0.4rem 0;
  color: var(--secondary-text-color);
  font-size: 0.95rem;
}

.title-accent {
  color: var(--accent-color);
}

.route-card {
  background: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  padding: 2rem;
  transition: all 0.3s ease;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  text-align: left;
}

.route-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
  border-left: 5px solid var(--accent-color);
  padding-left: calc(2rem - 5px);
}

.route-card-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
}

.route-card-description {
  font-size: 1rem;
  color: var(--secondary-text-color);
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
}

.route-card-tag {
  font-weight: 500;
  color: var(--accent-color);
  background-color: #ffe5e5;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  align-self: flex-start;
}

/* --- Swiper Custom Styles --- */
:root {
  --swiper-theme-color: var(--accent-color);
}

.hero-section :deep(.swiper-pagination-bullet-active) {
  background-color: white;
}

.hero-section :deep(.swiper-pagination-bullet) {
  background-color: rgba(255, 255, 255, 0.7);
  width: 10px;
  height: 10px;
  transition: all 0.3s ease;
}

.card-swiper :deep(.swiper-button-prev),
.card-swiper :deep(.swiper-button-next) {
  color: var(--accent-color);
  background-color: white;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  box-shadow: var(--card-shadow);
}

.card-swiper :deep(.swiper-button-prev::after),
.card-swiper :deep(.swiper-button-next::after) {
  font-size: 1.2rem;
  font-weight: 700;
}

/* Responsive Adjustments */
@media (max-width: 992px) {
  .hero-title { font-size: 2.8rem; }
}

@media (max-width: 768px) {
  .hero-title { font-size: 2.2rem; }
  .hero-subtitle { font-size: 1.1rem; }
  .section-title { font-size: 2rem; }
  .page-content { padding: 3rem 0; }
  .theme-grid { padding: 0 1rem; }
}

</style>
