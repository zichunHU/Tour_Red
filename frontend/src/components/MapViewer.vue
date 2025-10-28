<template>
  <div ref="mapContainer" class="map-viewer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  latitude: Number,
  longitude: Number,
  waypoints: {
    type: Array,
    default: () => []
  }
});

const mapContainer = ref(null);
let map = null; // To hold the map instance

// A reactive ref to hold a normalized list of points
const points = ref([]);

// Watch for any prop changes and update the internal 'points' array
watch(() => [props.latitude, props.longitude, props.waypoints], () => {
  const newPoints = [];
  if (props.latitude && props.longitude) {
    // Handle single point from latitude/longitude props
    newPoints.push({ latitude: props.latitude, longitude: props.longitude });
  } else if (props.waypoints && props.waypoints.length > 0) {
    // Handle array of points from waypoints prop
    newPoints.push(...props.waypoints);
  }
  points.value = newPoints;
}, { immediate: true, deep: true });


const initMap = () => {
  if (typeof AMap === 'undefined') {
    console.error('AMap SDK is not loaded.');
    return;
  }
  map = new AMap.Map(mapContainer.value, {
    zoom: 12,
    viewMode: '3D'
  });
  updateMap(points.value);
};

const updateMap = (currentPoints) => {
  if (!map || !currentPoints || currentPoints.length === 0) {
    return;
  }

  map.clearMap();

  const amapPoints = currentPoints.map(p => new AMap.LngLat(p.longitude, p.latitude));

  if (amapPoints.length === 1) {
    // Single point logic
    map.setCenter(amapPoints[0]);
    map.setZoom(15);
    const marker = new AMap.Marker({
      position: amapPoints[0],
      offset: new AMap.Pixel(-13, -30)
    });
    map.add(marker);
  } else {
    // Multi-point route planning logic
    const driving = new AMap.Driving({
      map: map,
      policy: AMap.DrivingPolicy.LEAST_TIME
    });

    const start = amapPoints[0];
    const end = amapPoints[amapPoints.length - 1];
    const waypoints = amapPoints.slice(1, -1);

    driving.search(start, end, { waypoints: waypoints }, (status, result) => {
      if (status !== 'complete') {
        console.error('Failed to get driving route:', result);
      }
    });
  }
};

onMounted(() => {
  // A small delay can help ensure the AMap script is fully loaded and parsed
  setTimeout(initMap, 150);
});

// Watch the normalized 'points' array to update the map
watch(points, (newPoints) => {
  if (map) { // Ensure map is initialized
    updateMap(newPoints);
  }
}, { deep: true });

</script>

<style scoped>
.map-viewer {
  width: 100%;
  height: 400px; /* Default height, can be overridden by parent */
  border-radius: var(--card-border-radius);
}
</style>
