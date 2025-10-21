<template>
  <div ref="mapContainer" class="map-viewer"></div>
</template>

<script setup>
import { ref, onMounted, watch, toRefs } from 'vue'

const props = defineProps({
  latitude: {
    type: Number,
    required: true
  },
  longitude: {
    type: Number,
    required: true
  }
})

const { latitude, longitude } = toRefs(props)
const mapContainer = ref(null)
let map = null // To hold the map instance

const initMap = () => {
  if (!latitude.value || !longitude.value) {
    console.warn('MapViewer: Latitude or Longitude is missing.');
    return;
  }

  // Ensure AMap is loaded
  if (typeof AMap === 'undefined') {
    console.error('AMap SDK is not loaded. Please check your index.html and API key.');
    return;
  }

  const center = [longitude.value, latitude.value];

  map = new AMap.Map(mapContainer.value, {
    zoom: 15,
    center: center,
    viewMode: '3D' // Use 3D view
  });

  const marker = new AMap.Marker({
    position: center,
    offset: new AMap.Pixel(-13, -30)
  });

  map.add(marker);
}

onMounted(() => {
  // A small delay might be necessary to ensure the AMap script is fully loaded and executed
  setTimeout(initMap, 100);
});

// Watch for prop changes to recenter the map
watch([latitude, longitude], (newVals) => {
  if (map && newVals[0] && newVals[1]) {
    const newCenter = [newVals[1], newVals[0]];
    map.setCenter(newCenter);
    // Clear existing markers and add a new one
    map.clearMap();
    const marker = new AMap.Marker({
      position: newCenter,
      offset: new AMap.Pixel(-13, -30)
    });
    map.add(marker);
  }
});

</script>

<style scoped>
.map-viewer {
  width: 100%;
  height: 400px; /* Default height, can be overridden by parent */
  border-radius: var(--card-border-radius);
}
</style>
