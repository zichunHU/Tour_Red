<script setup>
import { ref, computed, onMounted } from 'vue';
import MapViewer from '../components/MapViewer.vue';
import Stepper from '../components/Stepper.vue';
import TagChip from '../components/TagChip.vue';
import LoadingSkeleton from '../components/LoadingSkeleton.vue';
import Toast from '../components/Toast.vue';

// --- DISTANCE UTILS & RESULT METRICS ---
function haversineKm(lat1, lon1, lat2, lon2) {
  const toRad = (v) => (v * Math.PI) / 180;
  const R = 6371; // km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

const routeSegments = computed(() => {
  if (!generatedRoute.value || !generatedRoute.value.attractions) return [];
  const attrs = generatedRoute.value.attractions;
  return attrs.map((attr, idx) => {
    let distanceFromPrevKm = null;
    if (idx > 0 && attr.location && attrs[idx - 1].location) {
      const prev = attrs[idx - 1].location;
      const cur = attr.location;
      distanceFromPrevKm = haversineKm(prev.latitude, prev.longitude, cur.latitude, cur.longitude);
    }
    return { index: idx, attraction: attr, distanceFromPrevKm };
  });
});

const totalDistanceKm = computed(() => routeSegments.value.reduce((sum, s) => sum + (s.distanceFromPrevKm || 0), 0));

// --- STATE MANAGEMENT ---

// Overall step control: 'selection' or 'results'
const step = ref('selection');

// Step 1: Tag and Attraction Selection
const interestTags = ref(['革命足迹', '建党伟业', '革命烈士', '抗日战争', '伟人故居', '文化名人']);
const selectedTags = ref([]);
const allAttractions = ref([]);
const selectedAttractions = ref(new Set()); // Using a Set for efficient add/delete

// Step 2: Generated Route
const generatedRoute = ref(null);

// --- DATA FETCHING ---
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

// Filter attractions based on selected tags
const filteredAttractions = computed(() => {
  if (selectedTags.value.length === 0) {
    return allAttractions.value;
  }
  return allAttractions.value.filter(attraction => 
    selectedTags.value.every(tag => attraction.theme && attraction.theme.includes(tag))
  );
});

// Convert selected attraction IDs from the Set to an array for the template
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
      headers: {
        'Content-Type': 'application/json',
      },
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
  error.value = null; // Clear previous errors
}

</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <h2>个性化路线定制</h2>
      <p>选择您感兴趣的主题和景点，我们将为您生成专属的红色路线</p>
      <Stepper :steps="[{ key: 'selection', label: '选择' }, { key: 'results', label: '结果' }]" :current="step" />
    </header>

    <!-- Step 1: Selection Phase -->
    <section v-if="step === 'selection'">
      <!-- Interest Tag Filters -->
      <div class="filters-container">
        <h4>1. 选择兴趣主题</h4>
        <div class="tag-group">
          <TagChip
            v-for="tag in interestTags"
            :key="tag"
            :selected="selectedTags.includes(tag)"
            @toggle="() => { const i = selectedTags.indexOf(tag); if (i >= 0) selectedTags.splice(i,1); else selectedTags.push(tag); }"
          >{{ tag }}</TagChip>
        </div>
      </div>

      <LoadingSkeleton v-if="loading" :count="6" />
      <Toast v-if="error" :visible="true" :message="error" type="error" @close="error = null" />

      <!-- Attraction Selection -->
      <div v-if="!loading && !error" class="selection-grid">
        <div class="attraction-list-container">
          <h4>2. 选择您想去的景点 (已选 {{ selectedAttractions.size }} 个)</h4>
          <ul class="attraction-list">
            <li v-for="attraction in filteredAttractions" :key="attraction.id" @click="toggleAttractionSelection(attraction.id)" :class="{ selected: selectedAttractions.has(attraction.id) }">
              <div class="card">
                <div class="card-header">
                  <h5>{{ attraction.name }}</h5>
                  <span class="area-tag">{{ attraction.area }}</span>
                </div>
              </div>
            </li>
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

      <!-- Action Button -->
      <div class="actions-footer sticky">
        <button @click="handleGenerateRoute" :disabled="selectedAttractions.size < 2 || loading" class="button-primary">
          <span v-if="loading">正在生成...</span>
          <span v-else>生成我的专属路线</span>
        </button>
        <p v-if="selectedAttractions.size < 2" class="disabled-reason">
          请至少选择两个景点以生成路线
        </p>
      </div>
    </section>

    <!-- Step 2: Results Phase -->
    <section v-if="step === 'results' && generatedRoute">
      <div class="results-grid">
        <div class="route-list-container">
          <h4>推荐路线顺序</h4>
          <div class="route-summary" v-if="totalDistanceKm">
            总里程约：{{ totalDistanceKm.toFixed(1) }} 公里
          </div>
          <ol class="route-list">
            <li v-for="segment in routeSegments" :key="segment.attraction.id" class="timeline-item">
              <span class="bullet">{{ segment.index + 1 }}</span>
              <div class="route-attraction-info">
                <h5>{{ segment.attraction.name }}</h5>
                <p class="address">{{ segment.attraction.address }}</p>
                <p v-if="segment.index > 0 && segment.distanceFromPrevKm" class="distance">距离上一个点 ≈ {{ segment.distanceFromPrevKm.toFixed(1) }} 公里</p>
              </div>
            </li>
          </ol>
        </div>
        <div class="map-container-wrapper">
          <MapViewer :waypoints="generatedRoute.attractions" />
          <div class="map-hint">若地图未显示，请检查高德 Key 与安全码或网络状态</div>
        </div>
      </div>

      <div class="actions-footer sticky">
        <button @click="startOver" class="button-secondary">重新规划</button>
      </div>
    </section>

  </div>
