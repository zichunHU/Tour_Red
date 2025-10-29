<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  latitude: { type: Number, default: null },
  longitude: { type: Number, default: null },
  address: { type: String, default: '' },
  name: { type: String, default: '' },
})

const { t } = useI18n()

const userLat = ref(null)
const userLng = ref(null)
const locating = ref(false)
const locationError = ref(null)

function toRad(val) { return (val * Math.PI) / 180 }
function haversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371 // km
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat/2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon/2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  return R * c
}

const distanceKm = computed(() => {
  if (userLat.value == null || userLng.value == null || props.latitude == null || props.longitude == null) return null
  const d = haversineDistance(userLat.value, userLng.value, props.latitude, props.longitude)
  return Math.round(d * 10) / 10 // one decimal
})

const walkingMinutes = computed(() => {
  if (distanceKm.value == null) return null
  const kmPerHour = 4.5
  const minutes = Math.round((distanceKm.value / kmPerHour) * 60)
  return minutes
})

const amapUrl = computed(() => {
  if (props.latitude == null || props.longitude == null) return null
  const name = encodeURIComponent(props.name || props.address || 'Destination')
  return `https://uri.amap.com/marker?position=${props.longitude},${props.latitude}&name=${name}`
})

const appleMapsUrl = computed(() => {
  if (props.latitude == null || props.longitude == null) return null
  return `https://maps.apple.com/?daddr=${props.latitude},${props.longitude}`
})

async function getMyLocation() {
  if (!navigator.geolocation) {
    locationError.value = 'Geolocation not supported'
    return
  }
  locating.value = true
  locationError.value = null
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLat.value = pos.coords.latitude
      userLng.value = pos.coords.longitude
      locating.value = false
    },
    (err) => {
      locationError.value = err.message || 'Failed to get location'
      locating.value = false
    },
    { enableHighAccuracy: true, timeout: 10000 }
  )
}

async function copyAddress() {
  try {
    if (props.address) {
      await navigator.clipboard.writeText(props.address)
    }
  } catch (e) {
    // ignore
  }
}
</script>

<template>
  <div class="guide-card">
    <div class="guide-header">🧭 {{ t('map.directions') }}</div>
    <div class="guide-actions">
      <button class="guide-btn" @click="getMyLocation" :disabled="locating">
        {{ locating ? t('common.loading') : t('map.getMyLocation') }}
      </button>
      <a v-if="amapUrl" class="guide-btn link" :href="amapUrl" target="_blank" rel="noopener">{{ t('map.openInAMap') }}</a>
      <a v-if="appleMapsUrl" class="guide-btn link" :href="appleMapsUrl" target="_blank" rel="noopener">{{ t('map.openInAppleMaps') }}</a>
      <button class="guide-btn" @click="copyAddress" :disabled="!address">{{ t('map.copyAddress') }}</button>
    </div>
    <p v-if="address" class="guide-address">{{ address }}</p>
    <p v-if="distanceKm != null" class="guide-meta">
      {{ t('map.distanceFromYou', { km: distanceKm }) }}
      <span v-if="walkingMinutes != null" class="sep">·</span>
      <span v-if="walkingMinutes != null">{{ t('map.walkingTimeApprox', { minutes: walkingMinutes }) }}</span>
    </p>
    <p v-if="locationError" class="guide-error">{{ locationError }}</p>
  </div>
  
</template>

<style scoped>
.guide-card {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px dashed var(--border-color);
  border-radius: 12px;
  background-color: var(--background-color);
}
.guide-header {
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--primary-text-color);
}
.guide-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.guide-btn {
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--border-color);
  background: none;
  border-radius: 999px;
  font-size: 0.9rem;
  cursor: pointer;
  color: var(--primary-text-color);
}
.guide-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.guide-btn.link { text-decoration: none; display: inline-block; }
.guide-address { color: var(--secondary-text-color); margin: 0.25rem 0 0.25rem; }
.guide-meta { color: var(--secondary-text-color); font-size: 0.92rem; margin: 0.25rem 0; }
.guide-error { color: var(--accent-color); font-size: 0.9rem; margin-top: 0.25rem; }
.sep { margin: 0 0.3rem; }
</style>