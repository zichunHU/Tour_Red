<script setup>
import { ref, computed, onMounted } from 'vue';
import MapViewer from '../components/MapViewer.vue';

// --- STATE MANAGEMENT ---
const step = ref('selection');
const interestTags = ref(['革命足迹', '建党伟业', '革命烈士', '抗日战争', '伟人故居', '文化名人']);
const selectedTags = ref([]);
const allAttractions = ref([]);
const selectedAttractions = ref(new Set());
const generatedRoute = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await fetch('/api/attractions');
    if (!response.ok) throw new Error('Failed to fetch attractions');
    allAttractions.value = await response.json();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
});

// --- COMPUTED PROPERTIES ---
const filteredAttractions = computed(() => {
  if (selectedTags.value.length === 0) {
    return allAttractions.value;
  }
  return allAttractions.value.filter(attraction => 
    selectedTags.value.every(tag => attraction.theme && attraction.theme.includes(tag))
  );
});

const selectedAttractionsArray = computed(() => Array.from(selectedAttractions.value));

// --- METHODS ---

function toggleAttractionSelection(attractionId) {
  if (selectedAttractions.value.has(attractionId)) {
    selectedAttractions.value.delete(attractionId);
  } else {
    selectedAttractions.value.add(attractionId);
  }
}

async function handleGenerateRoute() {
  if (selectedAttractions.value.size < 2) return;
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch('/api/routes/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ attraction_ids: selectedAttractionsArray.value }),
    });
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.error || 'Failed to generate route');
    }
    generatedRoute.value = await response.json();
    step.value = 'results';
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

function startOver() {
  step.value = 'selection';
  selectedAttractions.value.clear();
  generatedRoute.value = null;
  error.value = null;
}

</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <h2>个性化路线定制</h2>
      <p v-if="step === 'selection'">选择您感兴趣的主题和景点，我们将为您生成专属的红色路线</p>
      <p v-else>根据您的选择，我们为您生成了如下专属路线</p>
    </header>

    <div v-if="error" class="error-message">处理失败: {{ error }}</div>

    <Transition name="fade" mode="out-in">
      <!-- Step 1: Selection Phase -->
      <section v-if="step === 'selection'" key="selection">
        <div class="step-header">
          <span class="step-number">1</span>
          <h3>选择兴趣主题</h3>
        </div>
        <div class="filters-container">
          <div class="tag-group">
            <label v-for="tag in interestTags" :key="tag" class="tag-chip">
              <input type="checkbox" :value="tag" v-model="selectedTags">
              <span class="checkmark">✓</span>
              <span>{{ tag }}</span>
            </label>
          </div>
        </div>

        <div v-if="loading && !allAttractions.length">正在加载景点...</div>
        
        <div class="step-header">
          <span class="step-number">2</span>
          <h3>选择您想去的景点 (已选 {{ selectedAttractions.size }} 个)</h3>
        </div>
        <div v-if="!loading || allAttractions.length" class="selection-grid">
          <div class="attraction-list-container">
            <ul class="attraction-list">
              <li v-for="attraction in filteredAttractions" :key="attraction.id" @click="toggleAttractionSelection(attraction.id)" :class="{ selected: selectedAttractions.has(attraction.id) }">
                <img :src="attraction.image_url" :alt="attraction.name" class="attraction-thumbnail" v-if="attraction.image_url"/>
                <div class="attraction-info">
                  <h5>{{ attraction.name }}</h5>
                  <p>{{ attraction.area }}</p>
                </div>
                <span class="selected-indicator">✓</span>
              </li>
              <li v-if="filteredAttractions.length === 0" class="no-results-li">没有匹配该主题的景点</li>
            </ul>
          </div>
          <div class="map-container-wrapper">
            <MapViewer 
              :waypoints="filteredAttractions" 
              :selected-ids="selectedAttractions"
              :interaction-enabled="true"
              @marker-click="toggleAttractionSelection"
            />
          </div>
        </div>

        <div class="actions-footer">
          <button @click="handleGenerateRoute" :disabled="selectedAttractions.size < 2 || loading" class="button-primary">
            <span v-if="loading">正在生成...</span>
            <span v-else>生成我的专属路线</span>
          </button>
          <p v-if="selectedAttractions.size < 2 && !loading" class="disabled-reason">
            请至少选择两个景点以生成路线
          </p>
        </div>
      </section>

      <!-- Step 2: Results Phase -->
      <section v-else-if="step === 'results' && generatedRoute" key="results">
        <div class="results-grid">
          <div class="route-list-container">
            <h4>推荐路线顺序</h4>
            <ol class="itinerary-list">
              <li v-for="(attraction, index) in generatedRoute.attractions" :key="attraction.id">
                <div class="itinerary-stop">
                  <div class="stop-number">{{ index + 1 }}</div>
                  <div class="stop-info">
                    <h5>{{ attraction.name }}</h5>
                    <p>{{ attraction.address }}</p>
                  </div>
                </div>
              </li>
            </ol>
          </div>
          <div class="map-container-wrapper">
            <MapViewer :waypoints="generatedRoute.attractions" />
          </div>
        </div>

        <div class="actions-footer">
          <button @click="startOver" class="button-secondary">重新规划</button>
        </div>
      </section>
    </Transition>

  </div>