</template>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.filters-container {
  background-color: var(--card-background-color);
  padding: 1.5rem;
  border-radius: var(--card-border-radius);
  margin-bottom: 2rem;
  box-shadow: var(--card-shadow);
}

.filters-container h4 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag-label {
  display: flex;
  align-items: center;
  background-color: var(--background-color);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  border: 1px solid var(--border-color);
}

.tag-label:hover {
  background-color: #e5e5ea;
}

.tag-label input {
  margin-right: 0.5rem;
}

.tag-label input:checked + span {
  font-weight: 600;
  color: var(--accent-color);
}

.selection-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  min-height: 600px;
}

.attraction-list-container {
  background-color: var(--card-background-color);
  padding: 1.5rem;
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  overflow-y: auto;
  max-height: 600px;
}

.attraction-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.attraction-list li {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: background-color 0.2s;
}

.attraction-list li:last-child {
  border-bottom: none;
}

.attraction-list li:hover {
  background-color: var(--background-color);
}

.attraction-list li.selected {
  background-color: #e3f2fd;
  border-left: 4px solid var(--accent-color);
  padding-left: calc(1rem - 4px);
}

.attraction-list h5 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
}

.attraction-list p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--secondary-text-color);
}

.map-container-wrapper {
  position: relative;
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  padding: 1rem;
}

.map-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  font-size: 1.2rem;
  z-index: 10;
}

.actions-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.disabled-reason {
  margin-top: 1rem;
  color: var(--secondary-text-color);
  font-size: 0.9rem;
}

.button-primary {
  font-family: var(--system-font);
  font-size: 1.2rem;
  font-weight: 600;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  background-color: var(--accent-color);
  color: white;
  transition: background-color 0.3s ease;
}

.button-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.button-secondary {
   /* Style for the start over button */
}

.results-header {
  text-align: center;
  margin-bottom: 2rem;
}
.route-list { list-style: none; padding: 0; margin: 0; }
.timeline-item { display: grid; grid-template-columns: 36px 1fr; gap: 1rem; padding: 0.75rem 0; }
.timeline-item + .timeline-item { border-top: 1px dashed var(--border-color); }
.bullet {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: var(--accent-color);
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}
.route-attraction-info h5 { margin: 0; font-size: 1rem; font-weight: 700; }
.route-attraction-info .address { margin: 0.25rem 0 0 0; color: var(--secondary-text-color); }
.route-attraction-info .distance { margin: 0.25rem 0 0 0; color: var(--secondary-text-color); font-size: 0.85rem; }

.route-summary {
  margin-bottom: 0.75rem;
  padding: 0.5rem 0.75rem;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  display: inline-block;
}

.map-hint { margin-top: 0.5rem; color: var(--secondary-text-color); font-size: 0.85rem; }
.tag-group { display: flex; flex-wrap: wrap; gap: 0.5rem; }

.attraction-list li { cursor: pointer; }
.attraction-list .card {
  background: var(--card-background-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
  transition: border-color 150ms ease, background 150ms ease;
}
.attraction-list .card:hover { background: var(--background-color); }
.attraction-list .card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.area-tag {
  font-size: 0.8rem;
  color: var(--secondary-text-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.15rem 0.5rem;
}
.attraction-list li.selected .card { border-color: var(--accent-color); }

.actions-footer.sticky {
  position: sticky;
  bottom: 0;
  background: var(--card-background-color);
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
}
</style>