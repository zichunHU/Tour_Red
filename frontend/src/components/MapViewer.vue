<template>
  <div ref="mapContainer" class="map-viewer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  waypoints: {
    type: Array,
    default: () => []
  }
})

const mapContainer = ref(null)
let map = null // To hold the map instance

const initMap = () => {
  if (typeof AMap === 'undefined') {
    console.error('AMap SDK is not loaded.');
    return;
  }

  map = new AMap.Map(mapContainer.value, {
    zoom: 12, // Default zoom
    viewMode: '3D'
  });

  updateMap(props.waypoints);
}

const updateMap = (newWaypoints) => {
  if (!map || !newWaypoints || newWaypoints.length === 0) {
    return;
  }

  map.clearMap();

  const points = newWaypoints.map(wp => new AMap.LngLat(wp.longitude, wp.latitude));

  if (points.length === 1) {
    // Single point logic
    map.setCenter(points[0]);
    map.setZoom(15);
    const marker = new AMap.Marker({
      position: points[0],
      offset: new AMap.Pixel(-13, -30)
    });
    map.add(marker);
  } else {
    // Multi-point route planning logic, assuming AMap.Driving is pre-loaded
    const driving = new AMap.Driving({
      map: map,
      policy: AMap.DrivingPolicy.LEAST_TIME
    });

    const start = points[0];
    const end = points[points.length - 1];
    const waypoints = points.slice(1, -1);

    driving.search(start, end, { waypoints: waypoints }, (status, result) => {
      if (status === 'complete') {
        // Route drawn successfully by the plugin
      } else {
        console.error('Failed to get driving route:', result);
      }
    });
  }
}

onMounted(() => {
  setTimeout(initMap, 100); // Delay to ensure AMap script is loaded
});

// Watch for prop changes to update the route
watch(() => props.waypoints, (newWaypoints) => {
  updateMap(newWaypoints);
}, { deep: true });

</script>

<style scoped>
.map-viewer {
  width: 100%;
  height: 400px; /* Default height, can be overridden by parent */
  border-radius: var(--card-border-radius);
}
</style>