</template>

<style scoped>
/* --- Transitions --- */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.step-number {
  background-color: var(--accent-color);
  color: white;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.step-header h3 {
  margin: 0;
  font-size: 1.5rem;
}

.error-message {
  background-color: #ffe5e5;
  color: var(--accent-color);
  text-align: center;
  padding: 1rem;
  border-radius: 8px;
  margin: 1.5rem 0;
}

/* --- Tag Chips --- */
.filters-container {
  background-color: var(--card-background-color);
  padding: 1.5rem;
  border-radius: var(--card-border-radius);
  margin-bottom: 2rem;
  box-shadow: var(--card-shadow);
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  background-color: var(--background-color);
}

.tag-chip input {
  display: none; /* Hide the actual checkbox */
}

.tag-chip .checkmark {
  display: none;
  margin-right: 0.4rem;
  font-weight: bold;
}

.tag-chip:hover {
  border-color: var(--accent-color);
  background-color: #fff5f5;
}

.tag-chip input:checked + .checkmark {
  display: inline;
}

.tag-chip input:checked ~ span {
  font-weight: 600;
}

.tag-chip input:checked {
  /* Style the parent label when checkbox is checked */
  & + .checkmark + span {
    color: var(--accent-color);
  }
  & ~ * {
    color: var(--accent-color);
  }
  &, & ~ .checkmark, & ~ span {
    color: var(--accent-color);
  }
  & ~ .tag-chip {
    background-color: #ffe5e5;
    border-color: var(--accent-color);
  }
}

.tag-chip input:checked + .checkmark + span {
  color: var(--accent-color);
}

.tag-chip input:checked + .checkmark {
  color: var(--accent-color);
}

.tag-chip input:checked ~ .tag-chip {
    background-color: #ffe5e5;
    border-color: var(--accent-color);
}

/* --- Selection Grid & Lists --- */
.selection-grid, .results-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 2rem;
  min-height: 600px;
}

.attraction-list-container, .route-list-container {
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  overflow-y: auto;
  max-height: 600px;
  padding: 0.5rem;
}

.attraction-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.attraction-list li {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: background-color 0.2s;
  position: relative;
}

.attraction-list li:last-child {
  border-bottom: none;
}

.attraction-list li:hover {
  background-color: #f5f6fa;
}

.attraction-thumbnail {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

.attraction-info h5 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
}

.attraction-info p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--secondary-text-color);
}

.selected-indicator {
  display: none;
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--accent-color);
  font-size: 1.5rem;
  font-weight: bold;
}

.attraction-list li.selected {
  background-color: #e3f2fd;
}

.attraction-list li.selected .selected-indicator {
  display: block;
}

.no-results-li {
  text-align: center;
  color: var(--secondary-text-color);
  padding: 2rem;
  cursor: default !important;
}

.map-container-wrapper {
  position: relative;
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  padding: 0; /* Remove padding */
  display: flex;
  overflow: hidden; /* Hide potential overflow from child radius */
}

.map-container-wrapper > .map-viewer {
  flex-grow: 1;
}

/* --- Footer --- */
.actions-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.button-primary, .button-secondary {
  font-family: var(--system-font);
  font-size: 1.2rem;
  font-weight: 600;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-primary {
  background-color: var(--accent-color);
  color: white;
}

.button-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.disabled-reason {
  margin-top: 1rem;
  color: var(--secondary-text-color);
  font-size: 0.9rem;
}

.button-secondary {
   background-color: var(--background-color);
   color: var(--primary-text-color);
   border: 1px solid var(--border-color);
}

.button-secondary:hover {
  background-color: #e5e5ea;
}

/* --- Itinerary Results View --- */
.itinerary-list {
  list-style: none;
  padding: 0;
  margin: 0;
  position: relative;
}

/* The connecting line */
.itinerary-list::before {
  content: '';
  position: absolute;
  left: 26px; /* Align with center of stop-number */
  top: 20px;
  bottom: 20px;
  width: 2px;
  background-color: var(--border-color);
}

.itinerary-stop {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem 0;
  position: relative;
}

.stop-number {
  background-color: var(--card-background-color);
  border: 2px solid var(--border-color);
  color: var(--accent-color);
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
  z-index: 1;
}

.stop-info h5 {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
}

.stop-info p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--secondary-text-color);
}

</style>
